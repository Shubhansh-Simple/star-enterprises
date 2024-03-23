# items/views.py

# django
from django.http          import HttpResponseRedirect
from django.contrib       import messages
from django.db.models     import ProtectedError, Sum
from django.views.generic import DeleteView, ListView, CreateView, UpdateView

# local
from .models               import Items
from utils.custom_messages import generate_msg



# URL - HOMEPAGE OF APPLICATION
class CurrentStockListView(ListView):
    '''Return the available stock of canteen for import/supply'''

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
    '''Return all the items of the canteen including non-active ones'''

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
        print(f'CLEANED DATA - {form.cleaned_data}')
        return super().form_invalid(form)


    def form_valid(self, form):
        '''Adding success message on form data is valid'''
        
        print('FORM VALID')
        print(f'form data - {form.cleaned_data}')

        # Success message
        msg = generate_msg( 0, form.cleaned_data['name'], 'added' )
        messages.info(self.request, msg, extra_tags='warning')

        return super().form_valid(form)



# URL - /update/<int:pk>/
class ItemsUpdateView(UpdateView):
    '''Update canteen items fields - name, price & availability'''

    model               = Items
    fields              = ['name','price','is_active']
    template_name       = 'item-update.html'
    context_object_name = 'item_update'

    def form_valid(self, form):
        '''Adding update message on form data is valid'''

        print('FORM VALID')
        print(f'form data - {form.cleaned_data}')

        # Success message
        msg = generate_msg( 0, form.cleaned_data['name'], 'updated' )
        messages.info(self.request, msg, extra_tags='warning' )

        return super().form_valid(form)



# URL - /delete/<int:pk>/
class ItemsDeleteView(DeleteView):
    '''Delete canteen items if not used by any table records (models.PROTECT)'''

    model = Items

    def form_valid(self, form):
        '''Delete the item if no dependency of item found, otherwise show cannot delete msg'''

        item = self.get_object()

        # Try to delete the item
        try:
            item.delete()
            msg   = generate_msg(0, item.name, 'removed')
            color = 'dark'

        # dependency found
        except ProtectedError:
            msg   = f'{item.name} cannot be deleted! ( Used by other entries)'
            color = 'danger'

        # Success message
        messages.info(self.request, msg, extra_tags=color)

        return HttpResponseRedirect( item.get_absolute_url() )
