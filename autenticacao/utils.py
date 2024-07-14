import re
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def user_is_valid(request, usuario, email):
  if not usuario:
      messages.add_message(request, constants.ERROR, 'O campo "Nome de usuário" não pode ser vazio!')
      return False
    
  if not email:
    messages.add_message(request, constants.ERROR, 'O campo "E-mail" não pode ser vazio!')
    return False
  
  usuario_existe = User.objects.filter(username=usuario)

  if usuario_existe:
      messages.add_message(request, constants.ERROR, 'Usuário já cadastrado no sistema')
      return False
  
  return True

def password_is_valid(request, password, confirm_password):
  if len(password) < 6:
    messages.add_message(request, constants.ERROR, 'Sua senha deve conter 6 ou mais caractertes')
    return False

  if not password == confirm_password:
    messages.add_message(request, constants.ERROR, 'As senhas não coincidem!')
    return False
  
  if not re.search('[A-Z]', password):
    messages.add_message(request, constants.ERROR, 'Sua senha não contem letras maiúsculas')
    return False

  if not re.search('[a-z]', password):
    messages.add_message(request, constants.ERROR, 'Sua senha não contem letras minúsculas')
    return False

  if not re.search('[1-9]', password):
    messages.add_message(request, constants.ERROR, 'Sua senha não contém números')
    return False

  return True

def email_html(path_template: str, assunto: str, para: list, **kwargs) -> dict:
    
    html_content = render_to_string(path_template, kwargs)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(assunto, text_content, settings.EMAIL_HOST_USER, para)

    email.attach_alternative(html_content, "text/html")
    email.send()
    return {'status': 1}
