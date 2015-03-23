import re

from collections import defaultdict

from django.db.models import Count, Sum
from django.utils.datastructures import SortedDict

from djanalytics import models
from djanalytics.reports import utils

from .base import DateRangeReportView


class PageOverviewReport(DateRangeReportView):
    report_name = "Page Overview"
    default_sort = ('Pageviews', DateRangeReportView.DESCENDING)

    def _build_report_data(self):
        page_visits = list(self.visit_queryset().values_list('pagevisit__pk', flat=True))
        if not page_visits:
            return []

        pages = models.PageVisit.objects.filter(
            pk__in=page_visits
        ).values('page__path').annotate(
            pageviews=Count('pk'),
            unique_pageviews=Count('visit__uuid', distinct=True),
            duration=Sum('duration')
        ).values(
            'page__path',
            'pageviews',
            'unique_pageviews',
            'duration'
        )

        if self.client:
            page_pattern_query = models.PagePattern.objects.filter(
                client=self.client
            )
        else:
            page_pattern_query = models.PagePattern.objects.filter(
                client__domain__web_property=self.web_property
            )
        page_patterns = {
            pattern.display_path: re.compile(pattern.pattern, re.IGNORECASE)
            for pattern in page_pattern_query
        }

        entrances = self.visit_queryset().values(
            'first_page__path'
        ).annotate(Count('uuid'))

        bounce_pks = list(
            self.visit_queryset().annotate(
                page_count=Count('pages')
            ).filter(page_count=1).values_list('pk', flat=True)
        )
        bounces = models.Page.objects.filter(
            pagevisit__visit__pk__in=bounce_pks
        ).values('path').annotate(
            bounce_count=Count('pagevisit__visit')
        ).values('path', 'bounce_count')

        exits = self.visit_queryset().exclude(last_page=None).values(
            'last_page__path'
        ).annotate(Count('uuid'))

        tmp_data = SortedDict()
        totals = defaultdict(int)
        pageview_idx = self._build_report_headers().index('Pageviews')
        uniqueview_idx = self._build_report_headers().index('Unique Pageviews')
        duration_idx = self._build_report_headers().index('Avg. Time on Page')
        sub_durations = defaultdict(int)
        for page in pages:
            path = page['page__path']
            duration = 0 if page['duration'] is None else page['duration']
            for display_path, regex in page_patterns.items():
                if regex.match(path):
                    path = display_path
                    sub_durations[path] += duration
                    break
            if path in tmp_data:
                tmp_data[path][pageview_idx] += page['pageviews']
                tmp_data[path][uniqueview_idx] += page['unique_pageviews']
            else:
                tmp_data[path] = [
                    path,
                    page['pageviews'],
                    page['unique_pageviews'],
                    utils.average_duration(duration, page['pageviews']),
                    0,  # entrances
                    0,  # bounce rate
                    0,  # % exit
                ]
            totals['pageviews'] += page['pageviews']
            totals['unique_pageviews'] += page['unique_pageviews']
            totals['duration'] += duration

        for path, total_duration in sub_durations.items():
            tmp_data[path][duration_idx] = utils.average_duration(
                total_duration, tmp_data[path][pageview_idx]
            )

        entrance_idx = self._build_report_headers().index('Entrances')
        for entrance in entrances:
            path = entrance['first_page__path']
            for name, regex in page_patterns.items():
                if regex.match(path):
                    path = name
                    break
            tmp_data[path][entrance_idx] += entrance['uuid__count']
            totals['entrances'] += entrance['uuid__count']

        bounce_idx = self._build_report_headers().index('Bounce Rate')
        sub_bounces = defaultdict(int)
        for bounce in bounces:
            path = bounce['path']
            for name, regex in page_patterns.items():
                if regex.match(path):
                    path = name
                    sub_bounces[path] += bounce['bounce_count']
                    break
            tmp_data[path][bounce_idx] = utils.percentage(
                bounce['bounce_count'], tmp_data[path][pageview_idx]
            )
            totals['bounces'] += bounce['bounce_count']
        for path, total_bounce in sub_bounces.items():
            tmp_data[path][bounce_idx] = utils.percentage(
                total_bounce, tmp_data[path][pageview_idx]
            )

        exit_idx = self._build_report_headers().index('% Exit')
        sub_exits = defaultdict(int)
        for exit_page in exits:
            path = exit_page['last_page__path']
            for name, regex in page_patterns.items():
                if regex.match(path):
                    path = name
                    sub_exits[path] += exit_page['uuid__count']
                    break
            if path in tmp_data.keys():
                tmp_data[path][exit_idx] = utils.percentage(
                    exit_page['uuid__count'], tmp_data[path][pageview_idx]
                )
                totals['exits'] += exit_page['uuid__count']
        for path, total_exits in sub_exits.items():
            tmp_data[path][exit_idx] = utils.percentage(
                total_exits, tmp_data[path][pageview_idx]
            )

        total_row = [
            "Totals",
            totals['pageviews'],
            totals['unique_pageviews'],
            utils.average_duration(totals['duration'], totals['pageviews']),
            totals['entrances'],
            utils.percentage(totals['bounces'], totals['pageviews']),
            utils.percentage(totals['exits'], totals['pageviews']),
        ]
        return tmp_data.values() + [total_row]


    def _build_report_headers(self):
        return (
            'Page',
            'Pageviews',
            'Unique Pageviews',
            'Avg. Time on Page',
            'Entrances',
            'Bounce Rate',
            '% Exit',
        )

page_overview = PageOverviewReport.as_view()
