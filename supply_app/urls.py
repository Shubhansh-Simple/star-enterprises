# supply_app/urls.py

# django
from django.urls import path

from .views import SupplyStockListView, SupplyStockCreateView, SupplyStockDetailView, SupplyStockUpdateView, SupplyStockDeleteView

urlpatterns = [
    path('',                  SupplyStockListView.as_view(),   name='supply_list'),
    path('create/',           SupplyStockCreateView.as_view(), name='supply_create'),
    path('<str:entry_date>/', SupplyStockDetailView.as_view(), name='supply_detail'),
    path('<int:pk>/update/',  SupplyStockUpdateView.as_view(), name='supply_update'),
    path('<int:pk>/delete/',  SupplyStockDeleteView.as_view(), name='supply_delete'),
]
