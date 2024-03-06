# import_app/views.py

# django
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.db.models     import Sum

# python
from datetime import datetime

# local
from .models import Imports


class ImportStockListView(ListView):
    '''Shows the import dates list in which stock added'''

    model = Imports
    template_name       = 'import-stock-list.html'
    context_object_name = 'import_stock_list'

    def get_queryset(self):
        '''Returns only import stock dates'''

        queryset = Imports.objects.values_list('import_date',flat=True).distinct()
        return queryset


class ImportStockCreateView(CreateView):
    '''Allow users to add stock in current stock'''
    pass


class ImportStockDetailView(DetailView):
    '''Shows all entries of imported stock of given dates'''

    model = Imports
    template_name       = 'import-stock-detail.html'
    context_object_name = 'import_stock_detail'

    def get_object(self, queryset=None):
        '''Returns all entries imported stock as per dates'''

        # Convert data into datetime object else 404
        entry_date = self.kwargs['entry_date']
        print('ENTRY DATE - ',entry_date)

        # HARD CODED
        entry_date = datetime.strptime(entry_date,'%Y-%m-%d').date()
        obj_import = Imports.objects.filter(import_date=entry_date)

        return obj_import

    def get_context_data(self, **kwargs):
        '''Adding Entry-date and total-import-quantity'''

        context      = super().get_context_data(**kwargs)
        import_stock = self.get_object()

        # Entry date
        entry_date            = self.kwargs['entry_date']
        entry_date            = f'Import Entries Of {entry_date}'
        context['entry_date'] = entry_date

        # Total import quantity of entry date
        context['total_import_quantity'] = import_stock.aggregate(total_import_quantity=Sum('import_quantity'))['total_import_quantity']

        return context


class ImportStockUpdateView(UpdateView):
    '''Allow owner (only) to update the today's entry'''
    pass


class ImportStockDeleteView(DeleteView):
    '''Allow owner (only) to delete the today's entry'''
    pass

