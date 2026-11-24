from django.contrib import admin

from accesos.models import Vivienda, Residente, Visitante, RegistroAcceso


@admin.register(Vivienda)
class ViviendaAdmin(admin.ModelAdmin):
    list_display = ('manzana', 'numero', 'tipo', 'fecha_registro')
    list_filter = ('tipo', 'manzana')
    search_fields = ('manzana', 'numero')


@admin.register(Residente)
class ResidenteAdmin(admin.ModelAdmin):
    list_display = ('apellidos', 'nombres', 'cedula', 'telefono', 'email')
    list_filter = ('viviendas__manzana',)
    search_fields = ('apellidos', 'nombres', 'cedula')
    filter_horizontal = ('viviendas',)  # selector cómodo para el ManyToMany


@admin.register(Visitante)
class VisitanteAdmin(admin.ModelAdmin):
    list_display = ('apellidos', 'nombres', 'cedula', 'placa', 'creado_por')
    list_filter = ('creado_por',)
    search_fields = ('apellidos', 'nombres', 'cedula', 'placa')


@admin.register(RegistroAcceso)
class RegistroAccesoAdmin(admin.ModelAdmin):
    list_display = ('visitante', 'vivienda', 'motivo', 'estado', 'fecha_ingreso', 'creado_por')
    list_filter = ('estado', 'motivo', 'fecha_ingreso')
    search_fields = ('visitante__apellidos', 'visitante__cedula', 'vivienda__numero')