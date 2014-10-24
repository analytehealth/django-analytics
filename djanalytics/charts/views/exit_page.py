from collections import defaultdict

from django.db.models import Min
from django.utils.datastructures import SortedDict

from djanalytics import models
from djanalytics.charts.views.base import DateRangeChartView


class ExitPage(DateRangeChartView):
    template_name = 'djanalytics/charts/exit_page.html'

    def get_context_data(self, **kwargs):
        context_data = super(ExitPage, self).get_context_data(**kwargs)
        if not self.client:
            return context_data
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
