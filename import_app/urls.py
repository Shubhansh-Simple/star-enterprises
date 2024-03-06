#import_app/urls.py

# django
from django.urls    import path

# local
from .views import ImportStockListView, ImportStockCreateView, ImportStockDetailView, ImportStockUpdateView, ImportStockDeleteView


urlpatterns = [
    path('',                 ImportStockListView.as_view(),   name='import_list'),
    path('create/',          ImportStockCreateView.as_view(), name='import_create'),
    path('<int:pk>/',        ImportStockDetailView.as_view(), name='import_detail'),
    path('<int:pk>/update/', ImportStockUpdateView.as_view(), name='import_update'),
    path('<int:pk>/delete/', ImportStockDeleteView.as_view(), name='import_delete'),
]

