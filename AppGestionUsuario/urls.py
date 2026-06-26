from django.urls import path
from .views import (
    RegisterView, CustomLoginView, ProfileView, MiProgresoView, 
    ContactoView, UserManagementListView, UserManagementCreateView, 
    UserManagementUpdateView, UserToggleStatusView,
    AdminContentDashboardView, AdminConfigUpdateView, AdminPaginaUpdateView,
    BadgeManagementListView, BadgeManagementCreateView, BadgeManagementUpdateView, BadgeManagementDeleteView,
    AdminProfileListView, AdminProfileUpdateView,
    AdminTemaListView, AdminTemaCreateView, AdminTemaUpdateView,
    AdminContenidoTemaListView, AdminContenidoTemaCreateView, AdminContenidoTemaUpdateView,
    AdminResultadoDiagnosticoListView, AdminResultadoDiagnosticoUpdateView,
    AdminRecomendacionListView, AdminRecomendacionCreateView, AdminRecomendacionUpdateView,
    GetUserDataView
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

    # Gestión de insignias
    path('admin/insignias/', BadgeManagementListView.as_view(), name='admin_badge_list'),
    path('admin/insignias/nueva/', BadgeManagementCreateView.as_view(), name='admin_badge_create'),
    path('admin/insignias/editar/<int:pk>/', BadgeManagementUpdateView.as_view(), name='admin_badge_update'),
    path('admin/insignias/eliminar/<int:pk>/', BadgeManagementDeleteView.as_view(), name='admin_badge_delete'),

    # Menu lateral de administrador
    path('admin/perfiles/', AdminProfileListView.as_view(), name='admin_profile_list'),
    path('admin/perfiles/editar/<int:pk>/', AdminProfileUpdateView.as_view(), name='admin_profile_update'),
    path('admin/temas/', AdminTemaListView.as_view(), name='admin_tema_list'),
    path('admin/temas/nuevo/', AdminTemaCreateView.as_view(), name='admin_tema_create'),
    path('admin/temas/editar/<int:pk>/', AdminTemaUpdateView.as_view(), name='admin_tema_update'),
    path('admin/contenido-teorico/', AdminContenidoTemaListView.as_view(), name='admin_contenido_tema_list'),
    path('admin/contenido-teorico/nuevo/', AdminContenidoTemaCreateView.as_view(), name='admin_contenido_tema_create'),
    path('admin/contenido-teorico/editar/<int:pk>/', AdminContenidoTemaUpdateView.as_view(), name='admin_contenido_tema_update'),
    path('admin/resultados-diagnostico/', AdminResultadoDiagnosticoListView.as_view(), name='admin_resultado_diagnostico_list'),
    path('admin/resultados-diagnostico/editar/<int:pk>/', AdminResultadoDiagnosticoUpdateView.as_view(), name='admin_resultado_diagnostico_update'),
    path('admin/recomendaciones/', AdminRecomendacionListView.as_view(), name='admin_recomendacion_list'),
    path('admin/recomendaciones/nueva/', AdminRecomendacionCreateView.as_view(), name='admin_recomendacion_create'),
    path('admin/recomendaciones/editar/<int:pk>/', AdminRecomendacionUpdateView.as_view(), name='admin_recomendacion_update'),
    path('api/user-data/<int:pk>/', GetUserDataView.as_view(), name='get_user_data'),
]
