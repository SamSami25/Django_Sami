from django.contrib import admin
from .models import Pregunta, Opcion, TipBelleza, TipSeguridad, Afirmacion, Envio

class OpcionInline(admin.TabularInline):
    model = Opcion
    extra = 1

@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ("texto", "categoria", "audiencia", "activo")
    list_filter = ("categoria", "audiencia", "activo")
    search_fields = ("texto",)
    inlines = [OpcionInline]

@admin.register(TipBelleza)
class TipBellezaAdmin(admin.ModelAdmin):
    list_display = ("texto", "genero")
    list_filter = ("genero",)
    search_fields = ("texto",)

@admin.register(TipSeguridad)
class TipSeguridadAdmin(admin.ModelAdmin):
    list_display = ("texto", "genero")
    list_filter = ("genero",)
    search_fields = ("texto",)

@admin.register(Afirmacion)
class AfirmacionAdmin(admin.ModelAdmin):
    list_display = ("texto", "genero")
    list_filter = ("genero",)
    search_fields = ("texto",)

@admin.register(Envio)
class EnvioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "genero", "categoria_top", "creado")
    list_filter = ("genero", "categoria_top", "creado")
    search_fields = ("nombre",)
