# vacancies/views.py

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import Http404

# Импортируем сущности ядра и локальную модель профиля
from core.entities.vacancy import Sphere as DomainSphere
from .models import EmployerProfile

# Импортируем фабрику сценариев
from employment_project.dependencies import (
    get_list_vacancies_use_case, get_create_vacancy_use_case,
    get_respond_to_vacancy_use_case, get_update_vacancy_use_case,
    get_delete_vacancy_use_case
)

# ==========================================
# ЛОГИКА АККАУНТОВ (Переехала из accounts)
# ==========================================

def register(request):
    """Регистрация нового работодателя"""
    if request.method == 'POST':
        print("========== ПОЛУЧЕН POST-ЗАПРОС ==========")
        print("Данные из формы:", request.POST)
        
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        company_name = request.POST.get('company_name', '').strip()
        email = request.POST.get('email', '').strip()
        address = request.POST.get('address', '').strip()
        
        if not username or not password or not company_name:
            print("ОШИБКА: Одно из полей пустое!")
            messages.error(request, 'Пожалуйста, заполните все обязательные поля формы.')
            return render(request, 'vacancies/register.html')
            
        if User.objects.filter(username=username).exists():
            print(f"ОШИБКА: Пользователь '{username}' уже существует в базе!")
            messages.error(request, 'Пользователь с таким логином уже существует')
            return render(request, 'vacancies/register.html')
        
        # ... (здесь идет старый код создания пользователя)
        user = User.objects.create_user(username=username, password=password)
        employer_group, _ = Group.objects.get_or_create(name='Работодатели')
        user.groups.add(employer_group)
        
        EmployerProfile.objects.create(
            user=user, company_name=company_name, email=email, address=address
        )
        
        print("УСПЕХ: Пользователь успешно создан. Перенаправляем на логин.")
        messages.success(request, 'Регистрация успешна! Теперь вы можете войти.')
        return redirect('login')
    
    return render(request, 'vacancies/register.html')


def vacancy_list(request):
    """Список вакансий"""
    sphere_filter = request.GET.get('sphere', '')
    page_number = int(request.GET.get('page', 1))
    
    use_case = get_list_vacancies_use_case()
    result = use_case.execute(sphere=sphere_filter if sphere_filter else None, page=page_number, page_size=2)
    
    class DjangoPageAdapter:
        def __init__(self, items, page, total_pages):
            self.object_list = items
            self.number = page
            self.paginator = type('DummyPaginator', (object,), {'num_pages': total_pages})()
            self.has_previous = page > 1
            self.has_next = page < total_pages
            self.previous_page_number = page - 1
            self.next_page_number = page + 1
            
        def __iter__(self):
            return iter(self.object_list)
            
    adapted_vacancies = DjangoPageAdapter(result['items'], result['page'], result['total_pages'])
    
    context = {
        'vacancies': adapted_vacancies,
        'spheres': DomainSphere.choices(),
        'current_sphere': sphere_filter,
    }
    return render(request, 'vacancies/vacancy_list.html', context)


def vacancy_detail(request, pk):
    """Детали вакансии"""
    use_case = get_list_vacancies_use_case()
    vacancy = use_case.vacancy_repo.get_by_id(pk)
    if vacancy is None:
        raise Http404("Вакансия не найдена")
    return render(request, 'vacancies/vacancy_detail.html', {'vacancy': vacancy})


def vacancy_response(request, pk):
    """Отклик на вакансию"""
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        
        if not first_name or not last_name or not phone:
            return render(request, 'vacancies/response_error.html', {'error': 'Заполните все поля!'})
        
        try:
            use_case = get_respond_to_vacancy_use_case()
            use_case.execute(vacancy_id=pk, first_name=first_name, last_name=last_name, phone=phone)
            return render(request, 'vacancies/response_success.html')
        except ValueError as e:
            return render(request, 'vacancies/response_error.html', {'error': str(e)})
            
    return redirect('vacancy_detail', pk=pk)


class VacancyCreateView(LoginRequiredMixin, View):
    """Создание вакансии"""
    def get(self, request):
        if request.user.is_superuser or not request.user.groups.filter(name='Работодатели').exists():
            messages.error(request, 'Доступ запрещен. Администраторы не могут добавлять вакансии.')
            return redirect('vacancy_list')
        
        try:
            company_name = request.user.employerprofile.company_name
        except EmployerProfile.DoesNotExist:
            messages.error(request, 'Профиль работодателя не найден.')
            return redirect('vacancy_list')
            
        return render(request, 'vacancies/vacancy_form.html', {
            'spheres': DomainSphere.choices(),
            'company_name': company_name,
        })
    
    def post(self, request):
        if request.user.is_superuser or not request.user.groups.filter(name='Работодатели').exists():
            messages.error(request, 'Доступ запрещен.')
            return redirect('vacancy_list')
            
        title = request.POST.get('title', '').strip()
        sphere = request.POST.get('sphere', '')
        company_name = request.user.employerprofile.company_name
        
        try:
            use_case = get_create_vacancy_use_case()
            use_case.execute(title=title, company=company_name, sphere=sphere, employer_id=request.user.id)
            messages.success(request, f'Вакансия "{title}" успешно добавлена!')
            return redirect('vacancy_list')
        except ValueError as e:
            return render(request, 'vacancies/vacancy_form.html', {
                'error': str(e),
                'spheres': DomainSphere.choices(),
                'company_name': company_name,
            })


class VacancyUpdateView(LoginRequiredMixin, View):
    """Редактирование вакансии"""
    def get(self, request, pk):
        use_case = get_update_vacancy_use_case()
        vacancy = use_case.vacancy_repo.get_by_id(pk)
        
        if vacancy is None:
            raise Http404("Вакансия не найдена")
            
        if not vacancy.can_be_edited_by(request.user.id, request.user.is_superuser):
            messages.error(request, 'У вас нет прав на редактирование этой вакансии.')
            return redirect('vacancy_detail', pk=pk)
            
        return render(request, 'vacancies/vacancy_form.html', {
            'vacancy': vacancy,
            'spheres': DomainSphere.choices(),
            'company_name': vacancy.company, 
        })
    
    def post(self, request, pk):
        use_case = get_update_vacancy_use_case()
        vacancy = use_case.vacancy_repo.get_by_id(pk)
        
        if vacancy is None:
            raise Http404("Вакансия не найдена")
            
        if not vacancy.can_be_edited_by(request.user.id, request.user.is_superuser):
            messages.error(request, 'У вас нет прав на редактирование этой вакансии.')
            return redirect('vacancy_detail', pk=pk)
            
        title = request.POST.get('title', '').strip()
        sphere = request.POST.get('sphere', '')
        
        try:
            use_case.execute(vacancy_id=pk, title=title, sphere=sphere, user_id=request.user.id, is_admin=request.user.is_superuser)
            messages.success(request, 'Вакансия успешно обновлена.')
            return redirect('vacancy_detail', pk=pk)
        except (ValueError, PermissionError) as e:
            messages.error(request, str(e))
            return redirect('vacancy_detail', pk=pk)


class VacancyDeleteView(LoginRequiredMixin, View):
    """Удаление вакансии"""
    def get(self, request, pk):
        use_case = get_delete_vacancy_use_case()
        vacancy = use_case.vacancy_repo.get_by_id(pk)
        
        if vacancy is None:
            raise Http404("Вакансия не найдена")
            
        if not vacancy.can_be_deleted_by(request.user.id, request.user.is_superuser):
            messages.error(request, 'У вас нет прав на удаление этой вакансии.')
            return redirect('vacancy_detail', pk=pk)
        return render(request, 'vacancies/vacancy_confirm_delete.html', {'vacancy': vacancy})
    
    def post(self, request, pk):
        use_case = get_delete_vacancy_use_case()
        vacancy = use_case.vacancy_repo.get_by_id(pk)
        
        if vacancy is None:
            raise Http404("Вакансия не найдена")
            
        if not vacancy.can_be_deleted_by(request.user.id, request.user.is_superuser):
            messages.error(request, 'У вас нет прав на удаление этой вакансии.')
            return redirect('vacancy_list')
            
        try:
            use_case.execute(vacancy_id=pk, user_id=request.user.id, is_admin=request.user.is_superuser)
            messages.success(request, 'Вакансия успешно удалена.')
        except (ValueError, PermissionError) as e:
            messages.error(request, str(e))
        return redirect('vacancy_list')


from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import VacancySerializer

class VacancyViewSet(viewsets.ViewSet):
    """API для работы с вакансиями"""
    
    def list(self, request):
        sphere = request.query_params.get('sphere')
        page = int(request.query_params.get('page', 1))
        
        use_case = get_list_vacancies_use_case()
        result = use_case.execute(sphere=sphere, page=page, page_size=10)
        
        serializer = VacancySerializer(result['items'], many=True)
        return Response({
            'items': serializer.data,
            'total': result['total']
        })

    def retrieve(self, request, pk=None):
        use_case = get_list_vacancies_use_case()
        vacancy = use_case.vacancy_repo.get_by_id(pk)
        
        if not vacancy:
            raise Http404("Вакансия не найдена")
            
        serializer = VacancySerializer(vacancy)
        return Response(serializer.data)