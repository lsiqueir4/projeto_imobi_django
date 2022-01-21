from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required 
from .models import Imovei, Cidade, Visitas #importando a classe imovei do models
# Create your views here.

#O decorator garante que o usuario precisa estar logado, 
# senao redireciona para a tela de login
@login_required(login_url='/auth/logar') 
def home(request):
    imoveis = Imovei.objects.all() #declarando todos os cadastros da tabela na variavel
    cidades = Cidade.objects.all()
    preco_minimo = request.GET.get('preco_minimo') #variavel do filtro q o user aplicou
    preco_maximo = request.GET.get('preco_maximo') #variavel do filtro q o user aplicou
    cidade = request.GET.get('cidade')
    tipo = request.GET.getlist('tipo')
    if preco_minimo or preco_maximo or cidade or tipo: #if para aplicar o filtro
        if not preco_minimo:
            preco_minimo = 0
        if not preco_maximo:
            preco_maximo = 999999999
        if not tipo:
            tipo = ['A', 'C']
        imoveis = Imovei.objects.filter(valor__gte=preco_minimo)\
        .filter(valor__lte=preco_maximo)\
        .filter(tipo_imovel__in=tipo).filter(cidade=cidade)
    else:
        imoveis = Imovei.objects.all()
    return render(request, 'home.html', {'imoveis': imoveis, 'cidades': cidades})

def imovel(request, id):
    imovel = get_object_or_404(Imovei, id=id) #tras o imovel pelo ID, senao retorna tela de erro 404
    sugestoes = Imovei.objects.filter(cidade=imovel.cidade).exclude(id=id)[:2]
    return render(request, 'imovel.html', {'imovel': imovel, 'sugestoes': sugestoes, 'id': id})

def agendar_visitas(request):
    usuario = request.user #pega o user q faz o agendamento
    dia = request.POST.get('dia')
    horario = request.POST.get('horario')
    id_imovel = request.POST.get('id_imovel')

    visitas = Visitas(
        imovel_id=id_imovel,
        usuario=usuario,
        dia=dia,
        horario=horario
    )

    visitas.save()
    return redirect('/agendamentos')

def agendamentos(request):
    visitas = Visitas.objects.filter(usuario=request.user)
    return render(request, "agendamentos.html", {'visitas': visitas})

def cancelar_agendamento(request, id):
    visitas = get_object_or_404(Visitas, id=id)
    visitas.status = "C"
    visitas.save()
    return redirect('/agendamentos')