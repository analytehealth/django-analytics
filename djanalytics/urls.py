from django.conf.urls import patterns, url


urlpatterns = patterns('djanalytics.views',
    url(r'^capture/$', 'capture_event', name='dja_capture'),
)
