from django.urls import path
from . import views

urlpatterns = [
    # Buses
    path('buses/', views.BusListView.as_view(), name='bus_list'),
    path('buses/nuevo/', views.BusCreateView.as_view(), name='bus_create'),
    path('buses/<int:pk>/', views.BusDetailView.as_view(), name='bus_detail'),
    path('buses/<int:pk>/editar/', views.BusUpdateView.as_view(), name='bus_update'),
    path('buses/<int:pk>/eliminar/', views.BusDeleteView.as_view(), name='bus_delete'),
]
