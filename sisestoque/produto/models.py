from django.db import models

# Create your models here.
class Cores(models.Model):
    cor = models.CharField('Cor', max_length=200)
    
    def __str__(self):
        return self.cor
    
class Produtos(models.Model):
    produto = models.CharField('Produto', max_length=200)
    cor = models.ForeignKey(Cores, on_delete=models.PROTECT, verbose_name='Cor')
    descricao = models.TextField('Descriçao', blank=True)
    quantidade = models.IntegerField('Quantidade', default=0)
    preco = models.DecimalField('Preço', decimal_places=2, max_digits=8, default=0)
    criado = models.DateTimeField('Criado em', auto_now_add=True)
    modificado = models.DateField('Modificado em', auto_now=True)

    def __str__(self):
        return self.produto

    def precoQuantidade(self):
        return self.preco * self.quantidade
    
    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['-produto']