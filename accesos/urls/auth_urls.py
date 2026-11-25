from django.urls import path

from accesos import views

urlpatterns = [
    path('registrarse/', views.registrarse, name='registrarse'),
    path('login/', views.iniciar_sesion, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
]