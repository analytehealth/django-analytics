from datetime import datetime, timedelta
from dateutil import parser

from django.conf import settings
from django.http.response import HttpResponseBadRequest
from django.views.generic.base import TemplateView
from django.utils import timezone

try:
    import pytz
except ImportError:
    pytz = None

from djanalytics import models

class DateRangeChartView(TemplateView):

    def get(self, request, *args, **kwargs):
        client_id = request.GET.get('client_id')
        try:
            self.client = models.Client.objects.get(uuid=client_id)
        except models.Client.DoesNotExist:
            return HttpResponseBadRequest(content='Bad or missing client id')
        return super(DateRangeChartView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super(DateRangeChartView, self).get_context_data(**kwargs)
        if self.request.GET.get('start_date'):
            start_date = parser.parse(
                self.request.GET.get('start_date')
            )
        else:
            start_date = timezone.now() - timedelta(days=7)
        if self.request.GET.get('end_date'):
            end_date = parser.parse(
                self.request.GET.get('end_date')
            )
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
