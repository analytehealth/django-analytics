import datetime

from django.core.urlresolvers import reverse
from django.test.testcases import TestCase

from djanalytics import models

class TestExitPage(TestCase):

    urls = 'djanalytics.charts.urls'

    def setUp(self):
        super(TestExitPage, self).setUp()
        self.dja_client = models.Client.objects.create(
            name='testclient'
        )
        models.Domain.objects.create(
            pattern='djanalytics.example.com',
            client=self.dja_client
        )

    def test_exit_page(self):
        for i in range(3):
            first_page = models.RequestEvent.objects.create(
                client=self.dja_client,
                path='/',
                ip_address='192.168.1.%s' % i
            )
            models.RequestEvent.objects.create(
                client=self.dja_client,
                path='/last_page',
                ip_address=first_page.ip_address,
                tracking_key=first_page.tracking_key,
                tracking_user_id=first_page.tracking_user_id
            )
        response = self.client.get(
            reverse('exit_page', urlconf='djanalytics.charts.urls'),
            data = {
                'client_id': self.dja_client.uuid,
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(3, response.context['exit_page_data']['/last_page'])

    def test_session_out_of_date_range(self):
        for i in range(3):
            first_page = models.RequestEvent.objects.create(
                client=self.dja_client,
                path='/',
                ip_address='192.168.1.%s' % i
            )
            models.RequestEvent.objects.create(
                client=self.dja_client,
                path='/last_page',
                ip_address=first_page.ip_address,
                tracking_key=first_page.tracking_key,
                tracking_user_id=first_page.tracking_user_id
            )
        first_page = models.RequestEvent.objects.create(
                client=self.dja_client,
                path='/',
                ip_address='192.168.1.%s' % i,
        )
        first_page.created = datetime.datetime.now() - datetime.timedelta(days=14)
        first_page.save()
        models.RequestEvent.objects.create(
            client=self.dja_client,
            path='/last_page',
            ip_address=first_page.ip_address,
            tracking_key=first_page.tracking_key,
            tracking_user_id=first_page.tracking_user_id,
            created=datetime.datetime.now()
        )
        response = self.client.get(
            reverse('exit_page', urlconf='djanalytics.charts.urls'),
            data = {
                'client_id': self.dja_client.uuid,
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(3, response.context['exit_page_data']['/last_page'])
