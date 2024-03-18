# supply_app/views.py

# django
from django.http          import Http404
from django.db.models     import Sum
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

        queryset = Supplys.objects.values_list('entry_date',flat=True).distinct()
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
    '''Allow owner (only) to update the today's entry'''

    model               = Supplys
    form_class          = SupplyUpdateForm
    template_name       = 'supply-stock-update.html'
    context_object_name = 'supply_stock_update'


# URL - /supply/<int:pk>/delete/
class SupplyStockDeleteView(DeleteView):
    '''Allow owner (only) to delete the today's entry'''

    model       = Supplys
