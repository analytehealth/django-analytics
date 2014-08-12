import logging

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
