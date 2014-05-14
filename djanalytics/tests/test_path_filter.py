from django.test import TestCase

from djanalytics import models


class TestPathFilter(TestCase):

    def setUp(self):
        super(TestPathFilter, self).setUp()
        self.client = models.Client.objects.create(
            name='test_client'
        )

    def test_include(self):
        path_filter = models.PathFilter.objects.create(
            client=self.client,
            include=True,
            path_pattern='^prefix-.*'
        )
        self.assertTrue(path_filter.valid('prefix-this/should/be/valid'))
        self.assertFalse(path_filter.valid('this/should/not/be'))

    def test_exclude(self):
        path_filter = models.PathFilter.objects.create(
            client=self.client,
            include=False,
            path_pattern='^prefix-.*'
        )
        self.assertFalse(path_filter.valid('prefix-this/should/not/be/valid'))
        self.assertTrue(path_filter.valid('this/should/be'))
