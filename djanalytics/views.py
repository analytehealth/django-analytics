import re

from urlparse import urlparse

from django.http.request import QueryDict
from django.http.response import (
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseBadRequest
)
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from djanalytics import models


class CaptureEventView(View):

    @csrf_exempt
    def post(self, request):
        tracking_id = request.session.get('dja_tracking_id')
        try:
            origin = urlparse(request.META.get('HTTP_ORIGIN')).hostname
        except AttributeError:
            return HttpResponseBadRequest(content='Unable to parse HTTP_ORIGIN')
        query = QueryDict(request.META.get('QUERY_STRING'))
        try:
            client_id = query['dja_id']
        except KeyError:
            return HttpResponseBadRequest(content='dja_id not passed')

        try:
            client = models.Client.objects.get(uuid=client_id)
        except models.Client.DoesNotExist:
            return HttpResponseForbidden(content='Client not found')

        for domain in client.domain_set.all():
            if re.match('.*%s$' % domain.pattern, origin, re.IGNORECASE):
                break
            return HttpResponseForbidden(content='Invalid domain for client')

        data = {
            'client': client,
            'ip_address': request.META.get('REMOTE_ADDR'),
            'user_agent': request.META.get('HTTP_USER_AGENT', 'None'),
            'path': request.path,
            'query_string': ','.join(('%s=%s' % (k, v) for k, v in request.POST.items())),
            'method': 'GET'
        }
        if tracking_id:
            data['tracking_key'] = tracking_id
        new_event = models.RequestEvent.objects.create(**data)
        if not tracking_id:
            request.session['dja_tracking_id'] = new_event.tracking_key
        return HttpResponse(status=204)

capture_event = CaptureEventView.as_view()