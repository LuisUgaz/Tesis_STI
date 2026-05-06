from django.urls import path
from . import views

app_name = 'evaluar'

urlpatterns = [
    path('rendir/<int:examen_id>/', views.rendir_examen, name='rendir_examen'),
    path('resultados/<int:examen_id>/', views.ver_resultados, name='ver_resultados'),
    path('practica/iniciar/', views.iniciar_practica, name='iniciar_practica'),
    path('practica/validar/', views.validar_respuesta, name='validar_respuesta'),
    path('historial/', views.HistorialResultadosView.as_view(), name='historial_resultados'),
    path('reportes/', views.ReportesDocenteView.as_view(), name='reportes_docente'),
    path('reportes/data/', views.ReportesDataJSONView.as_view(), name='reportes_data_json'),
    path('reportes/estudiante/<int:user_id>/', views.EstudianteDetalleJSONView.as_view(), name='reporte_estudiante_detalle'),
    path('reportes/exportar/', views.ExportarReporteExcelView.as_view(), name='exportar_reporte_excel'),
    path('banco-preguntas/', views.BancoPreguntasListView.as_view(), name='banco_preguntas_list'),
    path('banco-preguntas/nuevo/', views.BancoPreguntasCreateView.as_view(), name='banco_preguntas_create'),
    path('banco-preguntas/importar/', views.ImportarBancoPreguntasView.as_view(), name='importar_banco'),
    path('banco-preguntas/confirmar/', views.ConfirmarImportacionView.as_view(), name='confirmar_importacion'),
    path('banco-preguntas/editar/<int:pk>/', views.BancoPreguntasUpdateView.as_view(), name='banco_preguntas_edit'),
    path('banco-preguntas/eliminar/<int:pk>/', views.BancoPreguntasDeleteView.as_view(), name='banco_preguntas_delete'),
    
    # Gestión de Exámenes por Tema (HU39)
    path('examenes/', views.ExamenDashboardView.as_view(), name='examen_dashboard'),
    path('examenes/nuevo/', views.ExamenCreateView.as_view(), name='examen_create'),
    path('examenes/editar/<int:pk>/', views.ExamenUpdateView.as_view(), name='examen_update'),
    path('examenes/eliminar/<int:pk>/', views.ExamenDeleteView.as_view(), name='examen_delete'),

    # Rendición de Exámenes de Tema (HU41 Refactor)
    path('examenes/rendir/<int:examen_id>/', views.rendir_examen_tema, name='rendir_examen_tema'),
    path('examenes/resultados/<int:examen_id>/', views.ver_resultados_tema, name='ver_resultados_tema'),

    # Retroalimentación Inteligente (HU40)
    path('ia-feedback/<int:respuesta_id>/', views.IAFeedbackView.as_view(), name='ia_feedback'),
]
