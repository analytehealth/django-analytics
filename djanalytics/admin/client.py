from django.contrib import admin
from djanalytics import models


class DomainInline(admin.TabularInline):
    model = models.Domain
    extra = 1


class ClientAdmin(admin.ModelAdmin):
    inlines = [ DomainInline ]
