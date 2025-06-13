from django.shortcuts import render, redirect
from .models import Produtos
from .forms import ProdutoForm

def list_produto(request): 
    produtos = Produtos.objects.all() 
    template_name = 'list_produtos.html' 
    context = { 'produtos': produtos, } 
    return render(request, template_name, context)

def new_produto(request): 
    if request.method == 'POST': 
        form = ProdutoForm(request.POST) 
        if form.is_valid():
            if form.cleaned_data['preco'] <= 0:
                form.add_error('preco', 'Insira apenas valores positivos maiores que zero.')
                return render(request, 'new_produto.html', {'form': form}) 
            form.save() 
            return redirect('index') 
    else:     
        template_name = 'new_produto.html'
        context = {'form': ProdutoForm(),}
        return render(request, template_name, context)
        

def update_produto(request, pk): 
    produto = Produtos.objects.get(pk=pk) 
    if request.method == 'POST': 
        form = ProdutoForm(request.POST, instance=produto) 
        if form.is_valid():
            if form.cleaned_data['preco'] <= 0:
                form.add_error('preco', 'Insira apenas valores positivos maiores que zero.')
                return render(request, 'update_produto.html', {'form': form})
            form.save() 
            return redirect('index') 
    else:      
        template_name = 'update_produto.html'
        context = {'form': ProdutoForm(instance=produto),'pk': pk}
        return render(request, template_name, context)
        
def delete_produto(request, pk): 
    produto = Produtos.objects.get(pk=pk) 
    produto.delete() 
    return redirect('index')
