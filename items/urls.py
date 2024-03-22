# items/urls.py

# django
from django.urls    import path

# local
from .views import CurrentStockListView, ItemsListView, ItemsCreateView, ItemsUpdateView


urlpatterns = [
    # Current available stock in canteen
    path('',       CurrentStockListView.as_view(), name='current_stock_list' ),

    # CRUD of canteen items including non-active items
    path('items/',  ItemsListView.as_view(),   name='item_list'),
    path('create/', ItemsCreateView.as_view(), name='item_create'),
    path('update/<int:pk>/', ItemsUpdateView.as_view(), name='item_update'),
    #path('delete/<int:pk>/', ItemsDeleteView.as_view(), name='item_delete'),
]

