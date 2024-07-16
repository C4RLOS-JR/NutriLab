from django.urls import path
from . import views

urlpatterns = [
    path('gerenciar_pacientes/', views.gerenciar_pacientes, name='gerenciar_pacientes'),
    path('lista_pacientes/', views.lista_pacientes, name='lista_pacientes'),
    path('dados_paciente/<str:paciente_id>/', views.dados_paciente, name="dados_paciente"),
]
