from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Opcao, Pacientes, DadosPaciente, Refeicao
from django.contrib import messages
from django.contrib.messages import constants
from datetime import datetime
from nutrilab.settings import BASE_DIR

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
        email = email.lower(),
        telefone = telefone,
        nutri = request.user
      )
      paciente.save()
      messages.add_message(request, constants.SUCCESS, 'Paciente cadastrado com sucesso!')
    except:
      messages.add_message(request, constants.ERROR, 'Erro interno do sistema, tente novamente!')

    return redirect('/gerenciar_pacientes')
  
def alterar_paciente(request):
  id = request.POST.get('id')
  nome = request.POST.get('nome')
  sexo = request.POST.get('sexo')
  idade = request.POST.get('idade')
  email = request.POST.get('email').lower()
  telefone = request.POST.get('telefone')

  alterar_paciente = get_object_or_404(Pacientes, id=id)
  if not alterar_paciente.nutri == request.user:
    messages.add_message(request, constants.ERROR, 'Esse paciente não é seu!')
    return redirect('/gerenciar_pacientes')
  
  existem_pacientes = Pacientes.objects.filter(email=email)
  if existem_pacientes:
    for paciente in existem_pacientes:
      if paciente.id != alterar_paciente.id:
        messages.add_message(request, constants.ERROR, 'Já existe um paciente com esse email cadastrado no sistema!')
        return redirect('/gerenciar_pacientes')
  
  
  alterar_paciente.nome = nome
  alterar_paciente.sexo = sexo
  alterar_paciente.idade = idade
  alterar_paciente.email = email
  alterar_paciente.telefone = telefone
  alterar_paciente.save()
  
  messages.add_message(request, constants.SUCCESS, f'Dados de "{nome}" foram alterados com sucesso!')
  return redirect('/gerenciar_pacientes')     
  
def excluir_paciente(request):
  id = request.POST.get('id')
  paciente = Pacientes.objects.get(id=id)

  if not paciente.nutri == request.user:
    messages.add_message(request, constants.ERROR, 'Esse paciente não é seu!')
    return redirect('/gerenciar_pacientes')
  
  paciente.delete()
  messages.add_message(request, constants.SUCCESS, 'Paciente excluido com sucesso!')
  return redirect('/gerenciar_pacientes')

@login_required(login_url='/auth/logar')
def lista_dados_paciente(request):
  if request.method == 'GET':
    pacientes = Pacientes.objects.filter(nutri=request.user)
    return render(request, 'lista_dados_paciente.html', {'pacientes': pacientes})
  
@login_required(login_url='/auth/logar')
def dados_paciente(request, paciente_id):
  paciente = get_object_or_404(Pacientes, id=paciente_id)

  if not paciente.nutri == request.user:
    messages.add_message(request, constants.ERROR, 'Esse paciente não é seu!')
    return redirect('/lista_dados_paciente')
  
  if request.method == 'GET':
    dados = DadosPaciente.objects.filter(paciente=paciente)
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
  
@login_required(login_url='/auth/logar')
@csrf_exempt
def grafico_peso(request, paciente_id):
  paciente = Pacientes.objects.get(id=paciente_id)
  dados = DadosPaciente.objects.filter(paciente=paciente).order_by('data')

  pesos = [dado.peso for dado in dados] # Armazena na variável 'pesos' somente os dados de peso do paciente.
  labels = list(range(len(pesos)))  # Armazena na variável 'labels' uma lista numérica conforme a qnt de dados de 'pesos'.
  data = {'peso': pesos,
          'medicao': labels}
  
  return JsonResponse(data)

@login_required(login_url='/auth/logar')
def lista_plano_alimentar(request):
  pacientes = Pacientes.objects.filter(nutri=request.user)
  if request.method == 'GET':
    return render(request, 'lista_plano_alimentar.html', {'pacientes': pacientes})

@login_required(login_url='/auth/logar')
def plano_alimentar(request, paciente_id):
  paciente = get_object_or_404(Pacientes, id=paciente_id)

  if not paciente.nutri == request.user:
    messages.add_message(request, constants.ERROR, 'Esse paciente não é seu!')
    return redirect('/lista_plano_alimentar')
  
  if request.method == 'GET':
    refeicoes = Refeicao.objects.filter(paciente=paciente).order_by('horario')
    opcoes = Opcao.objects.all()
    
    return render(request, 'plano_alimentar.html', {'paciente': paciente, 'refeicoes': refeicoes, 'opcoes': opcoes})


def refeicao(request, paciente_id):
  paciente = get_object_or_404(Pacientes, id=paciente_id)
  if not paciente.nutri == request.user:
    messages.add_message(request, constants.ERROR, 'Esse paciente não é seu!')
    return redirect('/lista_plano_alimentar')
  
  if request.method == 'POST':
    titulo = request.POST.get('titulo')
    horario = request.POST.get('horario')
    carboidratos = request.POST.get('carboidratos')
    proteinas = request.POST.get('proteinas')
    gorduras = request.POST.get('gorduras')

    try:
      refeicao = Refeicao(
        paciente = paciente,
        titulo = titulo,
        horario = horario,
        carboidratos = carboidratos,
        proteinas = proteinas,
        gorduras = gorduras
      )
      refeicao.save()
      messages.add_message(request, constants.SUCCESS, 'Refeição cadastrada com sucesso!')
    except:
      messages.add_message(request, constants.ERROR, 'Algo deu errado, tente novamente ou entre em contato com a administração!')

    return redirect(f'/plano_alimentar/{paciente_id}')
  


def excluir_refeicao(request, refeicao_id):
  refeicao = Refeicao.objects.get(id=refeicao_id)

  if not refeicao.paciente.nutri == request.user:
    return redirect(f'/plano_alimentar/{refeicao.paciente_id}')
  refeicao.delete()

  return redirect(f'/plano_alimentar/{refeicao.paciente_id}')

  
def opcao(request, paciente_id):
  paciente = get_object_or_404(Pacientes, id=paciente_id)
  if not paciente.nutri == request.user:
    messages.add_message(request, constants.ERROR, 'Esse paciente não é seu!')
    return redirect('/lista_plano_alimentar')

  if request.method == 'POST':
    try:
      id_refeicao = request.POST.get('refeicao')
      imagem = request.FILES.get('imagem')
      descricao = request.POST.get('descricao')

      if not imagem:
        imagem = "default/Default.png"

      opcao = Opcao(
        refeicao_id = id_refeicao,
        imagem = imagem,
        descricao = descricao
      )
      opcao.save()
      messages.add_message(request, constants.SUCCESS, 'Opção de refeição cadastrada com sucesso!')
    except:
      messages.add_message(request, constants.ERROR, 'Algo deu errado, tente novamente ou entre em contato com a administração!')

    return redirect(f'/plano_alimentar/{paciente_id}')
  
def excluir_opcao(request, opcao_id):
  opcao = Opcao.objects.get(id=opcao_id)

  if not opcao.refeicao.paciente.nutri == request.user:
    return redirect(f'/plano_alimentar/{opcao.refeicao.paciente_id}')
  
  # Deleta a imagem(se não for a "Default.png").
  if not opcao.imagem == ("default/Default.png"):
    opcao.imagem.delete()
  opcao.delete()

  return redirect(f'/plano_alimentar/{opcao.refeicao.paciente_id}')
