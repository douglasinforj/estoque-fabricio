from django.contrib import admin
from .models import Produto, Pedido, ItemPedido, Fornecedor, Compra, ItemCompra

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'unidade', 'preco', 'estoque_atual', 'validade')
    search_fields = ('nome',)


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'data_pedido', 'solicitante', 'observacoes')


@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'produto', 'quantidade', 'preco_unitario', 'subtotal')


@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'contato', 'email')


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'fornecedor', 'data_compra', 'observacoes')


@admin.register(ItemCompra)
class ItemCompraAdmin(admin.ModelAdmin):
    list_display = ('compra', 'produto', 'quantidade', 'preco_unitario', 'subtotal')
