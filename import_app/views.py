# import_app/views.py

# django
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

# local
from .models import Imports


class ImportStockListView(ListView):
    '''Shows the dates list in which stock added'''

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
    '''Shows all entries of import stock of given dates'''
    pass


class ImportStockUpdateView(UpdateView):
    '''Allow owner (only) to update the today's entry'''
    pass


class ImportStockDeleteView(DeleteView):
    '''Allow owner (only) to delete the today's entry'''
    pass

