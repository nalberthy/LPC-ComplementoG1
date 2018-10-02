from django.shortcuts import render
from .models import *

# Create your views here.
def orcamentos_lista(request):
    # logica
    orcamentos = Orcamento.objects.all()
    return render(request, 'mp_orcamento/orcamentos.html', {'orcamentos': orcamentos})

def orcamentos_estatisticas(request):
    maior_custo = 0
    menor_custo = 999999999999
    orcamento_maior_custo = None
    orcamento_menor_custo = None
    orcamentos = Orcamento.objects.all()
    somatorio_custo_total = 0
    for orcamento in orcamentos:
        somatorio = 0
        for peca in Peca.objects.filter(orcamento=orcamento):
            somatorio += peca.custo_de_producao_ajustado()
        orcamento.custo_total = somatorio * 1.25
        somatorio_custo_total += orcamento.custo_total
        if orcamento.custo_total >= maior_custo:
            orcamento_maior_custo = orcamento
            maior_custo = orcamento.custo_total
        if orcamento.custo_total <= menor_custo:
            orcamento_menor_custo = orcamento
            menor_custo = orcamento.custo_total
    quantidade = Orcamento.objects.count() 
    media_custo_total = somatorio_custo_total / quantidade
    return render(request, 'mp_orcamento/estatisticas.html', 
        {'quantidade': quantidade, 
        'orcamento_maior_custo': orcamento_maior_custo,
        'orcamento_menor_custo': orcamento_menor_custo,
        'media_custo_total': media_custo_total
        })

def orcamento_cliente(request, codigo):         
    cliente = Cliente.objects.get(id=codigo)
    orcamento = Orcamento.objects.filter(cliente=cliente)    
    return render(request, 'mp_orcamento/orcamento_idcliente.html', {'cliente': cliente, 'orcamento':orcamento})



def cliente_estatisticas(request):
    clientes = Cliente.objects.count()
    orcamentos = Cliente.objects.all()
    maior_custo = 0
    menor_custo = 999999999999
    orcamento_maior_custo = None
    orcamento_menor_custo = None
    somatorio_custo_total = 0

    for orcamento in orcamentos:
        somatorio = 0
        for orcamento in Orcamento.objects.filter(cliente=orcamento):
            somatorio += orcamento.custo_total()
        orcamento.custo_total = somatorio
        if orcamento.custo_total >= maior_custo:
            orcamento_maior_custo = orcamento
            maior_custo = orcamento.custo_total
        if orcamento.custo_total <= menor_custo:
            orcamento_menor_custo = orcamento
            menor_custo = orcamento.custo_total
    quantidade = Orcamento.objects.count() 

    return render(request, 'mp_orcamento/cliente_estatisticas.html', {'clientes': clientes, 
    'orcamento_maior_custo':orcamento_maior_custo, 
    'orcamento_menor_custo':orcamento_menor_custo})
    
