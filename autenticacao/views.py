from django.shortcuts import render, redirect
from django.http import HttpResponse
from .utils import password_is_valid
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages, auth

def cadastro(request):
  if request.method == 'GET':
    if request.user.is_authenticated:
      return HttpResponse('Login feito com sucesso!')
    return render(request, 'cadastro.html')
  elif request.method == 'POST':
    usuario = request.POST.get('usuario')
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    confirmar_senha = request.POST.get('confirmar_senha')

    if not usuario:
      messages.add_message(request, constants.ERROR, 'O campo "Nome de usuário" não pode ser vazio!')
      return redirect('/auth/cadastro')
    
    if not email:
      messages.add_message(request, constants.ERROR, 'O campo "E-mail" não pode ser vazio!')
      return redirect('/auth/cadastro')
      
    if not password_is_valid(request, senha, confirmar_senha):  # função do utils.py
      return redirect('/auth/cadastro')

    try:
      user = User.objects.create_user(
        username=usuario,
        email=email,
        password=senha,
        is_active=False
      )
      messages.add_message(request, constants.SUCCESS, 'Cadastro realizado com sucesso, valide seu email para fazer o login!')
      return redirect('/auth/logar')
    
    except:
      messages.add_message(request, constants.ERROR, 'Não foi possível realizar o cadastro, erro interno do sistema!')
      return redirect('/auth/cadastro')

def logar(request):
  if request.method == 'GET':
    if request.user.is_authenticated:
      return HttpResponse('Login feito com sucesso!')
    return render(request, 'login.html')
  elif request.method == 'POST':
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    usuario_existe = auth.authenticate(username=usuario, password=senha)

    # if not usuario_existe.is_active:
    #   messages.add_message(request, constants.WARNING, 'Valide seu email!')
    #   return redirect('/auth/logar')

    if not usuario_existe:
      messages.add_message(request, constants.ERROR, 'Usuário ou senha inválido...tente novamente ou faça o cadastro!')
      return redirect('/auth/logar')
    
    auth.login(request, usuario_existe)
    return HttpResponse('Login feito com sucesso!')
  
def sair(request):
  auth.logout(request)
  return redirect('/auth/logar')
    
