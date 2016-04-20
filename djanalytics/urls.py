from django.conf.urls import include, url
from djanalytics.views import capture_event, djanalytics_js

urlpatterns = [
    url(r'^capture/$', capture_event, name='dja_capture'),
    url(r'^djanalytics.js$', djanalytics_js, name='djanalytics_js'),
]
