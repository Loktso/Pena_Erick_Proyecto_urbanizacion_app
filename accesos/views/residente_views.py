from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, render

from accesos.models import Residente


@login_required
@permission_required('accesos.view_residente', raise_exception=True)
def residente_list(request):
    residentes = Residente.objects.prefetch_related('viviendas')
    return render(request, 'accesos/residentes/lista.html', {'residentes': residentes})


@login_required
@permission_required('accesos.view_residente', raise_exception=True)
def residente_detail(request, pk):
    residente = get_object_or_404(Residente, pk=pk)
    return render(request, 'accesos/residentes/detalle.html', {'residente': residente})