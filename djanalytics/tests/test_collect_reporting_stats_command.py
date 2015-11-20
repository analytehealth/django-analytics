# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, date
from mock import Mock
from os import path

from django.test.testcases import TestCase

from freezegun.api import freeze_time

from djanalytics import models
from djanalytics.management.commands.collect_reporting_stats import Command


class TestCollectReportingStatsCommand(TestCase):

    def setUp(self):
        self.dja_client = models.Client.objects.create(
            name='testclient'
        )
        self.dja_property = models.WebProperty.objects.create(
            name='Djanalytics',
            slug='djanalytics',
        )
        self.dja_domain = models.Domain.objects.create(
            name='djanalytics.example.com',
            client=self.dja_client,
            web_property=self.dja_property,
        )
        funnel_type, created = models.PageType.objects.get_or_create(
            code=models.PageType.FUNNEL
        )
        models.PagePattern.objects.create(
            name='Funnel',
            code='funnel',
            page_type=funnel_type,
            pattern='/page_two',
            display_path='/page_two',
            client=self.dja_client,
        )
        models.Page.objects.create(
            path='/page_two',
            page_type=funnel_type,
            client=self.dja_client
        )
        checkout_type, created = models.PageType.objects.get_or_create(
            code=models.PageType.CONVERSION,
            defaults={
                'name': 'Checkout'
            }
        )
        models.PagePattern.objects.create(
            name='Conversion',
            code='conversion',
            page_type=checkout_type,
            pattern='/page_three/(\d+)',
            display_path='/page_three',
            client=self.dja_client,
        )
        self.page = models.Page.objects.create(
            path='/page_three/123/',
            page_type=checkout_type,
            client=self.dja_client,
        )

    def test_collect(self):
        tracking_key = models.generate_uuid()
        tracking_user_id = models.generate_uuid()
        right_now = datetime.now()
        for cnt, page in enumerate(['/page_three/123/', '/page_two', '/page_one']):
            re = models.RequestEvent.objects.create(
                ip_address='127.0.0.1',
                user_agent='Mozilla/5.0 (Windows NT 5.1; rv:30.0) Gecko/20100101 Firefox/30.0',
                tracking_key=tracking_key,
                tracking_user_id=tracking_user_id,
                protocol='http',
                domain='djanalytics.example.com',
                path=page,
                query_string='',
                method='GET',
                client=self.dja_client,
            )
            right_now = right_now - timedelta(seconds=(cnt*2))
            re.created=right_now
            re.save()
        command = Command()
        command.stdout = Mock()
        command.handle()
        page_visits = models.PageVisit.objects.order_by('request_event__created')
        self.assertEqual(4, page_visits[0].duration)
        self.assertEqual(2, page_visits[1].duration)
        self.assertEqual(None, page_visits[2].duration)
        visit = models.Visit.objects.get()
        self.assertEqual(6, visit.duration)
        self.assertEqual(1, visit.conversion_count)
        self.assertEqual(visit.last_page.path, '/page_three/123/')
        self.assertEqual(visit.first_page.path, '/page_one')
  
    def test_collect_no_funnel(self):
        # a funnel page MUST precede a conversion page
        # this prevents "order confirmation" type pages from being
        # counted as conversions
        tracking_key = models.generate_uuid()
        tracking_user_id = models.generate_uuid()
        right_now = datetime.now()
        for cnt, page in enumerate(['/page_three/123/', '/page_one']):
            re = models.RequestEvent.objects.create(
                ip_address='127.0.0.1',
                user_agent='Mozilla/5.0 (Windows NT 5.1; rv:30.0) Gecko/20100101 Firefox/30.0',
                tracking_key=tracking_key,
                tracking_user_id=tracking_user_id,
                protocol='http',
                domain='djanalytics.example.com',
                path=page,
                query_string='',
                method='GET',
                client=self.dja_client,
            )
            right_now = right_now - timedelta(seconds=(cnt*2))
            re.created=right_now
            re.save()
        command = Command()
        command.stdout = Mock()
        command.handle()
        page_visits = models.PageVisit.objects.order_by('request_event__created')
        self.assertEqual(2, page_visits[0].duration)
        self.assertEqual(None, page_visits[1].duration)
        visit = models.Visit.objects.get()
        self.assertEqual(2, visit.duration)
        self.assertEqual(0, visit.conversion_count)
        self.assertEqual(visit.last_page.path, '/page_three/123/')
        self.assertEqual(visit.first_page.path, '/page_one')
 
    def test_collect_non_ascii_user_agent(self):
        tracking_key = models.generate_uuid()
        tracking_user_id = models.generate_uuid()
        f = open(
            path.join(
                path.dirname(path.abspath(__file__)),
                'unicode_user_agent.txt'
            )
        )
        user_agent = f.read()
        f.close()
        models.RequestEvent.objects.create(
            ip_address='127.0.0.1',
            user_agent=user_agent,
            tracking_key=tracking_key,
            tracking_user_id=tracking_user_id,
            protocol='http',
            domain='djanalytics.example.com',
            path='page',
            query_string='',
            method='GET',
            client=self.dja_client,
        )
        command = Command()
        command.stdout = Mock()
        try:
            command.handle()
        except UnicodeEncodeError:
            self.fail()
  
    def test_max_age(self):
        freezer = freeze_time(datetime.now() - timedelta(days=15))
        freezer.start()
        device = models.Device.objects.create(
            os='OS',
            os_version='1.0',
            browser='Browser',
            browser_version='1.0',
            device=''
        )
        visitor = models.Visitor.objects.create(
            uuid=models.generate_uuid(),
        )
        visit = models.Visit.objects.create(
            uuid=models.generate_uuid(),
            visitor=visitor,
            device=device,
            web_property=self.dja_property,
            first_page=self.page,
            visit_date=date.today(),
        )
        re = models.RequestEvent.objects.create(
            ip_address='127.0.0.1',
            user_agent='Mozilla/5.0 (Windows NT 5.1; rv:30.0) Gecko/20100101 Firefox/30.0',
            protocol='http',
            domain='invalid.com',
            path='/foo',
            query_string='',
            method='GET',
            client=self.dja_client,
            tracking_user_id=visitor.uuid,
            tracking_key=visit.uuid,
            created=(datetime.now() - timedelta(seconds=10))
        )
        models.RequestEvent.objects.create(
            ip_address='127.0.0.1',
            user_agent='Mozilla/5.0 (Windows NT 5.1; rv:30.0) Gecko/20100101 Firefox/30.0',
            protocol='http',
            domain='invalid.com',
            path='/foo',
            query_string='',
            method='GET',
            client=self.dja_client,
            tracking_user_id=visitor.uuid,
            tracking_key=visit.uuid,
        )
        models.PageVisit.objects.create(
            page=self.page,
            visit=visit,
            request_event=re
        )
        freezer.stop()
        command = Command()
        command.stdout = Mock()
        command.handle(
            start=(datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d'),
            max_age=10
        )
        self.assertEqual(
            1, models.PageVisit.objects.count(),
            'should not have created a page visit for the second request event'
        )
        self.assertIsNone(
            models.PageVisit.objects.get().duration,
            'should not have set a duration on page visit'
        )
        visit = models.Visit.objects.get()
        self.assertIsNone(
            visit.last_page,
            'should not have set a last page on visit'
        )
        self.assertIsNone(
            visit.duration,
            'should not have set a duration on visit'
        )
        self.assertEqual(
            0,
            visit.conversion_count,
            'conversion_count should 0, not %s' % visit.conversion_count
        )
