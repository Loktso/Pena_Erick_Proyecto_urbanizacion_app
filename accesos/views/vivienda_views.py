from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, render

from accesos.models import Vivienda


@login_required
@permission_required('accesos.view_vivienda', raise_exception=True)
def vivienda_list(request):
    viviendas = Vivienda.objects.all()
    return render(request, 'accesos/viviendas/lista.html', {'viviendas': viviendas})


@login_required
@permission_required('accesos.view_vivienda', raise_exception=True)
def vivienda_detail(request, pk):
    vivienda = get_object_or_404(Vivienda, pk=pk)
    return render(request, 'accesos/viviendas/detalle.html', {'vivienda': vivienda})