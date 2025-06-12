from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import Entradas
from .forms import EntradaForm

def list_entrada(request):
    entradas = Entradas.objects.all()
    template_name = 'list_entrada.html'
    context = {
        'entradas': entradas
    }
    return render(request, template_name, context)


def new_entrada(request):
    if request.method == 'POST':
        form = EntradaForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            if form.cleaned_data['quantidade'] <= 0:
                form.add_error('quantidade', 'Insira apenas valores positivos maiores que zero.')
                return render(request, 'new_entrada.html', {'form': form})
            form.cleaned_data['produto'].quantidade = form.cleaned_data['produto'].quantidade + form.cleaned_data['quantidade']
            form.cleaned_data['produto'].save_base()
            form.save()
            return redirect('entrada:list_entrada')
    
    else:
        template_name = 'new_entrada.html'
        context = {
            'form': EntradaForm()
        }
        return render(request, template_name, context)

def update_entrada(request, pk):
    entrada = Entradas.objects.get(pk=pk)
    quantidade = entrada.quantidade
    template_name = 'update_entrada.html'

    if request.method == 'POST':
        form = EntradaForm(request.POST,instance=entrada)
        if form.is_valid():
            form.save(commit=False)
            if form.cleaned_data['produto'].quantidade - quantidade + form.cleaned_data['quantidade'] <= 0:
                form.add_error('quantidade', 'Quantidade insuficiente em estoque.')
                return render(request, template_name, {'form': form, 'pk': pk})
            if form.cleaned_data['quantidade'] <= 0:
                form.add_error('quantidade', 'Insira apenas valores positivos maiores que zero.')
                return render(request,template_name, {'form': form, 'pk': pk})
            form.cleaned_data['produto'].quantidade = form.cleaned_data['produto'].quantidade - quantidade + form.cleaned_data['quantidade']
            form.cleaned_data['produto'].save_base()
            form.save()
            return redirect('entrada:list_entrada')
    else:
        context = {
            'form': EntradaForm(instance=entrada),
            'pk': pk
        }
        return render(request, template_name, context)
        
def delete_entrada(request, pk): 
    entrada = Entradas.objects.get(pk=pk)     
    if entrada.produto.quantidade - entrada.quantidade <= 0:
        context = {
            'error': "Não foi possivel excluir a entrada, pois a entrada é menor que a saída",
        }
        return render(request, 'error_entrada.html', context)
    entrada.produto.quantidade = entrada.produto.quantidade - entrada.quantidade
    entrada.produto.save()
    entrada.delete()
    return redirect('entrada:list_entrada')
            