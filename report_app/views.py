# report_app/views.py

# django
from django.http          import Http404
from django.shortcuts     import get_object_or_404
from django.views.generic import ListView, DetailView

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

        queryset =  Reports.objects.values_list('entry_date',flat=True).distinct()
        return queryset


# URL - /report/<str:entry_date>/
class DailyReportDetailView(DetailView):
    '''Show report details of given date'''

    model               = Reports
    template_name       = 'daily-report-detail.html'
    context_object_name = 'daily_report_detail'

    def get_object(self, queryset=None):
        '''Return report details of provided dates'''

        # Validate provided entry date
        entry_date = validate_entry_date( self.kwargs['entry_date'] )

        if entry_date:
            obj_report = Reports.objects.filter(entry_date=entry_date)
            return obj_report
        raise Http404

    def get_context_data(self, **kwargs):
        '''Adding Entry-date'''

        context = super().get_context_data(**kwargs)
        report  = self.get_object()

        # Entry date
        context['entry_date'] = report[0].entry_date if report else self.kwargs['entry_date']

        return context
