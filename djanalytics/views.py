import re

from datetime import datetime, timedelta
from urlparse import urlparse

from django.http.request import QueryDict
from django.http.response import (
    HttpResponseForbidden,
    HttpResponseBadRequest
, HttpResponse)
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from . import models
from .http import JsonHttpResponse


class CaptureEventView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CaptureEventView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        tracking_id = request.session.get('dja_tracking_id')
        user_id = request.COOKIES.get('dja_uuid')
        try:
            origin = urlparse(request.META.get('HTTP_REFERER')).hostname
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

        if not client.path_valid(
            request.POST.get('pth', '')
        ) or not client.ip_valid(
            request.META.get('REMOTE_ADDR')
        ):
            return HttpResponse(status=204) # NO_CONTENT

        data = {
            'client': client,
            'ip_address': request.META.get('REMOTE_ADDR'),
            'user_agent': request.META.get('HTTP_USER_AGENT', 'None'),
            'path': request.POST.get('pth', ''),
            'query_string': request.POST.get('qs', ''),
            'method': 'GET'
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
        data = {
            'dja_tracking_id': new_event.tracking_key,
            'dja_uuid': new_event.tracking_user_id
        }
        response = JsonHttpResponse(content=data, status=status)
        response.set_cookie('dja_uuid', new_event.tracking_user_id,
                            expires=datetime.now() + timedelta(days=365))
        return response

capture_event = CaptureEventView.as_view()