# import_app/views.py

# django
from django.db.models     import Sum
from django.urls          import reverse, reverse_lazy
from django.utils         import timezone
from django.contrib       import messages
from django.http          import Http404, HttpResponseRedirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

# python
from datetime import datetime

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

        queryset = Imports.objects.values_list('import_date',flat=True).distinct()
        return queryset


# URL - /import/create/
class ImportStockCreateView(CreateView):
    '''Allow users to add stock in current stock'''

    model         = Imports
    form_class    = ImportCreateForm
    template_name = 'import-stock-create.html'
    success_url   = '/import/create/'

    def form_invalid(self, form):
        print('FORM INVALID')
        print(f'{form.errors}')
        return super().form_invalid(form)


    def form_valid(self, form):
        '''Handle already exist data as well'''
        print('FORM VALID')
        print('Cleaned data - ',form.cleaned_data)

        today = timezone.now().date()

        # Already exist
        try:
            import_item = Imports.objects.get(import_date=today, items=form.cleaned_data['items'])
            import_item.import_quantity += form.cleaned_data['import_quantity']
            import_item.save()

        # Newly created
        except Imports.DoesNotExist:
            Imports.objects.create(items=form.cleaned_data['items'], import_quantity=form.cleaned_data['import_quantity'])

        # ITEMS MODEL - Increase total quantity
        form.instance.items.total_quantity += form.cleaned_data['import_quantity']
        form.instance.items.save()

        # Success message
        msg = 'Item imported successfully!'
        messages.info(self.request, msg, extra_tags='danger')

        return HttpResponseRedirect( reverse('import_create') )


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
            obj_import = Imports.objects.filter(import_date=entry_date)
            return obj_import
        raise Http404


    def get_context_data(self, **kwargs):
        '''Adding Entry-date and total-import-quantity'''

        context = super().get_context_data(**kwargs)

        # Entry date
        context['entry_date'] = self.kwargs['entry_date']

        # Total import quantity of entry date
        import_stock                     = self.get_object()
        context['total_import_quantity'] = import_stock.aggregate(totalling=Sum('import_quantity'))['totalling']

        return context


class ImportStockUpdateView(UpdateView):
    '''Allow owner (only) to update the today's entry'''
    pass


class ImportStockDeleteView(DeleteView):
    '''Allow owner (only) to delete the today's entry'''
    pass

