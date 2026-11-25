from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render

from accesos.forms import VisitanteForm
from accesos.models import Visitante


def visitante_list(request):
    visitantes = Visitante.objects.all()
    return render(request, 'accesos/visitantes/lista.html', {'visitantes': visitantes})


def visitante_detail(request, pk):
    visitante = get_object_or_404(Visitante, pk=pk)
    return render(request, 'accesos/visitantes/detalle.html', {'visitante': visitante})


@login_required
def visitante_create(request):
    if request.method == 'POST':
        form = VisitanteForm(request.POST)
        if form.is_valid():
            visitante = form.save(commit=False)  # arma el objeto sin guardarlo aún
            visitante.creado_por = request.user  # asignamos quién lo creó
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
def visitante_delete(request, pk):
    visitante = get_object_or_404(Visitante, pk=pk)
    # Solo se elimina con POST; el GET únicamente muestra la confirmación
    if request.method == 'POST':
        try:
            visitante.delete()
        except ProtectedError:
            # PROTECT en el modelo: tiene accesos registrados
            messages.error(request, 'No se puede eliminar: el visitante tiene accesos registrados.')
            return redirect('visitante_detail', pk=visitante.pk)
        messages.success(request, 'Visitante eliminado exitosamente.')
        return redirect('visitante_list')
    return render(request, 'accesos/visitantes/confirmar_eliminar.html', {'visitante': visitante})