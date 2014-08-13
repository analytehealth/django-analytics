from collections import defaultdict
from datetime import datetime, timedelta
from dateutil import parser
from urlparse import urlparse

from django.conf import settings
from django.db.models import Count, Min
from django.http.response import HttpResponseBadRequest
from django.utils.datastructures import SortedDict
from django.views.generic import TemplateView

from graphos.renderers import gchart
from graphos.sources.simple import SimpleDataSource

from djanalytics import models
from django.utils import timezone
from django.utils.timezone import UTC

try:
    import pytz
except ImportError:
    pytz = None


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
                self.request.GET.get('end_date', datetime.now())
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
                tz = UTC()
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


class SessionChart(DateRangeChartView):
    template_name = 'charts/sessions.html'

    def get_context_data(self, **kwargs):
        context_data = super(SessionChart, self).get_context_data(**kwargs)
        data = [ ('Date', 'Sessions Created') ]
        date_dict = defaultdict(int)
        for row in models.RequestEvent.objects.values(
            'tracking_key'
        ).annotate(new_date=Min('created')).filter(
            new_date__range=[self.start_date, self.end_date],
            client=self.client
        ):
            date_dict[row['new_date'].strftime('%Y-%m-%d')] += 1
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
        data = [ ('Date', 'Users Created') ]
        date_dict = defaultdict(int)
        for row in models.RequestEvent.objects.values(
            'tracking_user_id'
        ).annotate(new_date=Min('created')).filter(
            new_date__range=[self.start_date, self.end_date],
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

class PageVisit(DateRangeChartView):
    template_name = 'charts/page_visit.html'

    def get(self, request, *args, **kwargs):
        self.start_page = request.GET.get('start_page')
        return super(PageVisit, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super(PageVisit, self).get_context_data(**kwargs)
        query = models.RequestEvent.objects.filter(
            client=self.client,
            created__range=[self.start_date, self.end_date]
        )
        if self.start_page:
            query = query.filter(path=self.start_page)
        try:
            target_page = query.values('path').annotate(visits=Count('pk')).order_by('-visits')[0]
        except IndexError:
            return context_data
        
        parent_pages = defaultdict(int)
        for parent in models.RequestEvent.objects.filter(
            created__range=[self.start_date, self.end_date],
            path=target_page['path']
        ):
            key = ''
            if parent.referrer:
                parsed_url = urlparse(parent.referrer)
                key = '%s://%s%s' % (
                    parsed_url.scheme, parsed_url.netloc, parsed_url.path
                )
            parent_pages[key] += 1
        parent_pages = SortedDict(
            sorted(parent_pages.items(), key=lambda x: x[1], reverse=True)
        )
        child_pages = models.RequestEvent.objects.filter(
            created__range=[self.start_date, self.end_date],
            referrer__endswith=target_page['path']
        ).values(
            'path'
        ).annotate(visits=Count('pk')).order_by('-visits')
        page_info = {
            'target_page': target_page,
            'parent_pages': parent_pages,
            'child_pages': child_pages
        }
        context_data.update({
            'page_info': page_info,
            'start_page': self.start_page or target_page['path'],
        })
        return context_data

page_visit = PageVisit.as_view()


class ExitPage(DateRangeChartView):
    template_name = 'charts/exit_page.html'

    def get_context_data(self, **kwargs):
        context_data = super(ExitPage, self).get_context_data(**kwargs)
        exit_page_data = defaultdict(int)
        sessions_query = models.RequestEvent.objects.values(
            'tracking_key'
        ).annotate(new_date=Min('created')).filter(
            new_date__range=[self.start_date, self.end_date],
            client=self.client
        )
        sessions = list(data['tracking_key'] for data in sessions_query)
        for exit_page_row in models.RequestEvent.objects.filter(
            tracking_key__in=sessions
        ).values('path', 'tracking_key').order_by(
            'tracking_key', '-created'
        ):
            if exit_page_row['tracking_key'] in sessions:
                exit_page_data[exit_page_row['path']] += 1
                sessions.pop(sessions.index(exit_page_row['tracking_key']))
        exit_page_data = SortedDict(
            sorted(exit_page_data.items(), key=lambda x: x[1], reverse=True)
        )
        context_data.update({
            'exit_page_data': exit_page_data
        })
        return context_data

exit_page = ExitPage.as_view()