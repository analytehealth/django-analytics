from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import TemplateView

from djanalytics import urls as djanalytics_urls
from djanalytics.charts import urls as charts_urls
from djanalytics.reports import urls as reports_urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(djanalytics_urls)),
    url(r'^', include(charts_urls)),
    url(r'^reports', include(reports_urls)),
    url(r'^$', TemplateView.as_view(template_name='djanalytics/djanalytics_index.html')),
]
