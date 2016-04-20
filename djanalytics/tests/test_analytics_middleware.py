import mock

from django.conf import settings
from django.conf.urls import patterns, url
from django.http.response import HttpResponse
from django.test import TestCase
from django.test.utils import override_settings

from djanalytics import models

urlpatterns = [
    url(r'^$', lambda request: HttpResponse(status=204)),
    url(r'^exclude_me/should_not_report',
        lambda request: HttpResponse(status=204)
    ),
]
@override_settings(
    MIDDLEWARE_CLASSES=settings.MIDDLEWARE_CLASSES + [
            'djanalytics.middleware.AnalyticsMiddleware',
    ]
)
class TestAnalyticsMiddleware(TestCase):

    def setUp(self):
        super(TestAnalyticsMiddleware, self).setUp()
        self.dja_client = models.Client.objects.create(
            name='test',
            uuid='test'
        )
        models.Domain.objects.create(
            pattern='.*',
            client=self.dja_client
        )

    @override_settings(ROOT_URLCONF=__name__)
    def test_middleware(self):
        response = self.client.get('/')
        tracking_id = response.client.session['dja_tracking_id']
        tracking_user_id = response.cookies.get('dja_uuid').value
        self.assertIsNotNone(tracking_id)
        event = models.RequestEvent.objects.get(
            tracking_key=tracking_id,
            tracking_user_id=tracking_user_id
        )
        self.assertEqual(event.response_code, 204)
        response = self.client.get('/')
        self.assertEqual(
            models.RequestEvent.objects.filter(
                tracking_key=tracking_id,
                tracking_user_id=tracking_user_id
            ).count(),
            2
        )
        self.client.cookies.pop('sessionid')
        response = self.client.get('/')
        self.assertEqual(
            models.RequestEvent.objects.filter(
                tracking_user_id=tracking_user_id
            ).count(),
            3
        )

    def test_request_failure(self):
        response = self.client.get('/bogus')
        tracking_id = response.client.session['dja_tracking_id']
        self.assertIsNotNone(tracking_id)
        event = models.RequestEvent.objects.get(tracking_key=tracking_id)
        self.assertEqual(event.response_code, 404)

    @override_settings(ROOT_URLCONF=__name__)
    def test_path_filter(self):
        event_count = models.RequestEvent.objects.count()
        models.PathFilter.objects.create(
            client=self.dja_client,
            path_pattern='^/exclude_me/.*',
            include=False
        )
        response = self.client.get('/exclude_me/should_not_report')
        self.assertEqual(
            response.status_code, 204,
            'Expected 204 (no content) because path should be excluded. '
            'Got %s instead' % response.status_code
        )
        self.assertNotIn('dja_tracking_id', response.client.session)
        self.assertEquals(models.RequestEvent.objects.count(), event_count)

    def test_referrer(self):
        response = self.client.get('/info', HTTP_REFERER='/')
        tracking_id = response.client.session['dja_tracking_id']
        tracking_user_id = response.cookies.get('dja_uuid').value
        self.assertIsNotNone(tracking_id)
        event = models.RequestEvent.objects.get(
            tracking_key=tracking_id,
            tracking_user_id=tracking_user_id
        )
        self.assertEqual(event.response_code, 404)
        self.assertEqual(event.referrer, '/')

