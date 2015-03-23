from django.conf.urls import patterns, url

urlpatterns = patterns('djanalytics.reports.views',
    url(r'^audience_overview/$', 'audience_overview', name='audience_overview'),
    url(r'^device_overview/$', 'device_overview', name='device_overview'),
    url(r'^ecommerce_overview/$', 'ecommerce_overview', name='ecommerce_overview'),
    url(r'^page_overview/$', 'page_overview', name='page_overview'),
    url(r'^device_detail/$', 'device_detail', name='device_detail'),
    url(r'^browser_detail/$', 'browser_detail', name='browser_detail'),
)
