from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import TemplateView

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', include('djanalytics.urls')),
    url(r'', include('djanalytics.charts.urls')),
    url(r'^reports', include('djanalytics.reports.urls')),
    url(r'^$', TemplateView.as_view(template_name='djanalytics/djanalytics_index.html')),
)
