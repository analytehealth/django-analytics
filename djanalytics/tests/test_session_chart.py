import datetime

from django.core.urlresolvers import reverse
from django.test.testcases import TestCase

from djanalytics import models


class TestSessionChart(TestCase):

    urls = 'djanalytics.charts.urls'

    def setUp(self):
        super(TestSessionChart, self).setUp()
        self.dja_client = models.Client.objects.create(
            name='testclient'
        )
        models.Domain.objects.create(
            pattern='djanalytics.example.com',
            client=self.dja_client
        )

    def test_get(self):
        models.RequestEvent.objects.create(
            ip_address = '1.1.1.1',
            protocol = 'http',
            domain = 'example.com',
            path = '/',
            method = 'GET',
            response_code = 200,
            client = self.dja_client,
            created = datetime.datetime.now() - datetime.timedelta(days=3)
        )
        response = self.client.get(
            reverse('session_chart', urlconf='djanalytics.charts.urls'),
            data = {
                'start_date': (
                    datetime.datetime.now() - datetime.timedelta(days=5)
                ).strftime('%Y-%m-%d'),
                'client_id': self.dja_client.uuid,
            }
        )
        self.assertEqual(response.status_code, 200)
