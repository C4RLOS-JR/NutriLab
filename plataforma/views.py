from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Pacientes, DadosPaciente
from django.contrib import messages
from django.contrib.messages import constants
from datetime import datetime

@login_required(login_url='/auth/logar')
def gerenciar_pacientes(request):
  if request.method == 'GET':
    pacientes = Pacientes.objects.filter(nutri=request.user)
    return render(request, 'pacientes.html', {'pacientes': pacientes})
  
  elif request.method == 'POST':
    nome = request.POST.get('nome')
    sexo = request.POST.get('sexo')
    idade = request.POST.get('idade')
    email = request.POST.get('email')
    telefone = request.POST.get('telefone')

    if (len(nome.strip())==0) or (len(sexo.strip())==0) or (len(idade.strip())==0) or (len(email.strip())==0) or (len(telefone.strip())==0):
      messages.add_message(request, constants.ERROR, 'Cadastro não realizado, todos os campos devem ser preenchidos!')
      return redirect('/gerenciar_pacientes')
    
    if not idade.isnumeric():
      messages.add_message(request, constants.ERROR, 'Digite uma idade válida!')
      return redirect('/gerenciar_pacientes')
    
    paciente_existe = Pacientes.objects.filter(email=email)
    if paciente_existe:
      messages.add_message(request, constants.ERROR, 'Já existe um paciente com esse email cadastrado no sistema!')
      return redirect('/gerenciar_pacientes')

    try:
      paciente = Pacientes(
        nome = nome,
        sexo = sexo,
        idade = idade,
        email = email,
        telefone = telefone,
        nutri = request.user
      )
      paciente.save()
      messages.add_message(request, constants.SUCCESS, 'Paciente cadastrado com sucesso!')
    except:
      messages.add_message(request, constants.ERROR, 'Erro interno do sistema, tente novamente!')

    return redirect('/gerenciar_pacientes')

@login_required(login_url='/auth/logar')
def lista_pacientes(request):
  if request.method == 'GET':
    pacientes = Pacientes.objects.filter(nutri=request.user)
    return render(request, 'lista_pacientes.html', {'pacientes': pacientes})
  
@login_required(login_url='/auth/logar')
def dados_paciente(request, paciente_id):
  paciente = get_object_or_404(Pacientes, id=paciente_id)

  if not paciente.nutri == request.user:
    messages.add_message(request, constants.ERROR, 'Esse paciente não é seu!')
    return redirect('/lista_pacientes')
  
  if request.method == 'GET':
    dados = DadosPaciente.objects.filter(paciente_id=paciente_id)
    
    return render(request, 'dados_paciente.html', {'paciente': paciente, 'dados': dados})
  elif request.method == "POST":
    peso = request.POST.get('peso')
    altura = request.POST.get('altura')
    gordura = request.POST.get('gordura')
    musculo = request.POST.get('musculo')

    hdl = request.POST.get('hdl')
    ldl = request.POST.get('ldl')
    colesterol_total = request.POST.get('ctotal')
    triglicerídios = request.POST.get('triglicerídios')

    if ((len(peso.strip())==0) or (len(altura.strip())==0) or (len(gordura.strip())==0) or (len(musculo.strip())==0) or 
        (len(hdl.strip())==0) or (len(ldl.strip())==0) or (len(colesterol_total.strip())==0) or (len(triglicerídios.strip())==0)):
      messages.add_message(request, constants.ERROR, 'Dados não adicionados. Todos os campos devem ser preenchidos!')
      return redirect(f'/dados_paciente/{paciente_id}')
    
    if ((not peso.isnumeric()) or (not altura.isnumeric()) or (not gordura.isnumeric()) or (not musculo.isnumeric()) or 
            (not hdl.isnumeric()) or (not ldl.isnumeric()) or (not colesterol_total.isnumeric()) or (not triglicerídios.isnumeric())):
      messages.add_message(request, constants.ERROR, 'Dados não adicionados. Os dados precisam ser numéricos!')
      return redirect(f'/dados_paciente/{paciente_id}')

    try:
      dados_paciente = DadosPaciente(
        paciente = paciente,
        data = datetime.now().date(),
        peso = peso,
        altura = altura,
        percentual_gordura = gordura,
        percentual_musculo = musculo,
        colesterol_hdl = hdl,
        colesterol_ldl = ldl,
        colesterol_total = colesterol_total,
        trigliceridios = triglicerídios
      )
      dados_paciente.save()
      messages.add_message(request, constants.SUCCESS, 'Dados cadastrados com sucesso!')
    except:
      messages.add_message(request, constants.ERROR, 'Algo deu errado, tente novamente ou entre em contato com a administração!')

    return redirect(f'/dados_paciente/{paciente_id}')
