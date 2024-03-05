# import_app/views.py

# django
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView


class ImportListView(ListView):
    '''Shows the dates list in which stock added'''
    pass


class ImportCreateView(CreateView):
    '''Allow users to add stock in current stock'''
    pass


class ImportDetailView(DetailView):
    '''Allow users to view the details of imports as per dates'''
    pass


class ImportUpdateView(UpdateView):
    '''Allow owner (only) to update the today's entry'''
    pass


class ImportDeleteView(DeleteView):
    '''Allow owner (only) to delete the today's entry'''
    pass

