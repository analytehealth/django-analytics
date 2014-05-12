from django.contrib import admin

from djanalytics import models
from djanalytics.admin.client import ClientAdmin

admin.site.register(models.Client, ClientAdmin)
