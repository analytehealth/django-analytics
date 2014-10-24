from _collections import defaultdict

from djanalytics.charts.views.base import DateRangeChartView
from djanalytics import models
from django.db.models.aggregates import Count
from django.utils.datastructures import SortedDict
from urlparse import urlparse


class Referrer(DateRangeChartView):
    template_name = 'djanalytics/charts/referrer.html'

    def get_context_data(self, **kwargs):
        context_data = super(Referrer, self).get_context_data(**kwargs)
        if not self.client:
            return context_data
        referrer_query = models.RequestEvent.objects.filter(
            client=self.client,
            created__range=[self.start_date, self.end_date]
        ).exclude(referrer=None).exclude(referrer='')
        for domain in self.client.domain_set.all():
            referrer_query = referrer_query.exclude(
                referrer__regex='^https?://.*%s/?.*' % domain.pattern
            )
        referrer_query = referrer_query.values('referrer').annotate(
            referrals=Count('pk')
        )
        referrer_data = defaultdict(int)
        for data in referrer_query:
            parse_result = urlparse(data['referrer'])
            path = parse_result.path or '/'
            referrer_data[
                '%s://%s%s' % (
                    parse_result.scheme, parse_result.netloc, path
                )
            ] += data['referrals']
        referrer_data = SortedDict(
            sorted(referrer_data.items(), key=lambda x: x[1], reverse=True)
        )
        context_data['referrer_data'] = referrer_data
        return context_data

referrer = Referrer.as_view()