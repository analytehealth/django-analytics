from django.test.testcases import TestCase

from djanalytics import models


class BaseChartTest(TestCase):

    urls = 'djanalytics.tests.urls'

    def setUp(self):
        super(BaseChartTest, self).setUp()
        self.dja_client = models.Client.objects.create(
            name='testclient'
        )
        self.domain = models.Domain.objects.create(
            pattern='djanalytics.example.com',
            client=self.dja_client
        )
