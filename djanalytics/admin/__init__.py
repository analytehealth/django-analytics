from django.contrib import admin

from djanalytics import models
from djanalytics.admin.client import ClientAdmin

admin.site.register(models.Client, ClientAdmin)
admin.site.register(models.Domain)
admin.site.register(models.IPFilter)
admin.site.register(models.PathFilter)
