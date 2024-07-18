from django.urls import path
from . import views

urlpatterns = [
    path('gerenciar_pacientes/', views.gerenciar_pacientes, name='gerenciar_pacientes'),
    path('lista_pacientes/', views.lista_pacientes, name='lista_pacientes'),
    path('dados_paciente/<str:paciente_id>/', views.dados_paciente, name="dados_paciente"),
    path('grafico_peso/<str:paciente_id>/', views.grafico_peso, name='grafico_peso'),
    path('lista_plano_alimentar/', views.lista_plano_alimentar, name='lista_plano_alimentar'),
    path('plano_alimentar/<str:paciente_id>/', views.plano_alimentar, name='plano_alimentar'),
]
