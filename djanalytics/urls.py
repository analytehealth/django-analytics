from django.conf.urls import patterns, include, url


urlpatterns = patterns('djanalytics.views',
    url(r'^capture/$', 'capture_event', name='dja_capture'),
    url(r'^djanalytics.js$', 'djanalytics_js', name='djanalytics_js'),
)
