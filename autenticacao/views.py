from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .utils import password_is_valid, user_is_valid, email_html
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages, auth
import os
from django.conf import settings
from .models import Ativacao
from hashlib import sha256

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

    if not user_is_valid(request, usuario, email):  # função do utils.py
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
      
      token = sha256(f'{usuario}{email}'.encode()).hexdigest()
      ativacao = Ativacao(token=token, user=user)
      ativacao.save()
      
      path_template = os.path.join(settings.BASE_DIR, 'autenticacao/templates/emails/cadastro_confirmado.html')
      email_html(path_template, 'Cadastro confirmado', [email,], username=usuario, link_ativacao=f"127.0.0.1:8000/auth/ativar_conta/{token}")

      messages.add_message(request, constants.SUCCESS, 'Cadastro realizado com sucesso, valide seu email para fazer o login!')
      return redirect('/auth/logar')
    
    except:
      messages.add_message(request, constants.ERROR, 'Não foi possível realizar o cadastro, erro interno do sistema!')
      return redirect('/auth/cadastro')

def ativar_conta(request, token):
    token = get_object_or_404(Ativacao, token=token)
    if token.ativo:
        messages.add_message(request, constants.WARNING, 'Sua conta já está ativada, faça o login para entrar!')
        return redirect('/auth/logar')
    
    user = User.objects.get(username=token.user.username)
    user.is_active = True
    user.save()
    
    token.ativo = True
    token.save()
    
    messages.add_message(request, constants.SUCCESS, 'Sua conta foi ativada com sucesso, você já pode fazer o login para entrar!')
    return redirect('/auth/logar')

def logar(request):
  if request.method == 'GET':
    if request.user.is_authenticated:
      return redirect('/pacientes')
    return render(request, 'login.html')
  elif request.method == 'POST':
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    usuario_existe = auth.authenticate(username=usuario, password=senha)

    try:
      usuario_validacao = User.objects.get(username=usuario)
      if usuario_validacao.is_active == False:
        messages.add_message(request, constants.WARNING, 'Esse usuário ainda não foi validado, verifique seu email e faça a validação para entrar!')
        return redirect('/auth/logar')
    except:
      pass

    if not usuario_existe:
      messages.add_message(request, constants.ERROR, 'Usuário ou senha inválido...tente novamente ou faça o cadastro!')
      return redirect('/auth/logar')    

    auth.login(request, usuario_existe)
    return redirect('/pacientes')
  
def sair(request):
  auth.logout(request)
  return redirect('/auth/logar')
    
