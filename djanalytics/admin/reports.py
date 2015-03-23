from django.contrib import admin
from djanalytics import models


class DeviceTypeInline(admin.TabularInline):
    
    model = models.Device
    

class DeviceTypeAdmin(admin.ModelAdmin):
    inlines = [ DeviceTypeInline ]