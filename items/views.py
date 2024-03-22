# items/views.py

# django
from django.views.generic import ListView, CreateView, UpdateView
from django.db.models     import Sum
from django.urls          import reverse

# local
from .models import Items

# URL - HOMEPAGE OF APPLICATION
class CurrentStockListView(ListView):
    '''Return the available stock of canteen to import/supply'''

    model               = Items
    template_name       = 'current-stock-list.html'
    context_object_name = 'current_stock_list'


    def get_queryset(self):
        '''Will show only active items as current stock'''

        queryset = super().get_queryset()
        return queryset.filter(is_active=True)


    def get_context_data(self, *, object_list=None, **kwargs):
        '''Add total quantity in current stock'''

        context       = super().get_context_data(object_list=object_list, **kwargs)
        current_stock = self.get_queryset()

        context['total_quantity'] = current_stock.aggregate(totalling=Sum('quantity'))['totalling']

        return context


#################################
# CANTEEN ITEMS CRUD OPERATIONS #
#################################

# URL - /items/
class ItemsListView(ListView):
    '''Return all the items of the canteen including non-active'''

    model               = Items
    template_name       = 'item-list.html'
    context_object_name = 'item_list'


    def get_context_data(self, *, object_list=None, **kwargs):
        '''Add total items including non-active items'''

        context = super().get_context_data(object_list=object_list, **kwargs)
        item    = self.get_queryset()

        context['total_items']  = item.count()
        return context


# URL - /create/
class ItemsCreateView(CreateView):
    '''Add canteen items for import/supply'''

    model         = Items
    fields        = ['name','price','is_active']
    template_name = 'item-create.html'


    def form_invalid(self, form):
        print('FORM INVALID')
        print(f'{form.errors}')


    def form_valid(self, form):
        print('FORM VALID')
        print(f'form data - {form.cleaned_data}')
        return super().form_valid(form)


# URL - /create/
class ItemsUpdateView(UpdateView):
    '''Update canteen items name, price & availability'''
    pass
