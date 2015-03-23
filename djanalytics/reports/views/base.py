from django.views.generic import FormView
from django.http import HttpResponse
from django.utils.text import slugify
from tablib.core import Dataset

from djanalytics import models
from djanalytics.reports.forms import DateRangeReportForm


class DateRangeReportView(FormView):
    ASCENDING = '0'
    DESCENDING = '1'

    template_name = 'djanalytics/reports/daterange_report.html'
    form_class = DateRangeReportForm
    exclude_bots = True
    report_name = ""
    default_sort = None

    def __init__(self, *args, **kwargs):
        super(DateRangeReportView, self).__init__(*args, **kwargs)
        self.client = None
        self.web_property = None
        self.start_date = None
        self.end_date = None

    def form_valid(self, form):
        if form.cleaned_data.get('start_date'):
            self.start_date = form.cleaned_data['start_date']
        if form.cleaned_data.get('end_date'):
            self.end_date = form.cleaned_data['end_date']
        self.web_property = form.cleaned_data['web_property']
        self.client = form.cleaned_data['client']
        if form.cleaned_data['format'] == 'csv':
            return self.render_csv_report()
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(DateRangeReportView, self).get_context_data(**kwargs)
        context.update(
            report_name=self.report_name,
            data=self._build_report_data(),
            headers=self._build_report_headers(),
            sort_column=self._build_report_headers().index(
                self.default_sort[0]
            ) if self.default_sort else None,
            sort_order=self.default_sort[1] if self.default_sort else None,
        )
        return context

    def visit_queryset(self):
        if self.client:
            web_properties = models.WebProperty.objects.filter(
                domain__client=self.client
            ).distinct()
            base_qs = models.Visit.objects.filter(
                web_property__in=web_properties
            )
        else:
            base_qs = models.Visit.objects.filter(
                web_property=self.web_property
            )
        if self.start_date:
            base_qs = base_qs.filter(visit_date__gte=self.start_date)
        if self.end_date:
            base_qs = base_qs.filter(visit_date__lte=self.end_date)
        if self.exclude_bots:
            base_qs = base_qs.exclude(
                device__device_type__code=models.DeviceType.BOT
            )
        return base_qs

    def render_csv_report(self):
        dataset = Dataset(
            *self._build_report_data(),
            headers=self._build_report_headers()
        )
        response = HttpResponse(
            dataset.csv, 'text/csv', None, 'text/csv; charset=utf-8',
        )
        filename = self.get_filename().encode('utf-8')
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response

    def _build_report_data(self):
        raise NotImplementedError

    def _build_report_headers(self):
        raise NotImplementedError

    def get_filename(self):
        parts = [slugify(unicode(self.report_name))]
        if self.start_date:
            parts.append(self.start_date.strftime("%m.%d.%Y"))
        if self.end_date:
            parts.append(self.end_date.strftime("%m.%d.%Y"))
        return "-".join(parts) + ".csv"
