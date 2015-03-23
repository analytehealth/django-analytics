from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
   url(r'^', include('djanalytics.urls')),
   url(r'^', include('djanalytics.charts.urls')),
   url(r'^reports', include('djanalytics.reports.urls')),
)
