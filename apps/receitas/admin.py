from django.contrib import admin
from .models import Receita


class ListandoReceitas(admin.ModelAdmin):
   
    dados = ('id', 'nome_receita','categoria','publicada')
    list_display = dados
    list_display_links =dados[:-1]
    search_fields = (dados[1],)
    list_filter = (dados[2],)
    list_editable= (dados[-1],)
    list_per_page =10
admin.site.register(Receita, ListandoReceitas)