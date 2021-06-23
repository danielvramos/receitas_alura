from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from receitas.models import Receita


def index(request):
    receitas = Receita.objects.order_by('-data_publicacao').filter(publicada=True)
    paginator = Paginator(receitas,3)
    page = request.GET.get('page')
    receitas_por_pagina = paginator.get_page(page)
    dados ={
        'receitas':receitas_por_pagina
    }
    return render(request,'receitas/index.html',dados)
 

def receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    dictReceita = {'receita':receita}
    return render(request,'receitas/receita.html',dictReceita)


def cria_receita(request):
    if request.method == 'POST':
        nome_receita = request.POST['nome_receita']
        ingredientes = request.POST['ingredientes']
        modo_de_preparo = request.POST['modo_preparo']
        tempo_de_preparo = request.POST['tempo_preparo']
        redimento = request.POST['rendimento']
        categoria = request.POST['categoria']
        foto_receita = request.FILES['foto_receita']
        receita =Receita.objects.create(
            pessoa = get_object_or_404(User, pk=request.user.id),
            nome_receita = nome_receita,
            ingredientes = ingredientes,
            modo_de_preparo = modo_de_preparo,
            tempo_de_preparo = tempo_de_preparo,
            redimento = redimento,
            categoria = categoria,
            foto_receita = foto_receita
        )
        receita.save()
        return redirect('dashboard')
    else:
        return render(request,'receitas/cria_receita.html')


def deleta_receita(request,receita_id):

    receita = get_object_or_404(Receita, pk = receita_id)
    receita.delete()
    return redirect('dashboard')


def atualiza_receita(request):
    if request.method == 'POST':
        r = Receita.objects.get(pk=request.POST['receita_id'])
        r.nome_receita = request.POST['nome_receita']
        r.ingredientes = request.POST['ingredientes']
        r.modo_de_preparo = request.POST['modo_preparo']
        r.tempo_de_preparo = request.POST['tempo_preparo']
        r.redimento = request.POST['rendimento']
        r.categoria = request.POST['categoria']
        if 'foto_receita' in request.FILES:
            r.foto_receita = request.FILES['foto_receita']
        print(r.foto_receita)
        r.save()
    return redirect('dashboard')
   

def edita_receita(request,receita_id):
    receita = get_object_or_404(Receita, pk = receita_id)
    dados = {'receita':receita}
    return render(request,'receitas/edita_receita.html',dados)
        