# report_app/views.py

# django
from django.views.generic import ListView, DetailView

# local
from .models                import Reports
from utils.custom_validators import validate_entry_date


# URL - /report/
class DailyReportListView(ListView):
    '''Shows the report dates list in which stock imported/exported'''

    model               = Reports
    template_name       = 'daily-report-list.html'
    context_object_name = 'daily-report_list'


# URL - /report/<str:entry_date>/
class DailyReportDetailView(DetailView):
    ''''''

    model               = Reports
    template_name       = 'daily-report-detail.html'
    context_object_name = 'daily-report_detail'
