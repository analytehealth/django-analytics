from django.db import models

from .validators import validate_type


class CodedModel(models.Model):
    code = models.CharField(
        unique=True, max_length=50, validators=[validate_type], db_index=True
    )

    class Meta:
        abstract = True


class PageType(CodedModel):
    ''' Way to 'tag' pages for things like 'funnel', 'conversion', etc. '''
    name = models.CharField(max_length=50, unique=True)

    CONVERSION = 'conversion'
    FUNNEL = 'funnel'

    class Meta:
        app_label = 'djanalytics'

    def __unicode__(self):
        return u'%s' % self.name


class Page(models.Model):
    ''' Auto generated for every page visited '''
    path = models.URLField()
    client = models.ForeignKey('Client')
    page_type = models.ForeignKey('PageType', null=True)

    def __unicode__(self):
        return u'%s' % self.path

    class Meta:
        app_label = 'djanalytics'
        unique_together = ('path', 'client')


class PagePattern(CodedModel):
    ''' Used to group pages together as a single 'page'.
        Useful for things like item pages where the id is part
        of the URL. '''
    name = models.CharField(max_length=80)
    pattern = models.CharField(max_length=200)
    display_path = models.CharField(
        max_length=200,help_text='How to display on reports'
    )
    client = models.ForeignKey('Client')
    page_type = models.ForeignKey('PageType')

    class Meta:
        app_label = 'djanalytics'
        unique_together = ('pattern', 'client')


    def __unicode__(self):
        return u'%s (%s) - %s' % (self.name, self.pattern, self.page_type)


class ReferrerType(CodedModel):
    ''' Used to classify referrer URLs '''
    name = models.CharField(max_length=80, unique=True)
    pattern = models.CharField(max_length=200, unique=True)

    class Meta:
        app_label = 'djanalytics'


class DeviceType(CodedModel):
    ''' Group multiple device objects together into a single 'type' '''
    name = models.CharField(max_length=80, unique=True)
    DESKTOP = 'desktop'
    MOBILE = 'mobile'
    TABLET = 'tablet'
    BOT = 'bot'
    UNKNOWN = 'unknown'

    class Meta:
        app_label = 'djanalytics'

    def __unicode__(self):
        return u'%s' % self.name


class Device(models.Model):
    ''' Auto generated for unique combinations of OS / Browser / Screen Resolution '''
    user_agent = models.TextField(blank=True)
    user_agent_md5 = models.CharField(max_length=32, db_index=True, unique=True)
    os = models.CharField(max_length=100, db_index=True)
    os_version = models.CharField(max_length=20, null=True, blank=True, db_index=True)
    browser = models.CharField(max_length=100, db_index=True)
    browser_version = models.CharField(max_length=20, null=True, blank=True, db_index=True)
    device = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    device_type = models.ForeignKey('DeviceType', null=True, blank=True, db_index=True)
    screen_width = models.PositiveSmallIntegerField(null=True, blank=True, db_index=True)
    screen_height = models.PositiveSmallIntegerField(null=True, blank=True, db_index=True)

    def __unicode__(self):
        return (
            u'OS: %(os)s (%(os_version)s) '
            'Browser: %(browser)s (%(browser_version)s) '
            'Device: %(device)s '
            'DeviceType: %(device_type)s' % {
                'os': self.os, 'os_version': self.os_version,
                'browser': self.browser, 'browser_version': self.browser_version,
                'device': self.device,
                'device_type': self.device_type.name if self.device_type else 'unknown'
            }
        )

    @property
    def resolution(self):
        if self.screen_height and self.screen_width:
            return '%sx%s' % (self.screen_width, self.screen_height)
        else:
            return '-'

    @property
    def name(self):
        """ Return a basic meaningful name based on device type """
        if (
            self.device_type and
            self.device_type.code in (DeviceType.MOBILE, DeviceType.TABLET)
        ):
            return self.device
        else:
            return self.browser

    class Meta:
        app_label = 'djanalytics'
        index_together = [
            ('browser','browser_version'),
            ('os', 'os_version'),
            ('screen_width', 'screen_height'),
        ]


class Visitor(models.Model):
    uuid = models.CharField(max_length=36, db_index=True)
    clients = models.ManyToManyField('Client')

    class Meta:
        app_label = 'djanalytics'


class PageVisit(models.Model):
    page = models.ForeignKey('Page')
    visit = models.ForeignKey('Visit')
    request_event = models.ForeignKey('RequestEvent')
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    duration = models.DecimalField(max_digits=7, decimal_places=0, null=True)

    class Meta:
        app_label = 'djanalytics'
        get_latest_by = 'request_event__created'


class Visit(models.Model):
    uuid = models.CharField(max_length=36, db_index=True)
    visitor = models.ForeignKey('Visitor')
    pages = models.ManyToManyField('Page', through='PageVisit')
    device = models.ForeignKey('Device')
    visit_date = models.DateField(db_index=True)
    duration = models.DecimalField(max_digits=7, decimal_places=0, null=True)
    first_page = models.ForeignKey('Page', related_name='first_visit')
    last_page = models.ForeignKey('Page', related_name='last_visit', null=True)
    conversion_count = models.IntegerField(default=0)
    web_property = models.ForeignKey('WebProperty')
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'djanalytics'

