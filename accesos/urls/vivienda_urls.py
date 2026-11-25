from django.urls import path

from accesos import views

urlpatterns = [
    path('viviendas/', views.vivienda_list, name='vivienda_list'),
    path('viviendas/<int:pk>/', views.vivienda_detail, name='vivienda_detail'),
]