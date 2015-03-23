import warnings
from mock import patch

from django.test import TestCase
from django.core.urlresolvers import reverse

from djanalytics import models


class TestCapture(TestCase):
    urls = 'djanalytics.tests.urls'

    def setUp(self):
        super(TestCapture, self).setUp()
        self.dja_client = models.Client.objects.create(
            name='testclient'
        )
        models.Domain.objects.create(
            name='djanalytics.example.com',
            client=self.dja_client
        )
        models.Domain.objects.create(
            name='djanalytics_too.example.com',
            client=self.dja_client
        )

    def test_capture_get(self):
        # first request
        response = self.client.get(
            reverse('dja_capture'),
            HTTP_USER_AGENT='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:29.0) '
                            'Gecko/20100101 Firefox/29.0',
            HTTP_REFERER='http://djanalytics_too.example.com:81',
            data={
                'dja_id': self.dja_client.uuid,
                'qs': 'query_key=query_value&another_query_key=another_query_value',
                'pth': '/',
                'sw': '800',
                'sh': '600'
            }
        )
        self.assertEqual(201, response.status_code)
        tracking_id = response.client.session['dja_tracking_id']
        tracking_user_id = response.cookies.get('dja_uuid').value
        event = models.RequestEvent.objects.get(
            tracking_key=tracking_id,
            tracking_user_id=tracking_user_id)
        self.assertEqual(
            event.query_string,
            'query_key=query_value&another_query_key=another_query_value'
        )
        self.assertEqual(event.path, '/')
        self.assertEqual(event.domain, 'djanalytics_too.example.com:81')
        self.assertEqual(event.protocol, 'http')
        self.assertEqual(event.screen_width, 800)
        self.assertEqual(event.screen_height, 600)

        # second request should have same tracking_id and tracking_user_id
        response = self.client.get(
            reverse('dja_capture'),
            HTTP_USER_AGENT='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:29.0) '
                            'Gecko/20100101 Firefox/29.0',
            HTTP_REFERER='http://djanalytics_too.example.com',
            data={
                'dja_id': self.dja_client.uuid,
                'qs': 'query_key=query_value&another_query_key=another_query_value',
                'pth': '/another_page',
                'rf': '/'
            }
        )
        self.assertEqual(202, response.status_code)
        self.assertEqual(
            models.RequestEvent.objects.filter(
                tracking_key=tracking_id,
                tracking_user_id=tracking_user_id
            ).count(),
            2
        )
        self.assertEqual(
            models.RequestEvent.objects.filter(
                tracking_key=tracking_id,
                tracking_user_id=tracking_user_id
            ).latest().referrer,
            '/'
        )

        # terminating session
        self.client.cookies.pop('sessionid')
        # third request should still have same tracking_user_id
        response = self.client.get(
            reverse('dja_capture'),
            HTTP_USER_AGENT='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:29.0) '
                            'Gecko/20100101 Firefox/29.0',
            HTTP_REFERER='http://djanalytics.example.com',
            data={
                'dja_id': self.dja_client.uuid,
                'qs': 'query_key=query_value&another_query_key=another_query_value',
                'pth': '/'
            }
        )
        self.assertEqual(202, response.status_code)
        self.assertEqual(
            models.RequestEvent.objects.filter(
                tracking_user_id=tracking_user_id
            ).count(),
            3
        )
        self.assertNotEqual(tracking_id, response.client.session['dja_tracking_id'],
            'New tracking id should be in session')

    def test_capture_get_tracking_ids_in_query(self):
        tracking_id = models.generate_uuid()
        tracking_user_id = models.generate_uuid()
        self.client.get(
            reverse('dja_capture'),
            HTTP_USER_AGENT='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:29.0) '
                            'Gecko/20100101 Firefox/29.0',
            HTTP_REFERER='http://djanalytics_too.example.com:81',
            data={
                'dja_id': self.dja_client.uuid,
                'qs': 'query_key=query_value&another_query_key=another_query_value',
                'pth': '/',
                'sw': '800',
                'sh': '600',
                'dti': tracking_id,
                'du': tracking_user_id
            }
        )
        self.assertTrue(
            models.RequestEvent.objects.filter(
                tracking_key=tracking_id,
                tracking_user_id=tracking_user_id
            ).exists()
        )

    def test_invalid_client_id(self):
        response = self.client.get(
            '%s?dja_id=%s' % (
                reverse('dja_capture'),
                'bogus'
            ),
            HTTP_REFERER='http://djanalytics.example.com',
        )
        self.assertEqual(403, response.status_code)
        self.assertNotIn('dja_tracking_id', response.client.session)
        self.assertEqual('Client not found', response.content)

    def test_invalid_domain_id(self):
        response = self.client.get(
            reverse('dja_capture'),
            HTTP_REFERER='http://bogus.example.com',
            data={
                'dja_id': self.dja_client.uuid,
                'qs': 'query_key=query_value&another_query_key=another_query_value',
                'pth': '/'
            }
        )
        self.assertEqual(403, response.status_code)
        self.assertNotIn('dja_tracking_id', response.client.session)
        self.assertEqual('Invalid domain for client', response.content)

    def test_filtered_ip(self):
        models.IPFilter.objects.create(
            client=self.dja_client,
            netmask='127.0.0.0/24',
            include=False,
        )
        response = self.client.get(
            reverse('dja_capture'),
            HTTP_USER_AGENT='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:29.0) '
                            'Gecko/20100101 Firefox/29.0',
            HTTP_REFERER='http://djanalytics.example.com',
            REMOTE_ADDR='127.0.0.1',
            data={
                'dja_id': self.dja_client.uuid,
                'qs': 'query_key=query_value&another_query_key=another_query_value',
                'pth': '/'
            }
        )
        self.assertEqual(
            204, response.status_code,
            'Expected 204 (no content) because ip should be excluded. '
            'Got %s instead' % response.status_code)
        self.assertNotIn('dja_tracking_id', response.client.session)

    def test_filtered_path(self):
        models.PathFilter.objects.create(
            client=self.dja_client,
            path_pattern='^/exclude_me/.*',
            include=False,
        )
        response = self.client.get(
            reverse('dja_capture'),
            HTTP_USER_AGENT='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:29.0) '
                            'Gecko/20100101 Firefox/29.0',
            HTTP_REFERER='http://djanalytics.example.com',
            REMOTE_ADDR='127.0.0.1',
            data={
                'dja_id': self.dja_client.uuid,
                'qs': 'query_key=query_value&another_query_key=another_query_value',
                'pth': '/exclude_me/should_not_report'
            }
        )
        self.assertEqual(204, response.status_code)
        self.assertNotIn(
            'dja_tracking_id', response.client.session,
            'Expected 204 (no content) because path should be excluded.'
            'Got %s instead' % response.status_code)

    def test_no_referrer(self):
        response = self.client.get(
            reverse('dja_capture'),
            HTTP_USER_AGENT='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:29.0) '
                            'Gecko/20100101 Firefox/29.0',
            data={
                'dja_id': self.dja_client.uuid,
                'qs': 'query_key=query_value&another_query_key=another_query_value',
                'pth': '/'
            }
        )
        self.assertEqual(
            403, response.status_code, 'Expected a FORBIDDEN (403) '
            'but got %s instead' % response.status_code
        )
        self.assertNotIn(
            'dja_tracking_id', response.client.session,
            'Expected 204 (no content) because path should be excluded.'
            'Got %s instead' % response.status_code)

    @patch('django.conf.settings.USE_X_FORWARDED_HOST', True)
    def test_x_forwarded_header(self):
        response = self.client.get(
            reverse('dja_capture'),
            HTTP_USER_AGENT='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:29.0) '
                            'Gecko/20100101 Firefox/29.0',
            HTTP_REFERER='http://djanalytics.example.com:81',
            HTTP_X_FORWARDED_FOR='192.168.254.254',
            REMOTE_ADDR='1.1.1.1',
            data={
                'dja_id': self.dja_client.uuid,
                'qs': 'query_key=query_value&another_query_key=another_query_value',
                'pth': '/'
            }
        )
        self.assertEqual(201, response.status_code)
        tracking_id = response.client.session['dja_tracking_id']
        tracking_user_id = response.cookies.get('dja_uuid').value
        event = models.RequestEvent.objects.get(
            tracking_key=tracking_id,
            tracking_user_id=tracking_user_id)
        self.assertEqual('192.168.254.254', event.ip_address)

    def test_domain_pattern_deprecated(self):
        models.Domain.objects.create(
            pattern="example.com",
            client=self.dja_client
        )
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")  # always trigger warnings
            response = self.client.get(
                reverse('dja_capture'),
                HTTP_REFERER='http://regex.example.com',
                data={
                    'dja_id': self.dja_client.uuid,
                    'qs': 'query_key=query_value',
                    'pth': '/'
                }
            )
            self.assertEqual(len(w), 1, "Expected 1 deprecation warning")
            warning = w[0]
            self.assertEqual(warning.category, DeprecationWarning)
            self.assertEqual(
                warning.message.message,
                "Use of domain patterns will be removed in a future version."
            )
        self.assertEqual(response.status_code, 201)

