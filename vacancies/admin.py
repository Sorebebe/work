from django.contrib import admin
from .models import Vacancy, Response
from .models import EmployerProfile

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'sphere', 'employer', 'created_at']
    list_filter = ['sphere']
    search_fields = ['title', 'company']

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'vacancy', 'created_at']


@admin.register(EmployerProfile)
class EmployerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'company_name', 'email', 'address']
    search_fields = ['company_name', 'user__username']    