from django.conf.urls import patterns, url
from djanalytics.charts.views import (
    exit_page,
    page_visit,
    referrer,
    session_chart,
    user_chart,
)

urlpatterns = [
    url(r'^charts/session/$', session_chart, name='session_chart'),
    url(r'^charts/user/$', user_chart, name='user_chart'),
    url(r'^charts/page_visit/$', page_visit, name='page_visit'),
    url(r'^charts/exit_page/$', exit_page, name='exit_page'),
    url(r'^charts/referrer/$', referrer, name='referrer'),
]
