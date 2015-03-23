from django.core.urlresolvers import reverse

from djanalytics import models
from djanalytics.tests.base_chart_test import BaseChartTest


class TestPageVisit(BaseChartTest):

    def test_page_visit(self):
        for i in range(10):
            models.RequestEvent.objects.create(
                client=self.dja_client,
                ip_address='192.168.1.%s' % i,
                path='/home/',
                referrer='http://djanalytics.example.com/referrer/' if i % 2 == 0 else '',
            )
        for i in range(10):
            models.RequestEvent.objects.create(
                client=self.dja_client,
                ip_address='192.168.1.%s' % i,
                path='/path1/' if i % 2 == 0 else '/path2/',
                referrer='http://djanalytics.example.com/home/'
            )
        response = self.client.post(
            reverse('page_visit'),
            data = {
                'client': self.dja_client.uuid,
            }
        )
        self.assertEqual(response.status_code, 200)
        page_info = response.context['page_info']
        self.assertEqual(10, page_info['target_page']['visits'])
        self.assertEqual(5, page_info['parent_pages'][''])
        self.assertEqual(5, page_info['parent_pages']['http://djanalytics.example.com/referrer/'])
        children = dict(
            (page['path'], page['visits'])
            for page in page_info['child_pages']
        )
        self.assertEqual(5, children['/path1/'])
        self.assertEqual(5, children['/path2/'])
