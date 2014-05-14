from django.test import TestCase

from djanalytics import models


class TestClient(TestCase):

    def setUp(self):
        super(TestClient, self).setUp()
        self.client = models.Client.objects.create(name='test_client')

    def test_no_ip_filters(self):
        self.assertTrue(self.client.ip_valid('192.168.1.1'))
        self.assertTrue(self.client.ip_valid('10.1.1.1'))

    def test_no_path_filters(self):
        self.assertTrue(self.client.path_valid('/any/old/thing'))
        self.assertTrue(self.client.path_valid('/will_do'))

    def test_ip_filter(self):
        '''
        This sets up a series of rules that says allow everything on
        the subnets 192.168.1.x and 192.168.2.x, but exclude
        either 192.168.1.199 or 192.168.1.202
        '''
        for include, netmask in (
            (True, '192.168.1.0/24'),
            (True, '192.168.2.0/24'),
            (False, '192.168.1.199'),
            (False, '192.168.2.202'),
        ):
            models.IPFilter.objects.create(
                client=self.client,
                include=include,
                netmask=netmask
            )
        self.assertTrue(self.client.ip_valid('192.168.1.1'))
        self.assertTrue(self.client.ip_valid('192.168.2.1'))
        self.assertFalse(self.client.ip_valid('192.168.1.199'))
        self.assertFalse(self.client.ip_valid('192.168.2.202'))
        self.assertFalse(self.client.ip_valid('10.1.1.1'))

    def test_ip_filter_excludes(self):
        for include, netmask in (
            (False, '192.168.1.0/24'),
            (False, '192.168.2.0/24'),
        ):
            models.IPFilter.objects.create(
                client=self.client,
                include=include,
                netmask=netmask
            )
        self.assertFalse(self.client.ip_valid('192.168.1.1'))
        self.assertFalse(self.client.ip_valid('192.168.2.101'))
        self.assertTrue(self.client.ip_valid('192.168.3.201'))

    def test_path_filter(self):
        for include, path_pattern in (
            (True, '^ok_prefix/.*'),
            (True, '^.*ok_postfix$'),
            (False, '.*not-ok.*'),
            (False, '.*also_not.*'),
        ):
            models.PathFilter.objects.create(
                client=self.client,
                include=include,
                path_pattern=path_pattern
            )
        self.assertTrue(self.client.path_valid('ok_prefix/works'))
        self.assertTrue(self.client.path_valid('also/this/ok_postfix'))
        self.assertFalse(self.client.path_valid('not-ok/to/use'))
        self.assertFalse(self.client.path_valid('use/not-ok/'))
        self.assertFalse(self.client.path_valid('still/also_not'))
