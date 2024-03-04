# items/urls.py

# django
from django.urls    import path

# local
from .views import CurrentStockListView


urlpatterns = [
    path('', CurrentStockListView.as_view(), name='current_stock_list' ),
]

