"""
URL configuration for hospital_system project.
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from hospital_app import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.index, name='index'),
    path('doctors/<int:doctor_id>/', views.doctor_detail, name="doctor_detail")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)