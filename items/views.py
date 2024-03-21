# items/views.py

# django
from django.views.generic import ListView
from django.db.models     import Sum

# local
from .models import Items

class CurrentStockListView(ListView):
    '''Return the current stock of the canteen'''

    model               = Items
    template_name       = 'current-stock-list.html'
    context_object_name = 'current_stock_list'

    def get_queryset(self):
        '''Will only shows active items in current stock'''

        queryset = super().get_queryset()
        return queryset.filter(is_active=True)


    def get_context_data(self, *, object_list=None, **kwargs):
        '''Add total quantity in current stock'''

        context       = super().get_context_data(object_list=object_list, **kwargs)
        current_stock = self.get_queryset()

        context['total_quantity'] = current_stock.aggregate(totalling=Sum('quantity'))['totalling']

        return context


# ITEMS CRUD OPERATIONS

class ItemListView(ListView):
    '''Return all the items of the canteen including non-active'''

    model               = Items
    template_name       = 'item-list.html'
    context_object_name = 'item_list'


    def get_context_data(self, *, object_list=None, **kwargs):
        '''Add total items count including non-active items'''

        context = super().get_context_data(object_list=object_list, **kwargs)
        item    = self.get_queryset()

        context['total_items']  = item.count()
        return context



