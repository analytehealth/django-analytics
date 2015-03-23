from collections import defaultdict

from django.db.models import Count
from django.utils.datastructures import SortedDict

from .base import DateRangeReportView
from djanalytics.reports import utils


class AudienceOverviewReport(DateRangeReportView):
    report_name = "Audience Overview"

    def _build_report_data(self):
        data = []
        tmp_data = SortedDict()
        totals = defaultdict(int)

        visits = self.visit_queryset().annotate(
            page_count=Count('pages'),
            visit_count=Count('visitor__visit')
        ).values(
            'visit_date', 'page_count', 'visit_count', 'duration'
        ).order_by('visit_date')
        for visit in visits:
            # ideally this would be done in the database
            # but grouping really isn't a thing Django does well
            date = visit["visit_date"]
            if date not in tmp_data:
                tmp_data[date] = defaultdict(int)
            tmp_data[date]['visits'] += 1
            tmp_data[date]['pageviews'] += visit['page_count']
            tmp_data[date]['duration'] += visit['duration'] or 0
            if visit['page_count'] == 1:
                tmp_data[date]['bounces'] += 1
            if visit['visit_count'] > 1:
                tmp_data[date]['returning_visits'] += 1
            else:
                tmp_data[date]['new_visits'] += 1
        for visit_date, visit_data in tmp_data.iteritems():
            for key, value in visit_data.items():
                totals[key] += value

            date_label = utils.format_date(visit_date)
            data.append(self._build_row(visit_data, date_label))
        if data:
            data.append(self._build_row(totals, "Totals"))

        return data

    def _build_report_headers(self):
        return (
            "Date",
            "Visits",
            "New Visits",
            "Returning Visits",
            "Pageviews",
            "Bounce Rate",
            "Pages/Session",
            "Avg. Session Duration",
        )

    def _build_row(self, datadict, first_column):
        bounce_rate = utils.percentage(
            datadict['bounces'], datadict['visits']
        )
        pages_per_session = utils.average(
            datadict['pageviews'], datadict['visits']
        )
        avg_duration = utils.average_duration(
            datadict['duration'], datadict['visits']
        )

        return (
            first_column,
            datadict['visits'],
            datadict['new_visits'],
            datadict['returning_visits'],
            datadict['pageviews'],
            bounce_rate,
            pages_per_session,
            avg_duration,
        )

audience_overview = AudienceOverviewReport.as_view()
