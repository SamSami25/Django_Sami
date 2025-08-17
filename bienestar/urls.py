from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('iniciar/', views.iniciar_test, name='iniciar'),
    path('test/', views.test, name='test'),
    path("exportar_excel/", views.exportar_excel, name="exportar_excel"),
]
