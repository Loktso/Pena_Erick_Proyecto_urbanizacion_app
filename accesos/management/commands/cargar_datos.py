from datetime import timedelta

from django.contrib.auth.models import Group, User
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils import timezone

from accesos.models import Vivienda, Residente, Visitante, RegistroAcceso


class Command(BaseCommand):
    help = 'Crea grupos, usuarios y datos de prueba (se puede ejecutar varias veces sin duplicar)'

    def crear_usuario(self, username, password, email, grupo=None, superusuario=False):
        usuario, creado = User.objects.get_or_create(
            username=username,
            defaults={'email': email, 'is_staff': superusuario, 'is_superuser': superusuario},
        )
        if creado:
            usuario.set_password(password)
            usuario.save()
        if grupo:
            usuario.groups.add(Group.objects.get(name=grupo))
        return usuario

    def handle(self, *args, **options):
        # 1. Grupos y permisos
        call_command('crear_grupos')

        # 2. Usuarios de prueba: un superusuario y usuarios de cada grupo
        admin = self.crear_usuario('admin', 'Admin12345', 'admin@urbanizacion.ec', superusuario=True)
        self.crear_usuario(
            'administrador1', 'Admin2026!', 'administrador1@urbanizacion.ec', grupo='administradores'
        )
        consultor1 = self.crear_usuario(
            'consultor1', 'Consul2026!', 'consultor1@urbanizacion.ec', grupo='consultores'
        )
        self.crear_usuario(
            'consultor2', 'Consul2026!', 'consultor2@urbanizacion.ec', grupo='consultores'
        )

        # 3. Viviendas (6)
        datos_viviendas = [
            ('A', '1', 'CASA'), ('A', '2', 'CASA'), ('B', '1', 'CASA'),
            ('B', '2', 'DEPTO'), ('C', '1', 'DEPTO'), ('C', '2', 'CASA'),
        ]
        viviendas = []
        for manzana, numero, tipo in datos_viviendas:
            vivienda, _ = Vivienda.objects.get_or_create(
                manzana=manzana, numero=numero, defaults={'tipo': tipo}
            )
            viviendas.append(vivienda)

        # 4. Residentes (6)
        datos_residentes = [
            ('Carlos', 'Mena', '1700000001'), ('Lucia', 'Paredes', '1700000002'),
            ('Jorge', 'Salazar', '1700000003'), ('Ana', 'Torres', '1700000004'),
            ('Pedro', 'Vega', '1700000005'), ('Marta', 'Rojas', '1700000006'),
        ]
        residentes = []
        for i, (nombres, apellidos, cedula) in enumerate(datos_residentes):
            residente, nuevo = Residente.objects.get_or_create(
                cedula=cedula,
                defaults={
                    'nombres': nombres,
                    'apellidos': apellidos,
                    'telefono': f'09900000{i:02d}',
                    'email': f'{nombres.lower()}@correo.com',
                },
            )
            if nuevo:
                residente.viviendas.add(viviendas[i])
                if i == 0:
                    residente.viviendas.add(viviendas[1])  # un residente con dos viviendas
            residentes.append(residente)

        # 5. Visitantes (6)
        datos_visitantes = [
            ('Diego', 'Cevallos', '1800000001', 'PBA1234'),
            ('Sofia', 'Andrade', '1800000002', ''),
            ('Mateo', 'Herrera', '1800000003', 'PCD5678'),
            ('Valeria', 'Lopez', '1800000004', ''),
            ('Andres', 'Ruiz', '1800000005', 'PEF9012'),
            ('Camila', 'Duran', '1800000006', ''),
        ]
        visitantes = []
        for nombres, apellidos, cedula, placa in datos_visitantes:
            visitante, _ = Visitante.objects.get_or_create(
                cedula=cedula,
                defaults={'nombres': nombres, 'apellidos': apellidos, 'placa': placa, 'creado_por': admin},
            )
            visitantes.append(visitante)

        # 6. Registros de acceso (6, solo si la tabla está vacía)
        #    Los pares los crea admin y los impares consultor1, para probar la regla de propiedad
        if not RegistroAcceso.objects.exists():
            motivos = ['VISITA', 'DELIVERY', 'SERVICIO', 'VISITA', 'OTRO', 'VISITA']
            estados = ['FINALIZADO', 'AUTORIZADO', 'PENDIENTE', 'RECHAZADO', 'FINALIZADO', 'AUTORIZADO']
            ahora = timezone.now()
            for i in range(6):
                ingreso = ahora - timedelta(hours=i * 5)
                RegistroAcceso.objects.create(
                    visitante=visitantes[i],
                    vivienda=viviendas[i],
                    autorizado_por=residentes[i],
                    motivo=motivos[i],
                    estado=estados[i],
                    fecha_ingreso=ingreso,
                    fecha_salida=ingreso + timedelta(hours=1) if estados[i] == 'FINALIZADO' else None,
                    creado_por=admin if i % 2 == 0 else consultor1,
                )

        self.stdout.write(self.style.SUCCESS('Grupos, usuarios y datos de prueba cargados'))