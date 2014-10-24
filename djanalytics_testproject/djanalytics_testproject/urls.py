from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import TemplateView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'djanalytics_testproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', include('djanalytics.urls')),
    url(r'', include('djanalytics.charts.urls')),
    url(r'^$', TemplateView.as_view(template_name='djanalytics/djanalytics_index.html')),
)
