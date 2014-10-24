from djanalytics.reports.forms import DateRangeForm
from django import forms

class PageViewChartForm(DateRangeForm):
    start_page = forms.CharField(required=False)
