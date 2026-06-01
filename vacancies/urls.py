from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    path('', views.vacancy_list, name='vacancy_list'),
    path('<int:pk>/', views.vacancy_detail, name='vacancy_detail'),
    path('<int:pk>/respond/', views.vacancy_response, name='vacancy_response'),
    path('create/', views.VacancyCreateView.as_view(), name='vacancy_create'),
    path('<int:pk>/update/', views.VacancyUpdateView.as_view(), name='vacancy_update'),
    path('<int:pk>/delete/', views.VacancyDeleteView.as_view(), name='vacancy_delete'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='vacancies/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='vacancy_list'), name='logout'),
]