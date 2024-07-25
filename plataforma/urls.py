from django.urls import path
from . import views

urlpatterns = [
    path('gerenciar_pacientes/', views.gerenciar_pacientes, name='gerenciar_pacientes'),
    path('alterar_paciente/', views.alterar_paciente, name='alterar_paciente'),
    path('excluir_paciente/', views.excluir_paciente, name='excluir_paciente'),
    path('lista_dados_paciente/', views.lista_dados_paciente, name='lista_dados_paciente'),
    path('dados_paciente/<str:paciente_id>/', views.dados_paciente, name="dados_paciente"),
    path('grafico_peso/<str:paciente_id>/', views.grafico_peso, name='grafico_peso'),
    path('lista_plano_alimentar/', views.lista_plano_alimentar, name='lista_plano_alimentar'),
    path('plano_alimentar/<str:paciente_id>/', views.plano_alimentar, name='plano_alimentar'),
    path('refeicao/<str:paciente_id>/', views.refeicao, name='refeicao'),
    path('excluir_refeicao/<str:refeicao_id>/', views.excluir_refeicao, name='excluir_refeicao'),
    path('opcao/<str:paciente_id>/', views.opcao, name='opcao'),
    path('excluir_opcao/<str:opcao_id>/', views.excluir_opcao, name='excluir_opcao'),
]
