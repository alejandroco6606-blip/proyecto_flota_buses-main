from django.urls import path
from . import views

app_name = 'viajes'

urlpatterns = [
    # Viajes
    path('', views.ViajeListView.as_view(), name='viaje_list'),
    path('nuevo/', views.ViajeCreateView.as_view(), name='viaje_create'),
    path('<int:pk>/', views.ViajeDetailView.as_view(), name='viaje_detail'),
    path('<int:pk>/editar/', views.ViajeUpdateView.as_view(), name='viaje_update'),
    path('<int:pk>/eliminar/', views.ViajeDeleteView.as_view(), name='viaje_delete'),
]
