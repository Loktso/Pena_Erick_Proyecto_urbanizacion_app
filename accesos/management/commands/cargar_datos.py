from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from accesos.models import Vivienda, Residente, Visitante, RegistroAcceso


class Command(BaseCommand):
    help = 'Carga datos de prueba (se puede ejecutar varias veces sin duplicar)'

    def handle(self, *args, **options):
        # Usuario base: lo necesitan los campos creado_por
        admin, creado = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@urbanizacion.ec', 'is_staff': True, 'is_superuser': True},
        )
        if creado:
            admin.set_password('Admin12345')
            admin.save()

        # 6 viviendas
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

        # 6 residentes
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

        # 6 visitantes
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

        # 6 registros de acceso (solo si la tabla está vacía)
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
                    creado_por=admin,
                )

        self.stdout.write(self.style.SUCCESS('Datos de prueba cargados'))