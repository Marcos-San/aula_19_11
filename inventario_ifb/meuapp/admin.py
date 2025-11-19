from django.contrib import admin
from .models import Setor, Sala, Inventario, Conferencia, ItemConferencia

@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ['sigla', 'nome', 'campus']
    search_fields = ['nome', 'sigla', 'campus']


@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = ['numero', 'setor']
    list_filter = ['setor']
    search_fields = ['numero']


@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descricao', 'tipo', 'status', 'sala_atual']
    list_filter = ['tipo', 'status']
    search_fields = ['codigo', 'descricao', 'numero_serie']


class ItemConferenciaInline(admin.TabularInline):
    model = ItemConferencia
    extra = 0


@admin.register(Conferencia)
class ConferenciaAdmin(admin.ModelAdmin):
    list_display = ['sala', 'ano', 'usuario', 'data_inicio', 'finalizada']
    list_filter = ['finalizada', 'ano', 'sala']
    search_fields = ['sala__numero', 'usuario__username']
    inlines = [ItemConferenciaInline]


@admin.register(ItemConferencia)
class ItemConferenciaAdmin(admin.ModelAdmin):
    list_display = ['conferencia', 'inventario', 'status_conferido', 'data_conferencia']
    list_filter = ['status_conferido', 'data_conferencia']
    search_fields = ['inventario__codigo', 'observacao']