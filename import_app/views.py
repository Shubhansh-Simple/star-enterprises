# import_app/views.py

# django
from django.http          import Http404, HttpResponseRedirect
from django.urls          import reverse 
from django.utils         import timezone
from django.contrib       import messages
from django.db.models     import Sum
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

# local
from .models                 import Imports
from .forms                  import ImportCreateForm, ImportUpdateForm
from utils.custom_validators import validate_entry_date
from utils.custom_messages   import generate_msg



# URL - /import/
class ImportStockListView(ListView):
    '''Shows the import dates list in which stock added'''

    model               = Imports
    template_name       = 'import-stock-list.html'
    context_object_name = 'import_stock_list'

    def get_queryset(self):
        '''Returns only import stock dates'''

        queryset = Imports.objects.values_list('entry_date',flat=True).distinct()
        return queryset



# URL - /import/create/
class ImportStockCreateView(CreateView):
    '''Allow users to add stock in current stock'''

    model         = Imports
    form_class    = ImportCreateForm
    template_name = 'import-stock-create.html'

    def form_invalid(self, form):
        print('FORM INVALID')
        print(f'{form.errors}')
        return super().form_invalid(form)


    def form_valid(self, form):
        '''Handle already exist data and Import Model as well'''

        print('FORM VALID')
        print('Cleaned data - ',form.cleaned_data)

        today = timezone.now().date()

        # Form Data Input
        item_input     = form.cleaned_data['items']
        quantity_input = form.cleaned_data['quantity']

        #            [ IMPORTS MODEL ]
        # Already exist
        try:
            import_item           = Imports.objects.get(entry_date=today, items=item_input)
            import_item.quantity += quantity_input
            import_item.save()

        # Newly created
        except Imports.DoesNotExist:
            Imports.objects.create(items=item_input, quantity=quantity_input)

        #            [ ITEMS MODEL ] 
        # Increased by imported quantity
        form.instance.items.quantity += quantity_input
        form.instance.items.save()

        # Success message
        msg = generate_msg(quantity_input, form.instance.items.name, 'added')
        messages.info(self.request, msg, extra_tags='success')

        return HttpResponseRedirect( reverse('import_create') + '#focus' )



# URL - /import/<str:entry_date>/
class ImportStockDetailView(DetailView):
    '''Shows all entries of imported stock of given dates'''

    model               = Imports
    template_name       = 'import-stock-detail.html'
    context_object_name = 'import_stock_detail'


    def get_object(self, queryset=None):
        '''Returns all entries of imported stock of provided dates'''

        # Validate provided entry date
        entry_date = validate_entry_date( self.kwargs['entry_date'] )

        if entry_date:
            obj_import = Imports.objects.filter(entry_date=entry_date)
            return obj_import
        raise Http404


    def get_context_data(self, **kwargs):
        '''Adding Entry-date and total-import-quantity'''

        context      = super().get_context_data(**kwargs)
        import_stock = self.get_object()

        # Entry date
        context['entry_date'] = import_stock[0].entry_date if import_stock else self.kwargs['entry_date']

        # Total import quantity of entry date
        context['total_import_quantity'] = import_stock.aggregate(totalling=Sum('quantity'))['totalling']

        return context



# URL - /import/<int:pk>/update/
class ImportStockUpdateView(UpdateView):
    '''Allow user to update the today's entry'''

    model               = Imports
    form_class          = ImportUpdateForm
    template_name       = 'import-stock-update.html'
    context_object_name = 'import_stock_update'


    def get_form_kwargs(self):
        '''Adding initial unmodifiedable choice of items in Select widget'''

        kwargs            = super().get_form_kwargs()
        kwargs['initial'] = {'items' : str(self.get_object().items) }
        #print('IMPORT UPDATE KWARGS - ',kwargs)
        return kwargs


    def form_valid(self, form):
        '''Handle Import and Items model as well'''

        print('UPDATE FORM VALID')
        print('Cleaned data - ',form.cleaned_data)

        import_item            = self.get_object()

        # Only active items can be updated
        if import_item.items.is_active:

            current_stock_quantity = import_item.quantity
            updated_stock_quantity = form.cleaned_data['quantity']

            # CHANGE IN IMPORT-QUANTITY
            if current_stock_quantity != updated_stock_quantity:

                difference = current_stock_quantity - updated_stock_quantity

                #           [IMPORTS MODEL]
                # Updating import-quantity
                import_item.quantity = updated_stock_quantity
                import_item.save()

                #           [ITEMS MODEL]
                import_item.items.quantity -= difference
                import_item.items.save()

            # Success message
            msg = generate_msg(updated_stock_quantity, import_item.items.name, 'updated')

        else:
            # Fail message
            msg = import_item.items.name + ' is not active, cannot be updated!'

        messages.info(self.request, msg, extra_tags='success')
        return HttpResponseRedirect( import_item.get_absolute_url() )



# URL - /import/<int:pk>/delete/
class ImportStockDeleteView(DeleteView):
    '''
    Handle Items model as well with Imports model
    Only active items allow to be deleted
    '''
    model = Imports

    def get_success_url(self):
        return self.object.get_absolute_url()


    def form_valid(self, form):
        '''Handle the Items models as well with Imports model'''

        import_item = self.get_object()

        # Only active items can be deleted
        if import_item.items.is_active:

            # ITEMS MODEL - Decrease total quantity
            import_item.items.quantity -= import_item.quantity
            import_item.items.save()

            # Success message
            msg = generate_msg(import_item.quantity, import_item.items.name, 'removed')
            messages.info(self.request, msg, extra_tags='dark')

            return super().form_valid(form)

        # Redirect with Fail message
        msg = import_item.items.name + ' is not active, cannot be deleted!'
        messages.info(self.request, msg, extra_tags='danger')

        return HttpResponseRedirect( import_item.get_absolute_url() )

