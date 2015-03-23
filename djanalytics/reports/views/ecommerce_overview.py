from django.db.models import Sum, Avg

from .base import DateRangeReportView
from djanalytics.reports.utils import format_date


class EcommerceOverviewReport(DateRangeReportView):
    report_name = "Ecommerce Overview"

    def _build_report_data(self):
        individual_days = self.visit_queryset().values(
            'visit_date'
        ).annotate(
            conversion_rate=Avg('conversion_count'),
            conversions=Sum('conversion_count')
        ).values(
            'visit_date', 'conversion_rate', 'conversions'
        ).order_by('visit_date')

        if not individual_days:
            return []

        total_data = self.visit_queryset().aggregate(
            conversion_rate=Avg('conversion_count'),
            conversions=Sum('conversion_count')
        )
        totals = [
            'Totals',
            total_data['conversions'],
            "%.2f%%" % (total_data['conversion_rate'] * 100)
        ]
        data = [
            [
                format_date(day['visit_date']),
                day['conversions'],
                "%.2f%%" % (day['conversion_rate'] * 100)
            ] for day in individual_days
        ]
        return data + [totals]

    def _build_report_headers(self):
        return ("Date", "Web Orders", "Conversion Rate")

ecommerce_overview = EcommerceOverviewReport.as_view()
