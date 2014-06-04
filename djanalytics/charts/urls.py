from django.conf.urls import patterns, url

urlpatterns = patterns('djanalytics.charts.views',
    url(r'^charts/session/$', 'session_chart', name='dja_session_chart'),
    url(r'^charts/user/$', 'user_chart', name='dja_user_chart'),
)
