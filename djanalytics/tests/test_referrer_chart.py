from djanalytics.tests.base_chart_test import BaseChartTest
from djanalytics import models
from django.core.urlresolvers import reverse


class TestReferrerChart(BaseChartTest):

    def test_referrer(self):
        for i in range(3):
            models.RequestEvent.objects.create(
                client=self.dja_client,
                ip_address='1.1.1.%s' % i,
                referrer='http://%s.example.com' % i
            )
            if i == 0:
                # verifying that query params are ignored
                models.RequestEvent.objects.create(
                    client=self.dja_client,
                    ip_address='1.1.1.%s' % i,
                    referrer='http://%s.example.com/?foo=bar' % i
                )
        # one request with referrer from analytics domain
        models.RequestEvent.objects.create(
            client=self.dja_client,
            ip_address='1.1.1.77',
            referrer='http://%s/home/' % self.domain.pattern
        )
        response = self.client.post(
            reverse('referrer'),
            data={'client': self.dja_client.uuid}
        )
        self.assertEquals(response.status_code, 200)
        referrer_data = response.context['referrer_data']
        self.assertEquals(len(referrer_data), 3)
        for i in range(3):
            expected = 1 if i != 0 else 2
            self.assertEquals(
                referrer_data['http://%s.example.com/' % i], expected
            )
