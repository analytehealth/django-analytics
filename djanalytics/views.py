import os
import re

from datetime import datetime, timedelta
from urlparse import urlparse

from django.http.response import (
    HttpResponseForbidden,
    HttpResponseBadRequest,
    HttpResponse
)
from django.views.generic.base import View

from . import models

TRACKING_PIXEL_PATH = os.path.join(os.path.dirname(__file__), 'templates')

class CaptureEventView(View):

    def get(self, request):
        tracking_id = request.session.get('dja_tracking_id')
        user_id = request.COOKIES.get('dja_uuid')
        parsed_url = urlparse(request.META.get('HTTP_REFERER', ''))
        origin = parsed_url.hostname
        try:
            client_id = request.GET.get('dja_id')
        except KeyError:
            return HttpResponseBadRequest(content='dja_id not passed')

        try:
            client = models.Client.objects.get(uuid=client_id)
        except models.Client.DoesNotExist:
            return HttpResponseForbidden(content='Client not found')

        if not client.domain_set.exists():
            return HttpResponseBadRequest(content='No domains found for client')

        for domain in client.domain_set.all():
            if re.match('.*%s$' % domain.pattern, origin, re.IGNORECASE):
                break
            return HttpResponseForbidden(content='Invalid domain for client')

        if not client.path_valid(
            request.GET.get('pth', '')
        ) or not client.ip_valid(
            request.META.get('REMOTE_ADDR')
        ):
            return HttpResponse(status=204) # NO_CONTENT

        data = {
            'domain': parsed_url.netloc,
            'protocol': parsed_url.scheme,
            'client': client,
            'ip_address': request.META.get('REMOTE_ADDR'),
            'user_agent': request.META.get('HTTP_USER_AGENT', 'None'),
            'path': request.GET.get('pth', ''),
            'query_string': request.GET.get('qs', ''),
        }
        status = 201 # CREATED
        if tracking_id:
            data['tracking_key'] = tracking_id
            status = 202 # ACCEPTED
        if user_id:
            data['tracking_user_id'] = user_id
            status = 202 # ACCEPTED
        new_event = models.RequestEvent.objects.create(**data)
        if not tracking_id:
            request.session['dja_tracking_id'] = new_event.tracking_key
        img_data = file(os.path.join(TRACKING_PIXEL_PATH, 'tracking_pixel.png')).read()
        response = HttpResponse(content=img_data, status=status, mimetype='image/png')
        response.set_cookie('dja_uuid', new_event.tracking_user_id,
                            expires=datetime.now() + timedelta(days=365))
        return response

capture_event = CaptureEventView.as_view()