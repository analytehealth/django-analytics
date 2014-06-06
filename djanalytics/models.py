import datetime
import ipaddress
import re
import uuid

from django.conf import settings
from django.db import models
from django.db.models.query import QuerySet

def generate_uuid():
    '''Generate a nice unique number (str).'''
    return str(uuid.uuid4())


class Client(models.Model):
    name = models.CharField(max_length=100)
    uuid = models.CharField(max_length=36, default=generate_uuid())

    def ip_valid(self, ip_address):
        return self._valid('ipfilter_set', ip_address)

    def path_valid(self, path):
        return self._valid('pathfilter_set', path)

    def _valid(self, attr, value):
        include_query = getattr(self, attr).filter(include=True)
        # if there are no include filters, the value is not excluded,
        # otherwise the value is allowed if there is at least include filter 
        # for which it is valid
        include = not include_query.exists() or any(
            filt.valid(value)
            for filt in include_query
        )
        # the value is valid if it is explicitly included (see above) and
        # there are no exclusion rules that apply
        return include and all(
            filt.valid(value)
            for filt in getattr(self, attr).filter(include=False)
        )

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.uuid)

    class Meta(object):
        app_label = 'djanalytics'


DATE_FORMAT_STRINGS = {
    'django.db.backends.mysql': "DATE_FORMAT({}, '%%Y-%%m-%%d')",
    'django.db.backends.postgresql.psycopg2': "to_char({}, 'yyyy-mm-dd')",
    'django.db.backends.sqlite3': "strftime('%%Y-%%m-%%d', {})"
}


class RequestEventQuerySet(QuerySet):

    def with_created_date(self):
        if hasattr(settings, 'DATABASES'):
            engine = settings.DATABASES[self.db]['ENGINE']
        else:
            engine = settings.DATABASE_ENGINE
        return self.extra(
            select={
                'created_date':
                    DATE_FORMAT_STRINGS[engine].format('djanalytics_requestevent.created')
            }
        )


class RequestEventManager(models.Manager):

    def get_query_set(self):
        return RequestEventQuerySet(self.model, using=self._db)

    def with_created_date(self):
        return self.get_query_set().with_created_date()

class RequestEvent(models.Model):
    ip_address = models.IPAddressField(db_index=True)
    user_agent = models.TextField(null=True, blank=True)
    tracking_key = models.CharField(max_length=36, default=generate_uuid)
    tracking_user_id = models.CharField(max_length=36, default=generate_uuid)
    protocol = models.CharField(max_length=10)
    domain = models.CharField(max_length=100, db_index=True)
    path = models.URLField(blank=True, db_index=True)
    query_string = models.TextField(null=True, blank=True)
    method = models.CharField(max_length=5, null=True, blank=True, db_index=True)
    referrer = models.URLField(blank=True, null=True, db_index=True)
    created = models.DateTimeField(default=datetime.datetime.now(), db_index=True)
    response_code = models.IntegerField(null=True, blank=True, db_index=True)
    client = models.ForeignKey(Client)

    objects = RequestEventManager()

    class Meta(object):
        app_label = 'djanalytics'
        get_latest_by = 'created'


class Domain(models.Model):
    pattern = models.CharField(max_length=100)
    client = models.ForeignKey(Client)

    def __unicode__(self):
        return '%s: %s' % (self.client.name, self.pattern)

    class Meta(object):
        app_label = 'djanalytics'


class IPFilter(models.Model):
    netmask = models.CharField(max_length=19)
    include = models.BooleanField()
    client = models.ForeignKey(Client)

    def valid(self, ip_address):
        return self.include == (
            ipaddress.ip_address(unicode(ip_address))
            in ipaddress.ip_network(unicode(self.netmask))
        )

    def __unicode__(self):
        return '%s: %s' % (self.client.name, self.netmask)

    class Meta(object):
        app_label = 'djanalytics'


class PathFilter(models.Model):
    path_pattern = models.CharField(max_length=200)
    include = models.BooleanField()
    client = models.ForeignKey(Client)

    def valid(self, path):
        if re.match(self.path_pattern, path):
            return self.include
        return not self.include

    def __unicode__(self):
        return '%s: %s' % (self.client.name, self.path_pattern)

    class Meta(object):
        app_label = 'djanalytics'

