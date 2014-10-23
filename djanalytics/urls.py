from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView


urlpatterns = patterns('djanalytics.views',
    url(r'^capture/$', 'capture_event', name='dja_capture'),
    url(r'^djanalytics.js$', 'djanalytics_js', name='djanalytics_js'),
    url(r'^$', TemplateView.as_view(template_name='reports/djanalytics_index.html')),
)
