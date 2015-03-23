import re

from django.test.testcases import TestCase

from djanalytics import models
from django.core.urlresolvers import reverse

class TestDjanalyticsJs(TestCase):
    urls = 'djanalytics.tests.urls'

    def setUp(self):
        super(TestDjanalyticsJs, self).setUp()
        self.dja_client = models.Client.objects.create(
            name='testclient'
        )
        models.Domain.objects.create(
            pattern='djanalytics.example.com',
            client=self.dja_client
        )
        models.Domain.objects.create(
            pattern='djanalytics_too.example.com',
            client=self.dja_client
        )
        self.uuid_regex = re.compile(
            '^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$'
        )

    def test_djanalytics_js_get(self):
        response = self.client.get(
            reverse('djanalytics_js'),
            HTTP_REFERER='http://djanalytics_too.example.com',
            data={
                'dja_id': self.dja_client.uuid,
            }
        )
        self.assertEqual(200, response.status_code)
        self.assertTrue(self.uuid_regex.match(response.context['uuid']))
        self.assertTrue(self.uuid_regex.match(response.context['tracking_id']))
        self.assertEqual(response.context['domain'], '.example.com')
        self.assertEqual(
            response.context['capture_img_url'],
            reverse('dja_capture')
        )
        self.assertEqual(response.context['dja_id'], self.dja_client.uuid)

    def test_invalid_client(self):
        response = self.client.get(
            reverse('djanalytics_js'),
            HTTP_REFERER='http://djanalytics_too.example.com',
            data={
                'dja_id': 'bogus',
            }
        )
        self.assertEqual(200, response.status_code)
        self.assertTrue(self.uuid_regex.match(response.context['uuid']))
        self.assertTrue(self.uuid_regex.match(response.context['tracking_id']))
        self.assertEqual(response.context['domain'], '.example.com')
        self.assertEqual(
            response.context['capture_img_url'],
            reverse('dja_capture')
        )
        self.assertEqual(response.context['dja_id'], 'bogus')
