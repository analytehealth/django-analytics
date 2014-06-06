from djanalytics import models, settings


class AnalyticsMiddleware(object):

    def process_response(self, request, response):
        tracking_id = request.session.get('dja_tracking_id')
        user_id = request.COOKIES.get('dja_uuid')
        client = models.Client.objects.get(uuid=settings.CLIENT_ID)

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
            'referrer': request.META.get('HTTP_REFERER'),
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
