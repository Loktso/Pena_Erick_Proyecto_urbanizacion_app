from django.urls import path

from accesos import views

urlpatterns = [
    path('visitantes/', views.visitante_list, name='visitante_list'),
    path('visitantes/nuevo/', views.visitante_create, name='visitante_create'),
    path('visitantes/<int:pk>/', views.visitante_detail, name='visitante_detail'),
    path('visitantes/<int:pk>/editar/', views.visitante_update, name='visitante_update'),
    path('visitantes/<int:pk>/eliminar/', views.visitante_delete, name='visitante_delete'),
]