from django.db import models
from django.contrib.auth.models import User



class EmployerProfile(models.Model):
    """Профиль работодателя (переехал из accounts)"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200, verbose_name='Название компании')
    email = models.EmailField(verbose_name='Почта')
    address = models.CharField(max_length=300, verbose_name='Адрес')
    
    def __str__(self):
        return f"{self.company_name} ({self.user.username})"


class DjangoVacancy(models.Model):
    """Модель вакансии для базы данных"""
    title = models.CharField(max_length=200, verbose_name='Название')
    company = models.CharField(max_length=200, verbose_name='Компания')
    sphere = models.CharField(max_length=50, verbose_name='Сфера')
    employer_id = models.IntegerField(verbose_name='ID Работодателя', default=0)

    class Meta:
        db_table = 'vacancies_vacancy' 

    def __str__(self):
        return self.title

class Sphere(models.TextChoices):
    IT = 'IT', 'Информационные технологии'
    MEDICINE = 'MEDICINE', 'Медицина'
    ARCHITECTURE = 'ARCHITECTURE', 'Архитектура'

class Vacancy(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название вакансии')
    company = models.CharField(max_length=200, verbose_name='Компания')
    sphere = models.CharField(max_length=20, choices=Sphere.choices, verbose_name='Сфера деятельности')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    employer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Работодатель', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-created_at']
        db_table = 'vacancies_vacancy_new' 

class Response(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='responses')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} → {self.vacancy.title}"


