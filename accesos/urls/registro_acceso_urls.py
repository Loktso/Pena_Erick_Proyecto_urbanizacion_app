from django.urls import path

from accesos import views

urlpatterns = [
    # La portada del sitio ('') muestra el listado de registros
    path('', views.registro_list, name='inicio'),
    path('registros/', views.registro_list, name='registro_list'),
    path('registros/nuevo/', views.registro_create, name='registro_create'),
    path('registros/<int:pk>/', views.registro_detail, name='registro_detail'),
    path('registros/<int:pk>/editar/', views.registro_update, name='registro_update'),
    path('registros/<int:pk>/eliminar/', views.registro_delete, name='registro_delete'),
]