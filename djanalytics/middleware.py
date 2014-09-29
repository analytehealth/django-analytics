import logging
import re

from urlparse import urlparse

from django.conf import settings

from djanalytics import models


class AnalyticsMiddleware(object):

    def process_response(self, request, response):
        tracking_id = request.session.get('dja_tracking_id')
        user_id = request.COOKIES.get('dja_uuid')
        try:
            client_id = getattr(settings, 'DJA_CLIENT_ID', '')
            client = models.Client.objects.get(uuid=client_id)
        except models.Client.DoesNotExist:
            logging.getLogger('djanalytics').exception(
                'Client %s does not exist', client_id
            )
            return response

        if not client.path_valid(
            request.path
        ) or not client.ip_valid(
            request.META.get('REMOTE_ADDR')
        ):
            return response

        data = {
            'client': client,
            'ip_address': request.META.get('REMOTE_ADDR'),
            'user_agent': request.META.get('HTTP_USER_AGENT', 'None'),
            'path': request.path,
            'query_string': request.META.get('QUERY_STRING'),
            'referrer': request.META.get('HTTP_REFERER', '')[:2083],
            'method': request.method,
            'domain': request.META.get('HTTP_HOST', ''),
            'response_code': response.status_code
        }
        if tracking_id:
            data['tracking_key'] = tracking_id
        if user_id:
            data['tracking_user_id'] = user_id
        new_event = models.RequestEvent.objects.create(**data)
        if not tracking_id:
            request.session['dja_tracking_id'] = new_event.tracking_key
        response.set_cookie('dja_uuid', new_event.tracking_user_id)
        return response


class CrossDomainMiddleware(object):

    def process_response(self, request, response):
        data = getattr(request, request.META.get('REQUEST_METHOD', 'GET'), {})
        uuid = data.get('dja_uuid')
        tracking_id = data.get('dja_tracking_id')
        client_id = data.get('dja_id')
        try:
            self.client = models.Client.objects.get(uuid=client_id)
        except models.Client.DoesNotExist:
            logging.getLogger('djanalytics').exception(
                'Client %s does not exist', client_id
            )
            return response

        if not self.client.domain_set.exists():
            logging.getLogger('djanalytics').exception(
                'No domains found for client %s', client_id
            )
            return response

        parsed_referrer = urlparse(request.META.get('HTTP_REFERER', ''))
        origin = parsed_referrer.hostname or ''
        domain_found = False
        for domain in self.client.domain_set.all():
            if re.match('.*%s$' % domain.pattern, origin, re.IGNORECASE):
                domain_found = True
                break
        if not domain_found:
            logging.getLogger('djanalytics').exception(
                'Invalid domain for client %s', client_id
            )
            return response

        if settings.USE_X_FORWARDED_HOST:
            client_ip = request.META.get(
                'HTTP_X_FORWARDED_FOR',
                request.META.get('REMOTE_ADDR', '')
            )
        else:
            client_ip = request.META.get('REMOTE_ADDR')
        if not self.client.ip_valid(client_ip):
            return response

        parsed_url = urlparse(request.META.get('HTTP_HOST', ''))
        domain = '.'.join(parsed_url.netloc.split('.')[-2:])
        response.set_cookie('dja_uuid', uuid, domain=domain)
        response.set_cookie('dti', tracking_id, domain=domain)
        return response
