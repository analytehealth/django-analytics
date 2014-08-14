from collections import defaultdict
from urlparse import urlparse

from django.db.models import Count
from django.utils.datastructures import SortedDict

from djanalytics.charts.views.base import DateRangeChartView
from djanalytics import models


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
