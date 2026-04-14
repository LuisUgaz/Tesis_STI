from django.urls import path
from .views import (
    RegisterView, CustomLoginView, ProfileView, MiProgresoView, 
    ContactoView, UserManagementListView, UserManagementCreateView, 
    UserManagementUpdateView, UserToggleStatusView,
    AdminContentDashboardView, AdminConfigUpdateView, AdminPaginaUpdateView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('mi-progreso/', MiProgresoView.as_view(), name='mi_progreso'),
    path('contacto/', ContactoView.as_view(), name='contacto'),
    path('admin/usuarios/', UserManagementListView.as_view(), name='admin_user_list'),
    path('admin/usuarios/nuevo/', UserManagementCreateView.as_view(), name='admin_user_create'),
    path('admin/usuarios/editar/<int:pk>/', UserManagementUpdateView.as_view(), name='admin_user_update'),
    path('admin/usuarios/toggle-status/<int:pk>/', UserToggleStatusView.as_view(), name='admin_user_toggle_status'),
    
    # Gestión de contenidos generales
    path('admin/contenidos/', AdminContentDashboardView.as_view(), name='admin_content_dashboard'),
    path('admin/contenidos/configuracion/', AdminConfigUpdateView.as_view(), name='admin_config_edit'),
    path('admin/contenidos/pagina/<int:pk>/editar/', AdminPaginaUpdateView.as_view(), name='admin_pagina_edit'),
]
