from django.contrib import admin
from djanalytics import models


class DomainInline(admin.TabularInline):
    model = models.Domain
    extra = 1


class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'uuid')
    readonly_fields = ('uuid', )
    inlines = [ DomainInline ]
