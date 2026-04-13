from django.urls import path
from . import views

urlpatterns = [
    path('rendir/<int:examen_id>/', views.rendir_examen, name='rendir_examen'),
    path('resultados/<int:examen_id>/', views.ver_resultados, name='ver_resultados'),
    path('practica/iniciar/', views.iniciar_practica, name='iniciar_practica'),
    path('practica/validar/', views.validar_respuesta, name='validar_respuesta'),
    path('historial/', views.HistorialResultadosView.as_view(), name='historial_resultados'),
    path('reportes/', views.ReportesDocenteView.as_view(), name='reportes_docente'),
    path('reportes/data/', views.ReportesDataJSONView.as_view(), name='reportes_data_json'),
    path('reportes/exportar/', views.ExportarReporteExcelView.as_view(), name='exportar_reporte_excel'),
    path('banco-preguntas/', views.BancoPreguntasListView.as_view(), name='banco_preguntas_list'),
    path('banco-preguntas/nuevo/', views.BancoPreguntasCreateView.as_view(), name='banco_preguntas_create'),
    path('banco-preguntas/editar/<int:pk>/', views.BancoPreguntasUpdateView.as_view(), name='banco_preguntas_edit'),
]
