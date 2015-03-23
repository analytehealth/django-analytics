from datetime import datetime, timedelta

from django.conf import settings
from django.utils import timezone
from django.views.generic import FormView

from djanalytics.charts.forms import DateRangeForm

try:
    import pytz
except ImportError:
    pytz = None


class DateRangeChartView(FormView):

    form_class = DateRangeForm

    def __init__(self, *args, **kwargs):
        super(DateRangeChartView, self).__init__(*args, **kwargs)
        self.client = None
        self.form = None

    def get_initial(self):
        return {
            'start_date': timezone.now() - timedelta(days=7),
            'end_date': timezone.now()
        }

    def form_valid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context_data = super(DateRangeChartView, self).get_context_data(**kwargs)
        self.form = context_data.get('form')
        if self.form.is_valid():
            if self.form.cleaned_data.get('start_date'):
                start_date = self.form.cleaned_data['start_date']
            else:
                start_date = timezone.now() - timedelta(days=7)
            if self.form.cleaned_data.get('end_date'):
                end_date = self.form.cleaned_data['end_date']
            else:
                end_date = timezone.now()
            self.start_date = datetime(
                start_date.year, start_date.month,
                start_date.day, 0, 0, 0
            )
            self.end_date = datetime(
                end_date.year, end_date.month,
                end_date.day, 23, 59
            )
            self.client = self.form.cleaned_data['client']
            if settings.USE_TZ:
                if pytz:
                    tz = pytz.timezone(settings.TIME_ZONE)
                else:
                    tz = timezone.UTC()
                if not timezone.is_aware(self.start_date):
                    self.start_date = tz.localize(self.start_date)
                if not timezone.is_aware(self.end_date):
                    self.end_date = tz.localize(self.end_date)
            context_data.update({
                'start_date': self.start_date.strftime('%m/%d/%Y'),
                'end_date': self.end_date.strftime('%m/%d/%Y'),
                'client_id': self.client.uuid,
            })
        return context_data
