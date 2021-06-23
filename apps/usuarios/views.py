from django.contrib.auth.models import User
from django.core import paginator
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib import auth,messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from receitas.models import Receita

def cadastro(request):
    """ Cadastra uma nova pessoa no sistema"""
    if request.method == "POST":
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['password']
        senha2 = request.POST['password2']
        if not nome.strip():
            print('Nome não pode ficar em branco')
            return redirect('cadastro')
        if not email.strip():
            print('E-maiil não pode ficar em branco')
            return redirect('cadastro')
        if senha != senha2:
            messages.error(request,'As SEnhas não são iguais')
            print('Senhas devem ser iguais')
            return redirect('cadastro')
        if auth.models.User.objects.filter(email=email).exists() or auth.models.User.objects.filter(username=nome).exists() :
            print('usuadio já cadastrado!')
            return redirect('cadastro')
        user = auth.models.User.objects.create_user(username = nome, email = email,password=senha)
        user.save()
        print("Ususario criado com sucesso!")
        messages.success(request,'Ususario criado com sucesso!')
        return redirect('login')
    else:
        return render(request,'usuarios/cadastro.html')


def login(request):
    if request.method == "POST":
        senha = request.POST['senha']
        email = request.POST['email']
        if email=="" or senha=='':
            print('E-maiil e senha não podem ficar em branco')
            return redirect('login')
        if auth.models.User.objects.filter(email=email).exists():
            nome = auth.models.User.objects.filter(email=email).values_list('username',flat=True)[0]
            print(nome)
            user = auth.authenticate(request, username=nome, password=senha)
            if user is not None:
                auth.login(request,user)
            print("Login realizado com sucesso!")
            return redirect('dashboard')
    return render(request,'usuarios/login.html')


def logout(request):
    auth.logout(request)
    return redirect('index')


def dashboard(request):
    if request.user.is_authenticated:
        receitas = Receita.objects.order_by('-data_publicacao').filter(pessoa =  request.user.id)
        paginator = Paginator(receitas,3)
        page = request.GET.get('page')
        receitas_da_pagina = paginator.get_page(page)
        dados ={
        'receitas':receitas_da_pagina
        }
        return render(request,'usuarios/dashboard.html', dados)
    else:
        return redirect('index')


