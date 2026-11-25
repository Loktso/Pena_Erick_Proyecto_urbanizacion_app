from django.urls import path

from accesos import views

urlpatterns = [
    path('residentes/', views.residente_list, name='residente_list'),
    path('residentes/<int:pk>/', views.residente_detail, name='residente_detail'),
]