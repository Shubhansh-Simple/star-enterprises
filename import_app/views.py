# import_app/views.py

# django
from django.db.models     import Sum
from django.urls          import reverse, reverse_lazy
from django.utils         import timezone
from django.contrib       import messages
from django.http          import Http404, HttpResponseRedirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

# local
from .models                 import Imports
from .forms                  import ImportCreateForm, ImportUpdateForm
from utils.custom_validators import validate_entry_date


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

        # Already exist
        try:
            import_item = Imports.objects.get(entry_date=today, items=item_input)
            import_item.quantity += quantity_input
            import_item.save()

        # Newly created
        except Imports.DoesNotExist:
            Imports.objects.create(items=item_input, quantity=quantity_input)

        # ITEMS MODEL - Increase total quantity
        form.instance.items.total_quantity += form.cleaned_data['quantity']
        form.instance.items.save()

        # Success message
        msg = 'Item imported successfully!'
        messages.info(self.request, msg, extra_tags='success')

        return HttpResponseRedirect( reverse('import_create')+'#focus' )


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
    '''Allow owner (only) to update the today's entry'''

    model               = Imports
    form_class          = ImportUpdateForm
    template_name       = 'import-stock-update.html'
    context_object_name = 'import_stock_update'


    def get_form_kwargs(self):
        '''Adding default choice in imported Items widget'''

        kwargs            = super().get_form_kwargs()
        kwargs['initial'] = {'items' : str(self.get_object().items) }
        return kwargs


    def form_valid(self, form):
        '''Handle Import and Items model as well'''

        print('UPDATE FORM VALID')
        print('Cleaned data - ',form.cleaned_data)

        import_item   = self.get_object()
        old_stock     = import_item.quantity
        updated_stock = form.cleaned_data['quantity']

        # CHANGE IN IMPORT-QUANTITY
        if old_stock != updated_stock:

            difference = abs(old_stock - updated_stock)

            # Changing import-quantity
            import_item.quantity = updated_stock
            import_item.save()

            # Changing total-quantity

            # INCREMENT OF IMPORT-STOCK
            if old_stock < updated_stock:
                import_item.items.total_quantity += difference

            # DECREMENT OF IMPORT-STOCK
            else:
                import_item.items.total_quantity -= difference

            import_item.items.save()

        # Success message
        msg = 'Item updated successfully!'
        messages.info(self.request, msg, extra_tags='success')

        return HttpResponseRedirect( reverse('import_detail', kwargs={'entry_date' : import_item.entry_date}) + '#focus' )


# URL - /import/<int:pk>/delete/
class ImportStockDeleteView(DeleteView):
    '''Allow owner (only) to delete the today's entry'''

    model       = Imports

    def get_success_url(self):
        '''Redirect to DetailPage after deletion'''

        return reverse_lazy('import_detail', kwargs={'entry_date' : self.object.entry_date}) + '#focus'


    def form_valid(self, form):
        '''Add success messsage'''

        # ITEMS MODEL - Decrease total quantity
        import_item                       = self.get_object()
        import_item.items.total_quantity -= import_item.quantity
        import_item.items.save()

        msg = 'Item deleted successfully!'
        messages.info(self.request, msg, extra_tags='dark')

        return super().form_valid(form)

