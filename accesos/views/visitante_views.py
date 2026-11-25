from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render

from accesos.forms import VisitanteForm
from accesos.models import Visitante


@login_required
@permission_required('accesos.view_visitante', raise_exception=True)
def visitante_list(request):
    visitantes = Visitante.objects.all()
    return render(request, 'accesos/visitantes/lista.html', {'visitantes': visitantes})


@login_required
@permission_required('accesos.view_visitante', raise_exception=True)
def visitante_detail(request, pk):
    visitante = get_object_or_404(Visitante, pk=pk)
    return render(request, 'accesos/visitantes/detalle.html', {'visitante': visitante})


@login_required
@permission_required('accesos.add_visitante', raise_exception=True)
def visitante_create(request):
    if request.method == 'POST':
        form = VisitanteForm(request.POST)
        if form.is_valid():
            visitante = form.save(commit=False)
            visitante.creado_por = request.user
            visitante.save()
            messages.success(request, 'Visitante creado exitosamente.')
            return redirect('visitante_list')
    else:
        form = VisitanteForm()
    return render(request, 'accesos/visitantes/formulario.html', {
        'form': form,
        'titulo': 'Nuevo visitante',
    })


@login_required
@permission_required('accesos.change_visitante', raise_exception=True)
def visitante_update(request, pk):
    visitante = get_object_or_404(Visitante, pk=pk)
    if request.method == 'POST':
        form = VisitanteForm(request.POST, instance=visitante)
        if form.is_valid():
            form.save()
            messages.success(request, 'Visitante actualizado exitosamente.')
            return redirect('visitante_detail', pk=visitante.pk)
    else:
        form = VisitanteForm(instance=visitante)
    return render(request, 'accesos/visitantes/formulario.html', {
        'form': form,
        'titulo': 'Editar visitante',
    })


@login_required
@permission_required('accesos.delete_visitante', raise_exception=True)
def visitante_delete(request, pk):
    visitante = get_object_or_404(Visitante, pk=pk)
    if request.method == 'POST':
        try:
            visitante.delete()
        except ProtectedError:
            messages.error(request, 'No se puede eliminar: el visitante tiene accesos registrados.')
            return redirect('visitante_detail', pk=visitante.pk)
        messages.success(request, 'Visitante eliminado exitosamente.')
        return redirect('visitante_list')
    return render(request, 'accesos/visitantes/confirmar_eliminar.html', {'visitante': visitante})