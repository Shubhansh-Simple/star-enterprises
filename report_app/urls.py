# report_app/urls.py

# django
from django.urls import path

# local
from .views import DailyReportListView, DailyReportDetailView


urlpatterns = [
    path('', DailyReportListView.as_view(), name='report_list'),
    path('<str:entry_date>/', DailyReportDetailView.as_view(), name='report_detail'),
]
