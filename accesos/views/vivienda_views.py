from django.shortcuts import get_object_or_404, render

from accesos.models import Vivienda


def vivienda_list(request):
    viviendas = Vivienda.objects.all()
    return render(request, 'accesos/viviendas/lista.html', {'viviendas': viviendas})


def vivienda_detail(request, pk):
    vivienda = get_object_or_404(Vivienda, pk=pk)
    return render(request, 'accesos/viviendas/detalle.html', {'vivienda': vivienda})