from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

MODELOS = ['vivienda', 'residente', 'visitante', 'registroacceso']


class Command(BaseCommand):
    help = 'Crea los grupos administradores y consultores con sus permisos'

    def handle(self, *args, **options):
        # administradores: add, change, delete y view de las cuatro entidades
        administradores, _ = Group.objects.get_or_create(name='administradores')
        permisos_admin = Permission.objects.filter(
            content_type__app_label='accesos',
            content_type__model__in=MODELOS,
        )
        administradores.permissions.set(permisos_admin)

        # consultores: ver todo + crear/editar/eliminar registros de acceso
        # (editar y eliminar quedan limitados por la regla de propiedad en las vistas)
        consultores, _ = Group.objects.get_or_create(name='consultores')
        codigos = [f'view_{modelo}' for modelo in MODELOS] + [
            'add_registroacceso',
            'change_registroacceso',
            'delete_registroacceso',
        ]
        permisos_consultor = Permission.objects.filter(
            content_type__app_label='accesos',
            codename__in=codigos,
        )
        consultores.permissions.set(permisos_consultor)

        self.stdout.write(self.style.SUCCESS('Grupos creados: administradores y consultores'))