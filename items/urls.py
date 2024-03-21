# items/urls.py

# django
from django.urls    import path

# local
from .views import CurrentStockListView, ItemListView


urlpatterns = [
    path('',       CurrentStockListView.as_view(), name='current_stock_list' ),
    path('items/', ItemListView.as_view(),         name='item_list'),
]

