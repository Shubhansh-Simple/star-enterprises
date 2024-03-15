# supply_app/views.py

# django
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

# local
from .models                 import Supplys
from .forms                  import SupplyCreateForm, SupplyUpdateForm
from utils.custom_validators import validate_entry_date


# URL - /supply/
class SupplyStockListView(ListView):
    '''Shows the supply dates list in which stock supplied'''

    model               = Supplys
    template_name       = 'supply-stock-list.html'
    context_object_name = 'supply_stock_list'

    def get_queryset(self):
        '''Returns only supply stock dates'''

        queryset = Supplys.objects.values_list('supply_date',flat=True).distinct()
        return queryset


# URL - /supply/create/
class SupplyStockCreateView(CreateView):
    '''Allow users to supply stock from current stock'''

    model         = Supplys
    form_class    = SupplyCreateForm
    template_name = 'supply-stock-create.html'


# URL - /supply/<str:entry_date>/
class SupplyStockDetailView(DetailView):
    '''Shows all entries of supplied stock of given dates'''

    model               = Supplys
    template_name       = 'supply-stock-detail.html'
    context_object_name = 'supply_stock_detail'


# URL - /supply/<int:pk>/update/
class SupplyStockUpdateView(UpdateView):
    '''Allow owner (only) to update the today's entry'''

    model               = Supplys
    form_class          = SupplyUpdateForm
    template_name       = 'supply-stock-update.html'
    context_object_name = 'supply_stock_update'


# URL - /supply/<int:pk>/delete/
class SupplyStockDeleteView(DeleteView):
    '''Allow owner (only) to delete the today's entry'''

    model       = Supplys
