from django.contrib import admin

from djanalytics import models
from djanalytics.admin.client import ClientAdmin
from djanalytics.admin.reports import DeviceTypeAdmin

admin.site.register(models.Client, ClientAdmin)
admin.site.register(models.WebProperty)
admin.site.register(models.Domain)
admin.site.register(models.IPFilter)
admin.site.register(models.PathFilter)
admin.site.register(models.PagePattern)
admin.site.register(models.ReferrerType)
admin.site.register(models.DeviceType, DeviceTypeAdmin)
admin.site.register(models.Page)
admin.site.register(models.PageType)
