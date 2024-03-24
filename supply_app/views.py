# supply_app/views.py

# django
from django.urls          import reverse, reverse_lazy
from django.http          import Http404, HttpResponseRedirect
from django.utils         import timezone
from django.contrib       import messages
from django.db.models     import Sum
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView


# local
from .models                 import Supplys
from .forms                  import SupplyCreateForm, SupplyUpdateForm
from utils.custom_validators import validate_entry_date
from utils.custom_messages   import generate_msg



# URL - /supply/
class SupplyStockListView(ListView):
    '''Shows the supply dates list in which stock supplied'''

    model               = Supplys
    template_name       = 'supply-stock-list.html'
    context_object_name = 'supply_stock_list'

    def get_queryset(self):
        '''Returns only supply stock dates'''

        queryset = Supplys.objects.values_list('entry_date',flat=True).distinct()
        return queryset



# URL - /supply/create/
class SupplyStockCreateView(CreateView):
    '''Allow users to supply stock from current stock'''

    model         = Supplys
    form_class    = SupplyCreateForm
    template_name = 'supply-stock-create.html'

    def form_invalid(self, form):
        print('FORM INVALID')
        print(f'{form.errors}')
        return super().form_invalid(form)


    def form_valid(self, form):
        '''Handle both Supplys & Items model together'''

        print('FORM VALID')
        print('Cleaned data - ',form.cleaned_data)

        today = timezone.now().date()

        # Form Data Input
        item_input     = form.cleaned_data['items']
        quantity_input = form.cleaned_data['quantity']

        #            [ SUPPLYS MODEL ]
        # Already exist
        try:
            supply_item           = Supplys.objects.get(entry_date=today, items=item_input)
            supply_item.quantity += quantity_input
            supply_item.save()

        # Newly created
        except Supplys.DoesNotExist:
            Supplys.objects.create(items=item_input, quantity=quantity_input)

        #            [ ITEMS MODEL ]
        # Decreased by supplied quantity
        form.instance.items.quantity -= quantity_input
        form.instance.items.save()

        # Success message
        msg = generate_msg(quantity_input, form.instance.items.name, 'supplied')
        messages.info(self.request, msg, extra_tags='danger')

        return HttpResponseRedirect( reverse('supply_create')+'#focus' )



# URL - /supply/<str:entry_date>/
class SupplyStockDetailView(DetailView):
    '''Shows all entries of supplied stock of given dates'''

    model               = Supplys
    template_name       = 'supply-stock-detail.html'
    context_object_name = 'supply_stock_detail'


    def get_object(self, queryset=None):
        '''Returns all entries of supplied stock of provided dates'''

        # Validate provided entry date
        entry_date = validate_entry_date( self.kwargs['entry_date'] )

        if entry_date:
            obj_supply = Supplys.objects.filter(entry_date=entry_date)
            return obj_supply
        raise Http404


    def get_context_data(self, **kwargs):
        '''Adding Entry-date and total-supply-quantity'''

        context      = super().get_context_data(**kwargs)
        supply_stock = self.get_object()

        # Entry date
        context['entry_date'] = supply_stock[0].entry_date if supply_stock else self.kwargs['entry_date']

        # Total supply quantity of entry date
        context['total_supply_quantity'] = supply_stock.aggregate(totalling=Sum('quantity'))['totalling']

        return context



# URL - /supply/<int:pk>/update/
class SupplyStockUpdateView(UpdateView):
    '''Allow user to update the today's entry'''

    model               = Supplys
    form_class          = SupplyUpdateForm
    template_name       = 'supply-stock-update.html'
    context_object_name = 'supply_stock_update'


    def get_form_kwargs(self):
        '''Adding initial unmodifiedable choice of items in Select widget'''

        kwargs            = super().get_form_kwargs()
        kwargs['initial'] = {'items' : str(self.get_object().items)}
        #print('SUPPLY UPDATE KWARGS - ',kwargs)
        return kwargs


    def form_valid(self, form):
        '''
        Handle Items model as well with Supply model
        Only active items allow to be updated
        '''

        print('UPDATE FORM VALID')
        print('Cleaned data - ',form.cleaned_data)

        supply_item            = self.get_object()

        # Only active items can be updated
        if supply_item.items.is_active:

            current_stock_quantity = supply_item.quantity
            updated_stock_quantity = form.cleaned_data['quantity']

            # CHANGE IN SUPPLY-QUANTITY
            if current_stock_quantity != updated_stock_quantity:

                difference = current_stock_quantity - updated_stock_quantity

                #           [SUPPLY MODEL]
                # Updating supply-quantity
                supply_item.quantity = updated_stock_quantity
                supply_item.save()

                #           [ITEMS MODEL]
                supply_item.items.quantity += difference
                supply_item.items.save()

            # Success message
            msg = generate_msg( updated_stock_quantity, supply_item.items.name, 'updated' )

        else:
            # Fail message
            msg = supply_item.items.name + ' is not active, cannot be updated!'

        messages.info(self.request, msg, extra_tags='danger' )
        return HttpResponseRedirect( supply_item.get_absolute_url() )



# URL - /supply/<int:pk>/delete/
class SupplyStockDeleteView(DeleteView):
    '''
    Handle Items model as well with Supplys model
    Only active items allow to be deleted
    '''
    model = Supplys

    def get_success_url(self):
        return self.object.get_absolute_url()


    def form_valid(self, form):
        '''Handle the Items models as well with Supplys model'''
            
        supply_item = self.get_object()

        # Only active items can be deleted
        if supply_item.items.is_active:

            # ITEMS MODEL - Increase total quantity
            supply_item.items.quantity += supply_item.quantity
            supply_item.items.save()

            # Success message
            msg = generate_msg(supply_item.quantity, supply_item.items.name, 'removed')
            messages.info(self.request, msg, extra_tags='dark')

            return super().form_valid(form)
        
        # Redirect with Fail message
        msg = supply_item.items.name + ' is not active, cannot be deleted!'
        messages.info(self.request, msg, extra_tags='danger')

        return HttpResponseRedirect( supply_item.get_absolute_url() )
