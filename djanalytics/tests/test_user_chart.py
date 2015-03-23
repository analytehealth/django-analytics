import datetime

from django.utils import timezone

from djanalytics import models
from djanalytics.tests.base_chart_test import BaseChartTest
from django.core.urlresolvers import reverse


class TestUserChart(BaseChartTest):

    def test_user_chart(self):
        created_date = timezone.now() - datetime.timedelta(days=3)
        for i in range(3):
            re = models.RequestEvent.objects.create(
                ip_address = '1.1.1.1',
                protocol = 'http',
                domain = 'example.com',
                path = '/',
                method = 'GET',
                response_code = 200,
                client = self.dja_client,
            )
            re.created = created_date
            re.save()
            models.RequestEvent.objects.create(
                client=re.client,
                ip_address=re.ip_address,
                tracking_user_id=re.tracking_user_id
            )
        re = models.RequestEvent.objects.create(
            ip_address = '1.1.1.1',
            protocol = 'http',
            domain = 'example.com',
            path = '/',
            method = 'GET',
            response_code = 200,
            client = self.dja_client,
        )
        # ensure this session was created before chart date range
        re.created = timezone.now() - datetime.timedelta(days=7)
        re.save()
        models.RequestEvent.objects.create(
            client=re.client,
            ip_address=re.ip_address,
            tracking_user_id=re.tracking_user_id
        )
        response = self.client.post(
            reverse('user_chart'),
            data = {
                'start_date': (
                    datetime.datetime.now() - datetime.timedelta(days=5)
                ).strftime('%Y-%m-%d'),
                'client': self.dja_client.uuid,
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(7, len(response.context['chart'].data_source.data))
        # first entry in the chart is header data
        for i in range(6):
            chart_date, count = response.context['chart'].data_source.data[i + 1]
            if count > 0:
                self.assertEqual(i, 2)
                self.assertEqual(chart_date, created_date.strftime('%Y-%m-%d'))
