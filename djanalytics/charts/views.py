from collections import defaultdict
from datetime import datetime, timedelta
from dateutil import parser

from django.db.models import Count, Min
from django.views.generic import TemplateView

from graphos.renderers import gchart
from graphos.sources.simple import SimpleDataSource

from djanalytics import models
from django.http.response import HttpResponseBadRequest


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
        default_start = datetime.now() - timedelta(days=7)
        default_end = datetime.now()
        self.start_date = parser.parse(
            self.request.GET.get('start_date', default_start.strftime('%Y-%m-%d 00:00:00'))
        )
        self.end_date = parser.parse(
            self.request.GET.get('end_date', default_end.strftime('%Y-%m-%d 23:59:59'))
        )
        return context_data


class SessionChart(DateRangeChartView):
    template_name = 'charts/sessions.html'

    def get_context_data(self, **kwargs):
        context_data = super(SessionChart, self).get_context_data(**kwargs)
        data = [ ('Date', 'Sessions Created') ]
        date_dict = defaultdict(int)
        for row in models.RequestEvent.objects.with_created_date().filter(
            created__gte=self.start_date,
            created__lte=self.end_date,
            client=self.client
        ).values('created_date').annotate(
            Count('tracking_key', distinct=True)
        ).order_by():
            date_dict[row['created_date']] = row['tracking_key__count']
        d = self.start_date
        while d <= self.end_date:
            data.append( (d.strftime('%Y-%m-%d'), date_dict[d.strftime('%Y-%m-%d')]) ) 
            d += timedelta(days=1)
        chart = gchart.LineChart(SimpleDataSource(data=data),
            options={
                'title': 'Sessions Created'
            })
        context_data.update(
            {
                'chart': chart
            }
        )
        return context_data

session_chart = SessionChart.as_view()


class UserChart(DateRangeChartView):
    template_name = 'charts/users.html'

    def get_context_data(self, **kwargs):
        context_data = super(UserChart, self).get_context_data(**kwargs)
        data = [ ('Date', 'Sessions Created') ]
        date_dict = defaultdict(int)
        for row in models.RequestEvent.objects.values(
            'tracking_user_id'
        ).annotate(new_date=Min('created')).filter(
            new_date__gte=self.start_date,
            new_date__lte=self.end_date,
            client=self.client
        ):
            date_dict[row['new_date'].strftime('%Y-%m-%d')] += 1
        d = self.start_date
        while d <= self.end_date:
            data.append( (d.strftime('%Y-%m-%d'), date_dict[d.strftime('%Y-%m-%d')]) )
            d += timedelta(days=1)
        chart = gchart.LineChart(SimpleDataSource(data=data))
        context_data.update(
            {
                'chart': chart
            }
        )
        return context_data

user_chart = UserChart.as_view()