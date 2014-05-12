from django.conf import settings

from djanalytics import models


class AnalyticsMiddleware(object):

    def process_response(self, request, response):
        tracking_id = request.session.get('dja_tracking_id')
        user_id = request.COOKIES.get('dja_uuid')
        client = models.Client.objects.get(uuid=settings.DJANALYTICS_ID)

        data = {
            'client': client,
            'ip_address': request.META.get('REMOTE_ADDR'),
            'user_agent': request.META.get('HTTP_USER_AGENT', 'None'),
            'path': request.path,
            'query_string': request.META.get('QUERY_STRING'),
            'method': request.method,
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
