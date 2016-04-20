from django.conf.urls import include, url
from djanalytics import urls as djanalytics_urls
from djanalytics.charts import urls as charts_urls
from djanalytics.reports import urls as reports_urls

urlpatterns = [
   url(r'^', include(djanalytics_urls)),
   url(r'^', include(charts_urls)),
   url(r'^reports', include(reports_urls)),
]
