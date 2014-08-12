from django.conf.urls import patterns, url

urlpatterns = patterns('djanalytics.charts.views',
    url(r'^charts/session/$', 'session_chart', name='session_chart'),
    url(r'^charts/user/$', 'user_chart', name='user_chart'),
    url(r'^charts/page_visit/$', 'page_visit', name='page_visit'),
)
