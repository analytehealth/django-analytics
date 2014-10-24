from datetime import timedelta
from collections import defaultdict

from django.db.models import Min

from graphos.renderers import gchart
from graphos.sources.simple import SimpleDataSource

from djanalytics import models
from djanalytics.charts.views.base import DateRangeChartView


class UserChart(DateRangeChartView):
    template_name = 'djanalytics/charts/users.html'

    def get_context_data(self, **kwargs):
        context_data = super(UserChart, self).get_context_data(**kwargs)
        if not self.client:
            return context_data
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
                'chart': chart,
            }
        )
        return context_data

user_chart = UserChart.as_view()

