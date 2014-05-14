from django.test import TestCase

from djanalytics import models


class TestIPFilter(TestCase):

    def setUp(self):
        super(TestIPFilter, self).setUp()
        self.client = models.Client.objects.create(
            name='test_client'
        )

    def test_include(self):
        ipfilter = models.IPFilter.objects.create(
            client=self.client,
            include=True,
            netmask='192.168.0.0/16'
        )
        self.assertTrue(ipfilter.valid('192.168.1.1'))
        self.assertFalse(ipfilter.valid('10.1.1.1'))

    def test_exclude(self):
        # to exclude an ip address range, create an
        # IPFilter with include=False
        ipfilter = models.IPFilter.objects.create(
            client=self.client,
            include=False,
            netmask='192.168.0.0/16'
        )
        self.assertFalse(ipfilter.valid('192.168.1.1'))
        self.assertTrue(ipfilter.valid('10.1.1.1'))
