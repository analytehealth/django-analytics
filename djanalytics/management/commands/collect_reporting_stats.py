import re

from collections import defaultdict, namedtuple
from datetime import datetime, timedelta
from hashlib import md5
from optparse import make_option

from user_agents import parse

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import reset_queries
from django.db.models.aggregates import Sum, Count
from django.utils.dateparse import parse_date

from djanalytics import models

class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option(
            '-s', '--start', type='string',
            help='Beginning date for request events. If not provided, '
                 'request events from the beginning of time will be '
                 'selected.'
        ),
        make_option(
            '-e', '--end', type='string',
            help='End date for request events. If not provided, '
                 'up to the most recent request event will be selected.'
        ),
        make_option(
            '-a', '--max-age', type='int', dest='max_age', default=30,
            help='Max number of days in the past to look for Visit and '
                 'PageVisit objects. Default is 30.'
        )
    )

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.device_type_cache = {}

    def handle(self, start=None, end=None, max_age=30, **options):
        self.max_age = max_age

        self.create_page_visits(start, end)
        self.calculate_page_durations()
        self.collect_visit_data()

    def create_page_visits(self, start, end):
        page_pattern_cache = defaultdict(list)
        for page_pattern in models.PagePattern.objects.order_by('client'):
            page_pattern_cache[page_pattern.client.pk].append(
                namedtuple('CachedPagePattern', 'pattern,page_type')(
                    re.compile(page_pattern.pattern, flags=re.IGNORECASE),
                    page_pattern.page_type
                )
            )
        web_property_cache = {
            domain.name: domain.web_property
            for domain in models.Domain.objects.select_related()
        }
        device_cache = {}
        visitor_cache = {}
        visit_cache = {}
        page_cache = {}
        created_page_visits = []
        query_dict = {
            'pagevisit': None,
            'domain__in': web_property_cache.keys(),
        }
        if start:
            start = parse_date(start)
            query_dict['created__gte'] = start
        if end:
            end = parse_date(end)
            query_dict['created__lte'] = end

        query = models.RequestEvent.objects.filter(
            **query_dict
        ).select_related().order_by('tracking_user_id', 'created')
        total_events = query.count()
        query = query.iterator()
        self.stdout.write(
            'Processing %s RequestEvents - Start: %s\tEnd: %s\n' % (
                total_events,
                start.strftime('%m/%d/%Y') if start else 'None',
                end.strftime('%m/%d/%Y') if end else 'None'
            )
        )
        for cnt, request_event in enumerate(query):
            if cnt % 1000 == 0:
                self.stdout.write('Processed %s of %s\n' % (cnt, total_events))
                # in DEBUG mode, django holds on to all database queries
                # this can cause memory issues in pre-production environments
                # with large sets of data
                if settings.DEBUG:
                    reset_queries()
            if cnt % 20000 == 0:
                self.stdout.write('Clearing caches')
                visit_cache = {}
                visitor_cache = {}
                page_cache = {}
                device_cache = {}
                models.PageVisit.objects.bulk_create(
                    created_page_visits
                )
                created_page_visits = []
            user_agent_md5 = device = None
            if request_event.user_agent:
                user_agent_md5 = md5(request_event.user_agent.encode('utf-8')).hexdigest()
                device = device_cache.get(user_agent_md5)
            if user_agent_md5 and not device:
                user_agent = parse(request_event.user_agent)
                device, created = models.Device.objects.get_or_create(
                    user_agent_md5=user_agent_md5,
                    defaults={
                        'user_agent': request_event.user_agent,
                        'screen_width': request_event.screen_width,
                        'screen_height': request_event.screen_height,
                        'os': user_agent.os.family,
                        'os_version': user_agent.os.version_string,
                        'browser': user_agent.browser.family,
                        'browser_version': user_agent.browser.version_string,
                        'device': user_agent.device.family,
                        'device_type': self._get_device_type(user_agent),
                    }
                )
                device_cache[request_event.user_agent] = device
            if not device:
                continue
            visitor = visitor_cache.get(request_event.tracking_user_id)
            if not visitor:
                visitor, _created = models.Visitor.objects.get_or_create(
                    uuid=request_event.tracking_user_id,
                )
                visitor_cache[request_event.tracking_user_id] = visitor
            visitor.clients.add(request_event.client)
            page_key = (request_event.path, request_event.client)
            page = page_cache.get(page_key)
            if not page:
                page_type = None
                for page_pattern in page_pattern_cache[request_event.client.pk]:
                    if page_pattern.pattern.match(request_event.path):
                        page_type = page_pattern.page_type
                        break
                page, created = models.Page.objects.get_or_create(
                    path=request_event.path,
                    client=request_event.client,
                    defaults={"page_type": page_type}
                )
                page_cache[page_key] = page
            web_property = web_property_cache.get(request_event.domain.lower())
            if not web_property:
                self.stdout.write(
                    'No WebProperty found for domain: %s - skipping' % request_event.domain
                )
                continue
            visit = visit_cache.get(request_event.tracking_key)
            if not visit:
                visit, _created = models.Visit.objects.get_or_create(
                    uuid=request_event.tracking_key,
                    visitor=visitor,
                    defaults={
                        'first_page': page,
                        'device': device,
                        'visit_date': request_event.created.date(),
                        'web_property': web_property,
                    },
                )
                visit_cache[request_event.tracking_key] = visit

            created_page_visits.append(
                models.PageVisit(
                    page=page,
                    visit=visit,
                    request_event=request_event
                )
            )
        if created_page_visits:
            models.PageVisit.objects.bulk_create(created_page_visits)

    def calculate_page_durations(self):
        # finding all page visits with no duration
        # from the last 'max_age' days
        query = models.PageVisit.objects.filter(
            duration=None,
            request_event__created__gte=datetime.now() - timedelta(
                days=self.max_age
            ),
        )
        # This looks a little messy, but makes use of python to get a distinct list
        # as opposed to the database. At least with MySQL, the 'distinct' can be
        # a performance hit.
        all_visits = list(set(
            query.values_list(
                'request_event__tracking_key', flat=True
            )
        ))
        total_visits = len(all_visits)
        start_idx = 0
        subset = 100000 if total_visits > 100000 else total_visits
        while start_idx < total_visits:
            self.stdout.write('\n')
            self.stdout.write('Processing %s to %s of %s total '
                'page visits for duration\n' % (
                    start_idx,
                    start_idx + subset
                        if start_idx + subset < total_visits else total_visits,
                    total_visits
                )
            )
            tracking_keys = all_visits[start_idx: start_idx+subset]
            start_idx += subset
            # finding sessions with more than one request event
            events = list(
                models.RequestEvent.objects.filter(
                    tracking_key__in=tracking_keys
                ).values(
                    'tracking_key'
                ).annotate(
                    Count('tracking_key')
                ).order_by().filter(
                    tracking_key__count__gt=1
                ).values_list('tracking_key', flat=True).distinct()
            )
            # limit the page visits to just those with sessions that
            # have more than one request event
            subquery = query.filter(
                request_event__tracking_key__in=events
            ).select_related('request_event')
            total_page_visits = subquery.count()
            self.stdout.write('Processing %s page visits for durations\n' % total_page_visits)
            for cnt, page_visit in enumerate(subquery):
                if cnt % 1000 == 0:
                    self.stdout.write(
                        'Processed %s of %s page visits\n' % (cnt, total_page_visits)
                    )
                    if settings.DEBUG:
                        reset_queries()
                try:
                    # get the next chronological request event
                    next_event = models.RequestEvent.objects.filter(
                        tracking_key=page_visit.request_event.tracking_key,
                        created__gt=page_visit.request_event.created
                    ).earliest()
                    elapsed_delta = next_event.created - page_visit.request_event.created
                    page_visit.duration = round(elapsed_delta.total_seconds())
                    page_visit.save()
                except models.RequestEvent.DoesNotExist:
                    # nothing newer than the current PageVisit
                    pass

    def collect_visit_data(self):
        # Visit data
        page_pattern_cache = {}
        for pattern in models.PagePattern.objects.select_related().filter(
            page_type__code__in=(
                models.PageType.CONVERSION,
                models.PageType.FUNNEL
            )
        ).order_by('client','page_type').distinct():
            if not pattern.client.pk in page_pattern_cache:
                page_pattern_cache[pattern.client.pk] = defaultdict(list)
            page_pattern_cache[pattern.client.pk][pattern.page_type.code].append(
                re.compile(pattern.pattern, flags=re.IGNORECASE),
            )
        query = models.Visit.objects.filter(
            visit_date__gte=(datetime.now() - timedelta(days=self.max_age))
        ).distinct().annotate(
            calc_duration=Sum('pagevisit__duration')
        ).prefetch_related(
            'pagevisit_set__page__page_type', 'pagevisit_set__page__client',
            'pagevisit_set__request_event'
        )
        total_visits = query.count()
        start_idx = 0
        subset = 100000 if total_visits > 100000 else total_visits
        while start_idx < total_visits:
            self.stdout.write('\n')
            self.stdout.write('Processing %s to %s of %s total '
                'page visits for other data\n' % (
                    start_idx,
                    start_idx + subset
                        if start_idx + subset < total_visits else total_visits,
                    total_visits
                )
            )
            visit_subset = query[start_idx: start_idx+subset]
            start_idx += subset

            for cnt, visit in enumerate(visit_subset):
                if cnt % 1000 == 0:
                    self.stdout.write(
                        'Processed %s of %s visits\n' % (cnt, len(visit_subset))
                    )
                    if settings.DEBUG:
                        reset_queries()
                update_fields = []
                pagevisits = sorted(
                    visit.pagevisit_set.all(),
                    cmp=lambda x, y: cmp(x.request_event.created, y.request_event.created)
                )
                if not visit.last_page or visit.last_page.pk != pagevisits[-1].pk:
                    visit.last_page = pagevisits[-1].page
                    update_fields.append('last_page')
                order_ids = []
                conversion_count = 0
                funnel_found = False
                for page_visit in pagevisits:
                    page_patterns = page_pattern_cache.get(page_visit.page.client.pk, {})
                    # in order to count a conversion, the visitor has to have hit
                    # at least one funnel page
                    for pattern in page_patterns.get(models.PageType.FUNNEL, []):
                        if pattern.match(page_visit.page.path):
                            funnel_found = True
                            break
                    for pattern in page_patterns.get(models.PageType.CONVERSION, []):
                        m = pattern.match(page_visit.page.path)
                        if m and len(m.groups()) > 0 and funnel_found:
                            order_ids.append(m.group(1))
                            funnel_found = False
                            break
                conversion_count = len(set(order_ids))
                if visit.conversion_count != conversion_count:
                    visit.conversion_count = conversion_count
                    update_fields.append('conversion_count')
                if visit.duration != visit.calc_duration:
                    visit.duration = visit.calc_duration
                    update_fields.append('duration')
                if update_fields:
                    visit.save(update_fields=update_fields)

    def _get_device_type(self, user_agent):
        code = models.DeviceType.UNKNOWN
        if user_agent.is_mobile:
            code = models.DeviceType.MOBILE
        elif user_agent.is_tablet:
            code = models.DeviceType.TABLET
        elif user_agent.is_pc:
            code = models.DeviceType.DESKTOP
        elif user_agent.is_bot:
            code = models.DeviceType.BOT
        device_type = self.device_type_cache.get(code)
        if not device_type:
            device_type, _created = models.DeviceType.objects.get_or_create(
                code=code,
                defaults={'name': code.capitalize()}
            )
            self.device_type_cache[code] = device_type
        return device_type
