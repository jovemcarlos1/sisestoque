from django.shortcuts import render, redirect
from .models import Saidas
from .forms import SaidaForm

# Create your views here.
def list_saida(request):
    saidas = Saidas.objects.all()
    template_name = 'list_saida.html'
    context = {
        'saidas': saidas
    }
    return render(request, template_name, context)

def new_saida(request):
    if request.method == 'POST':
        form = SaidaForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            if form.cleaned_data['quantidade'] > form.cleaned_data['produto'].quantidade:
                form.add_error('quantidade', 'Quantidade insuficiente em estoque.')
                return render(request, 'new_saida.html', {'form': form})
            if form.cleaned_data['quantidade'] <= 0:
                form.add_error('quantidade', 'Insira apenas valores positivos maiores que zero.')
                return render(request, 'new_saida.html', {'form': form})
            form.cleaned_data['produto'].quantidade = form.cleaned_data['produto'].quantidade - form.cleaned_data['quantidade']
            form.cleaned_data['produto'].save_base()
            form.save()
            return redirect('saida:list_saida')
    
    else:
        template_name = 'new_saida.html'
        context = {
            'form': SaidaForm()
        }
        return render(request, template_name, context)

def update_saida(request, pk):
    saida = Saidas.objects.get(pk=pk)
    quantidade = saida.quantidade
    template_name = 'update_saida.html'
    if request.method == 'POST':
        form = SaidaForm(request.POST,instance=saida)
        if form.is_valid():
            form.save(commit=False)
            if form.cleaned_data['quantidade'] > form.cleaned_data['produto'].quantidade + quantidade:
                form.add_error('quantidade', 'Quantidade insuficiente em estoque.')
                return render(request, template_name, {'form': form, 'pk': pk})
            if form.cleaned_data['quantidade'] <= 0:
                form.add_error('quantidade', 'Insira apenas valores positivos maiores que zero.')
                return render(request, template_name, {'form': form, 'pk': pk})
            form.cleaned_data['produto'].quantidade = form.cleaned_data['produto'].quantidade + quantidade - form.cleaned_data['quantidade']
            form.cleaned_data['produto'].save_base()
            form.save()
            return redirect('saida:list_saida')
    else:
        context = {
            'form': SaidaForm(instance=saida),
            'pk': pk
        }
        return render(request, template_name, context)
    

def delete_saida(request, pk): 
    saida = Saidas.objects.get(pk=pk)     
    saida.produto.quantidade = saida.produto.quantidade + saida.quantidade
    saida.produto.save()
    saida.delete()
    return redirect('saida:list_saida')