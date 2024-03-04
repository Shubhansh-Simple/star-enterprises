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
        return super().get_queryset()

    def get_context_data(self, *, object_list=None, **kwargs):
        '''Add total quantity in current stock'''

        context       = super().get_context_data(object_list=object_list, **kwargs)
        current_stock = self.get_queryset()

        context['final_total_quantity'] = current_stock.aggregate(final_total_quantity=Sum('total_quantity'))['final_total_quantity']

        return context



