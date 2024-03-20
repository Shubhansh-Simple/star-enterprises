# report_app/views.py

# django
from django.views.generic import ListView, DetailView
from django.shortcuts     import get_object_or_404

# local
from .models                 import Reports
from utils.custom_validators import validate_entry_date


# URL - /report/
class DailyReportListView(ListView):
    '''Shows the report dates list in which stock imported/exported'''

    model               = Reports
    template_name       = 'daily-report-list.html'
    context_object_name = 'daily_report_list'

    def get_queryset(self):
        '''Returns entry dates of daily reports'''

        queryset =  Reports.objects.values_list('entry_date',flat=True)
        return queryset


# URL - /report/<str:entry_date>/
class DailyReportDetailView(DetailView):
    ''''''

    model               = Reports
    template_name       = 'daily-report-detail.html'
    context_object_name = 'daily_report_detail'


    def get_object(self, queryset=None):
        '''Returns entries details of provided dates'''

        # Validate provided entry date
        entry_date = validate_entry_date( self.kwargs['entry_date'] )

        get_object_or_404(Reports,)

        return super().get_object(queryset)
