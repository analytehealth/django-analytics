from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings

from djanalytics import models


@override_settings(
    MIDDLEWARE_CLASSES=settings.MIDDLEWARE_CLASSES + [
        'djanalytics.middleware.CrossDomainMiddleware',
    ]
)
class TestCrossDomainMiddleware(TestCase):

    def setUp(self):
        super(TestCrossDomainMiddleware, self).setUp()
        self.dja_client = models.Client.objects.create(
            name='test',
            uuid='test'
        )
        models.Domain.objects.create(
            pattern='.*',
            client=self.dja_client
        )

    def test_get(self):
        uuid = models.generate_uuid()
        tracking_id = models.generate_uuid()
        self.client.get(
            '/', 
            data={
                'dja_uuid': uuid,
                'dja_tracking_id': tracking_id,
                'dja_id': self.dja_client.uuid,
            }
        )
        uuid_cookie = self.client.cookies.pop('dja_uuid')
        self.assertEqual(uuid_cookie.value, uuid)

        tracking_id_cookie = self.client.cookies.pop('dti')
        self.assertEqual(tracking_id_cookie.value, tracking_id)

    def test_post(self):
        uuid = models.generate_uuid()
        tracking_id = models.generate_uuid()
        self.client.post(
            '/', 
            data={
                'dja_uuid': uuid,
                'dja_tracking_id': tracking_id,
                'dja_id': self.dja_client.uuid,
            }
        )
        uuid_cookie = self.client.cookies.pop('dja_uuid')
        self.assertEqual(uuid_cookie.value, uuid)

        tracking_id_cookie = self.client.cookies.pop('dti')
        self.assertEqual(tracking_id_cookie.value, tracking_id)

    def test_bad_domain(self):
        models.Domain.objects.update(pattern='ex.com')
        uuid = models.generate_uuid()
        tracking_id = models.generate_uuid()
        self.client.post(
            '/', 
            data={
                'dja_uuid': uuid,
                'dja_tracking_id': tracking_id,
                'dja_id': self.dja_client.uuid,
            },
            HTTP_REFERRER='example.com'
        )
        with self.assertRaises(KeyError):
            self.client.cookies.pop('dja_uuid')
        
        with self.assertRaises(KeyError):
            self.client.cookies.pop('dti')
