from django import http
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.messages import constants
# Create your views here.

def cadastro(request):
    if request.method =='GET':
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'cadastro.html')
    elif request.method =='POST':
        username = request.POST.get('username') #capturando o valor do campo e armazenando em uma variavel
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        user = User.objects.filter(username = username)#user vai puxar o usuario do banco de dados

        if len(username.strip()) == 0 or len(email.strip()) == 0 or len(senha.strip()) == 0: # .strip() retira os espaços dos campos
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
            return redirect('/auth/cadastro')
        
        if user.exists(): #se o usuario existe no banco, redireciona pra tela de cadastro
            messages.add_message(request, constants.ERROR, 'Já existe um usuário com esse nome cadastrado')
            return redirect('/auth/cadastro')
        
        try: 
            user= User.objects.create_user(username=username, email=email, password=senha)
            user.save() #salva o novo usuario na tabela do db
            messages.add_message(request, constants.SUCCESS, 'Cadastro realizado com sucesso')
            return redirect('/auth/logar')
        except NameError:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
            return redirect('/auth/cadastro')
            print(NameError)

        
    
def logar(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'logar.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        usuario = auth.authenticate(username=username, password=senha)

        if not usuario:
            messages.add_message(request, constants.ERROR, 'Usuário ou senha invalidos')
            return redirect('/auth/logar')
        else:
            auth.login(request, usuario)
            return redirect('/')

def sair(request):
    auth.logout(request)
    return redirect('/auth/logar')
