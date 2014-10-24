from collections import defaultdict
from urlparse import urlparse

from django.db.models import Count
from django.utils.datastructures import SortedDict

from djanalytics import models
from djanalytics.charts.views.base import DateRangeChartView
from djanalytics.charts.forms import PageViewChartForm


class PageVisit(DateRangeChartView):
    template_name = 'djanalytics/charts/page_visit.html'
    form_class = PageViewChartForm

    def get_context_data(self, **kwargs):
        context_data = super(PageVisit, self).get_context_data(**kwargs)
        if not self.client:
            return context_data
        query = models.RequestEvent.objects.filter(
            client=self.client,
            created__range=[self.start_date, self.end_date]
        )
        start_page = self.form.cleaned_data.get('start_page')
        if start_page:
            query = query.filter(path=start_page)
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
            'start_page': start_page or target_page['path'],
        })
        return context_data

page_visit = PageVisit.as_view()
