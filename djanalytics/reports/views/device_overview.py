from django.db.models import Count
from django.utils.datastructures import SortedDict

from djanalytics import models

from .base import DateRangeReportView
from djanalytics.reports.utils import format_date


class DeviceOverviewReport(DateRangeReportView):
    report_name = "Device Overview"
    DEVICE_TYPES = (
        models.DeviceType.DESKTOP,
        models.DeviceType.MOBILE,
        models.DeviceType.TABLET
    )

    def _build_report_data(self):
        tmp_data = SortedDict()
        totals = ['Totals'] + [0] * len(self.DEVICE_TYPES)

        visit_counts = self.visit_queryset().values(
            'visit_date',
            'device__device_type__code',
        ).filter(
            device__device_type__code__in=self.DEVICE_TYPES
        ).annotate(Count('device__device_type')).order_by('visit_date')

        if not visit_counts:
            return []

        for visit in visit_counts:
            device_type = visit['device__device_type__code']
            date_obj = visit['visit_date']
            if date_obj not in tmp_data:
                date_str = format_date(date_obj)
                tmp_data[date_obj] = [date_str] + ([0] * len(self.DEVICE_TYPES))
            index = self.DEVICE_TYPES.index(device_type) + 1
            tmp_data[date_obj][index] += visit['device__device_type__count']
            totals[index] += visit['device__device_type__count']

        return tmp_data.values() + [totals]

    def _build_report_headers(self):
        return ["Date"] + [dt.capitalize() for dt in self.DEVICE_TYPES]

device_overview = DeviceOverviewReport.as_view()
