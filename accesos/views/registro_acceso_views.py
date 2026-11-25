from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from accesos.forms import RegistroAccesoForm
from accesos.models import RegistroAcceso


def registro_list(request):
    # select_related trae las tablas relacionadas en una sola consulta
    registros = RegistroAcceso.objects.select_related(
        'visitante', 'vivienda', 'autorizado_por', 'creado_por'
    )
    return render(request, 'accesos/registros/lista.html', {'registros': registros})


def registro_detail(request, pk):
    registro = get_object_or_404(RegistroAcceso, pk=pk)
    return render(request, 'accesos/registros/detalle.html', {'registro': registro})


@login_required
def registro_create(request):
    if request.method == 'POST':
        form = RegistroAccesoForm(request.POST)
        if form.is_valid():
            registro = form.save(commit=False)
            registro.creado_por = request.user
            registro.save()
            messages.success(request, 'Registro de acceso creado exitosamente.')
            return redirect('registro_list')
    else:
        form = RegistroAccesoForm()
    return render(request, 'accesos/registros/formulario.html', {
        'form': form,
        'titulo': 'Nuevo registro de acceso',
    })


@login_required
def registro_update(request, pk):
    registro = get_object_or_404(RegistroAcceso, pk=pk)
    if request.method == 'POST':
        form = RegistroAccesoForm(request.POST, instance=registro)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro de acceso actualizado exitosamente.')
            return redirect('registro_detail', pk=registro.pk)
    else:
        form = RegistroAccesoForm(instance=registro)
    return render(request, 'accesos/registros/formulario.html', {
        'form': form,
        'titulo': 'Editar registro de acceso',
    })


@login_required
def registro_delete(request, pk):
    registro = get_object_or_404(RegistroAcceso, pk=pk)
    if request.method == 'POST':
        registro.delete()
        messages.success(request, 'Registro de acceso eliminado exitosamente.')
        return redirect('registro_list')
    return render(request, 'accesos/registros/confirmar_eliminar.html', {'registro': registro})