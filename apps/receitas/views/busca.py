from django.shortcuts import render
from receitas.models import Receita


def busca (request):

    receitasEncontradodas = Receita.objects.order_by('-data_publicacao').filter(publicada=True)
    
    if 'buscar' in request.GET:
        nome_a_buscar=request.GET['buscar']
        receitasEncontradodas = receitasEncontradodas.filter(nome_receita__icontains=nome_a_buscar)
    dados ={'receitas':receitasEncontradodas}
    return render(request, 'receitas/buscar.html',dados)
