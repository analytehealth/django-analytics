import os
import re
import warnings

from datetime import datetime, timedelta
from urlparse import urlparse

import jsmin

from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.http.response import (
    HttpResponseForbidden,
    HttpResponseBadRequest,
    HttpResponse
)
from django.template.response import TemplateResponse
from django.views.generic.base import View, TemplateView

from . import models

TRACKING_PIXEL_PATH = os.path.join(os.path.dirname(__file__), 'templates')

class ValidatedViewMixin(object):

    parsed_url = None
    client = None
    client_ip = None

    def is_valid(self, request):
        self.parsed_url = urlparse(request.META.get('HTTP_REFERER', ''))
        origin = self.parsed_url.hostname or ''
        client_id = request.GET.get('dja_id')

        try:
            self.client = models.Client.objects.get(uuid=client_id)
        except models.Client.DoesNotExist:
            return HttpResponseForbidden(content='Client not found')

        if not self.client.domain_set.exists():
            return HttpResponseBadRequest(content='No domains found for client')

        domain_found = self.client.domain_set.filter(name=origin).exists()
        if not domain_found:
            warnings.warn(
                "Use of domain patterns will be removed in a future version.",
                DeprecationWarning
            )
            for domain in self.client.domain_set.all():
                if (
                    domain.pattern and
                    re.match('.*%s$' % domain.pattern, origin, re.IGNORECASE)
                ):
                    domain_found = True
                    break
        if not domain_found:
            return HttpResponseForbidden(content='Invalid domain for client')

        if settings.USE_X_FORWARDED_HOST:
            self.client_ip = request.META.get(
                'HTTP_X_FORWARDED_FOR',
                request.META.get('REMOTE_ADDR', '')
            )
        else:
            self.client_ip = request.META.get('REMOTE_ADDR')


class CaptureEventView(View, ValidatedViewMixin):

    def get(self, request):
        invalid_response = self.is_valid(request)

        if invalid_response:
            return invalid_response

        if not self.client.path_valid(
            request.GET.get('pth', '')
        ) or not self.client.ip_valid(self.client_ip):
            return HttpResponse(status=204) # NO_CONTENT

        tracking_id = request.GET.get(
            'dti', request.session.get('dja_tracking_id')
        )
        user_id = request.GET.get(
            'du', request.COOKIES.get('dja_uuid')
        )
        data = {
            'domain': self.parsed_url.netloc,
            'protocol': self.parsed_url.scheme,
            'client': self.client,
            'ip_address': self.client_ip,
            'user_agent': request.META.get('HTTP_USER_AGENT', 'None'),
            'path': request.GET.get('pth', ''),
            'query_string': request.GET.get('qs', ''),
            'referrer': request.GET.get('rf', '')[:2083],
            'screen_width': request.GET.get('sw'),
            'screen_height': request.GET.get('sh'),
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
        response = HttpResponse(content=img_data, status=status, content_type='image/png')
        response.set_cookie('dja_uuid', new_event.tracking_user_id,
                            expires=datetime.now() + timedelta(days=365))
        return response

capture_event = CaptureEventView.as_view()


class MinifiedJsTemplateResponse(TemplateResponse):

    @property
    def rendered_content(self):
        """Returns a 'minified' version of the javascript content"""
        template = self.resolve_template(self.template_name)
        if template.name.endswith('.min'):
            return super(MinifiedJsTemplateResponse, self).rendered_content
        # if no minified template exists, minify the response
        content = super(MinifiedJsTemplateResponse, self).rendered_content
        content = jsmin.jsmin(content)
        return content


class DjanalyticsJs(TemplateView):

    response_class = MinifiedJsTemplateResponse
    content_type = 'application/javascript'

    def get_template_names(self):
        return ['djanalytics.js.min', 'djanalytics.js']

    def get_context_data(self, **kwargs):
        parsed_url = urlparse(self.request.META.get('HTTP_REFERER', ''))
        client_id = self.request.GET.get('dja_id')
        context_data = super(DjanalyticsJs, self).get_context_data(**kwargs)
        tl_domain = '.'.join(parsed_url.netloc.split('.')[-2:])
        # the js will check for existing cookie values for uuid and tracking_id
        # and will only use the generated values below if cookie values
        # don't exist
        context_data.update(
            {
                'uuid': models.generate_uuid(),
                'tracking_id': models.generate_uuid(), 
                'domain': '.%s' % tl_domain,
                'dja_id': client_id,
                'capture_img_url': '%s%s' % (
                    self.request.META.get('HTTP_HOST', ''),
                    reverse_lazy('dja_capture')
                ),
            }
        )
        return context_data

djanalytics_js = DjanalyticsJs.as_view()