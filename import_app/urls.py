#import_app/urls.py

# django
from django.urls    import path

# local
from .views import ImportListView, ImportCreateView, ImportDetailView, ImportUpdateView, ImportDeleteView


urlpatterns = [
    path('',                 ImportListView.as_view(),   name='import_list'),
    path('create/',          ImportCreateView.as_view(), name='import_create'),
    path('<int:pk>/',        ImportDetailView.as_view(), name='import_detail'),
    path('<int:pk>/update/', ImportUpdateView.as_view(), name='import_update'),
    path('<int:pk>/delete/', ImportDeleteView.as_view(), name='import_delete'),
]

