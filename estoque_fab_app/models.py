from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    unidade = models.CharField(
        max_length=10,
        choices=[('unidade', 'Unidade'), ('kg', 'Kg')],
        default='unidade'
    )
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço unitário")
    estoque_atual = models.FloatField(default=0, verbose_name="Quantidade em Estoque")
    validade = models.DateField(null=True, blank=True, verbose_name="Data de Validade")

    def __str__(self):
        return self.nome
    
#----------------------Pedidos--------------------

class Pedido(models.Model):
    data_pedido = models.DateTimeField(auto_now_add=True)
    solicitante = models.CharField(max_length=100, verbose_name="Cliente/Departamento")
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.solicitante}"


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.FloatField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        # Calcula o subtotal e atualiza o estoque do produto
        self.subtotal = self.quantidade * self.preco_unitario
        super().save(*args, **kwargs)

        # Atualiza o estoque
        self.produto.estoque_atual -= self.quantidade
        if self.produto.estoque_atual < 0:
            raise ValueError("Estoque insuficiente para o produto.")
        self.produto.save()


#--------------Compras-------------------------------

class Fornecedor(models.Model):
    nome = models.CharField(max_length=100)
    contato = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.nome


class Compra(models.Model):
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
    data_compra = models.DateTimeField(auto_now_add=True)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Compra #{self.id} - {self.fornecedor.nome}"


class ItemCompra(models.Model):
    compra = models.ForeignKey(Compra, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.FloatField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        # Calcula o subtotal e atualiza o estoque do produto
        self.subtotal = self.quantidade * self.preco_unitario
        super().save(*args, **kwargs)

        # Atualiza o estoque
        self.produto.estoque_atual += self.quantidade
        self.produto.save()
