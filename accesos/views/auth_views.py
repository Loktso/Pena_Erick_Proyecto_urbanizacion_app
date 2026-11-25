from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from accesos.forms import RegistroForm


def registrarse(request):
    # Si ya tiene sesión, no tiene sentido registrarse otra vez
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)  # inicia sesión automáticamente
            messages.success(request, f'Cuenta creada. Bienvenido, {usuario.username}.')
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = RegistroForm()
    return render(request, 'accesos/auth/registrarse.html', {'form': form})


def iniciar_sesion(request):
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)
    # "next" es la página que el usuario quería abrir antes de que lo mandaran al login
    siguiente = request.POST.get('next') or request.GET.get('next') or ''
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            messages.success(request, f'Bienvenido, {usuario.username}.')
            # Solo se redirige a "next" si apunta a este mismo sitio (evita redirecciones a webs externas)
            if siguiente and url_has_allowed_host_and_scheme(
                siguiente, allowed_hosts={request.get_host()}
            ):
                return redirect(siguiente)
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = AuthenticationForm(request)
    return render(request, 'accesos/auth/login.html', {'form': form, 'next': siguiente})


@require_POST  # si alguien abre /logout/ escribiendo la URL (GET), Django responde 405
def cerrar_sesion(request):
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente.')
    return redirect(settings.LOGOUT_REDIRECT_URL)