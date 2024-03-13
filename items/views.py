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

        context['final_total_quantity'] = current_stock.aggregate(totalling=Sum('total_quantity'))['totalling']

        return context



