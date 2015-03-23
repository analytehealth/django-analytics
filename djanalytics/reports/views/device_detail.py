from collections import defaultdict

from django.db.models import Count

from .base import DateRangeReportView
from djanalytics.models import DeviceType
from djanalytics.reports import utils
from djanalytics.reports.forms import DeviceDetailReportForm


class BaseDeviceReport(DateRangeReportView):
    def _device_group(self, device):
        raise NotImplementedError

    def _build_report_data(self):
        data = []
        tmp_data = {}
        totals = defaultdict(int)
        visits = self.visit_queryset().annotate(
            page_count=Count('pages'),
            visit_count=Count('visitor__visit')
        ).select_related('device')
        for visit in visits:
            device_group = self._device_group(visit.device)
            if device_group not in tmp_data:
                tmp_data[device_group] = defaultdict(int)
            tmp_data[device_group]['visits'] += 1
            tmp_data[device_group]['pageviews'] += visit.page_count
            tmp_data[device_group]['duration'] += visit.duration or 0
            tmp_data[device_group]['conversions'] += visit.conversion_count
            if visit.page_count == 1:
                tmp_data[device_group]['bounces'] += 1
            if visit.visit_count > 1:
                tmp_data[device_group]['returning_visits'] += 1
            else:
                tmp_data[device_group]['new_visits'] += 1

        for device_group, visit_data in tmp_data.iteritems():
            for key, value in visit_data.items():
                totals[key] += value

            data.append(
                self._build_row(visit_data, *device_group)
            )

        if data:
            # sort the report by visits
            visit_idx = self._build_report_headers().index("Visits")
            data.sort(key=lambda x: x[visit_idx], reverse=True)
            data.append(self._build_row(totals, "Totals", ""))

        return data

    def _build_report_headers(self):
        """ This returns all but the first 2 headers, provided by subclasses """
        return (
            "Visits",
            "New Visits",
            "Returning Visits",
            "Pageviews",
            "Bounce Rate",
            "Pages/Session",
            "Avg. Session Duration",
            "Web Orders",
            "Web Conversion Rate",
        )

    def _build_row(self, datadict, *first_columns):
        bounce_rate = utils.percentage(
            datadict['bounces'], datadict['visits']
        )
        pages_per_session = utils.average(
            datadict['pageviews'], datadict['visits']
        )
        avg_duration = utils.average_duration(
            datadict['duration'], datadict['visits']
        )
        conversion_rate = utils.percentage(
            datadict['conversions'], datadict['visits']
        )

        return first_columns + (
            datadict['visits'],
            datadict['new_visits'],
            datadict['returning_visits'],
            datadict['pageviews'],
            bounce_rate,
            pages_per_session,
            avg_duration,
            datadict['conversions'],
            conversion_rate,
        )

class DeviceDetailReport(BaseDeviceReport):
    form_class = DeviceDetailReportForm
    exclude_bots = False

    def __init__(self, *args, **kwargs):
        super(DeviceDetailReport, self).__init__(*args, **kwargs)
        self.device_type = None

    def form_valid(self, form):
        self.device_type = form.cleaned_data['device_type']
        return super(DeviceDetailReport, self).form_valid(form)

    def visit_queryset(self):
        base_qs = super(DeviceDetailReport, self).visit_queryset()
        base_qs = base_qs.filter(device__device_type=self.device_type)
        return base_qs

    def _device_group(self, device):
        return device.name, device.resolution

    def _build_report_headers(self):
        return (
            "Device Info",
            "Device Resolution",
        ) + super(DeviceDetailReport, self)._build_report_headers()

    @property
    def report_name(self):
        if self.device_type:
            return "Device Detail - %s" % self.device_type.name
        else:
            return "Device Detail"


class BrowserDetailReport(BaseDeviceReport):
    report_name = "Browser Detail"

    def _device_group(self, device):
        return device.browser, device.os

    def _build_report_headers(self):
        return (
            "Browser",
            "OS",
        ) + super(BrowserDetailReport, self)._build_report_headers()

device_detail = DeviceDetailReport.as_view()
browser_detail = BrowserDetailReport.as_view()
