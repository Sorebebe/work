from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('vacancies.urls')),
    path('api/', include('vacancies.api_urls')),
]