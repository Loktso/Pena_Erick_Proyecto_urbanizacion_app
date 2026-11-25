from django.shortcuts import get_object_or_404, render

from accesos.models import Residente


def residente_list(request):
    # prefetch_related trae las viviendas de todos los residentes en una sola consulta
    residentes = Residente.objects.prefetch_related('viviendas')
    return render(request, 'accesos/residentes/lista.html', {'residentes': residentes})


def residente_detail(request, pk):
    residente = get_object_or_404(Residente, pk=pk)
    return render(request, 'accesos/residentes/detalle.html', {'residente': residente})