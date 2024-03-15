# Core/urls.py

# django
from django.contrib import admin
from django.urls    import path, include

urlpatterns = [
    # admin site
    path('admin/', admin.site.urls),

    # custom apps
    path('',        include('items.urls') ),
    path('import/', include('import_app.urls') ),
    path('supply/', include('supply_app.urls') ),
]


# Updating Admin Site's Page Title
admin.site.site_header = 'ADMINISTRATION'
admin.site.index_title = 'Star Enterprises Database'


