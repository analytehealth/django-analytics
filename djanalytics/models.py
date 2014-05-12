import uuid

from django.db import models


def generate_uuid():
    '''Generate a nice unique number (str).'''
    return str(uuid.uuid4())


class Client(models.Model):
    name = models.CharField(max_length=100)
    uuid = models.CharField(max_length=36, default=generate_uuid())

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.uuid)

    class Meta(object):
        app_label='djanalytics'


class RequestEvent(models.Model):
    ip_address = models.IPAddressField()
    user_agent = models.TextField(null=True, blank=True)
    tracking_key = models.CharField(max_length=36, default=generate_uuid)
    tracking_user_id = models.CharField(max_length=36, default=generate_uuid)
    path = models.URLField(blank=True)
    query_string = models.TextField(null=True, blank=True)
    method = models.CharField(max_length=5)
    datetime = models.DateTimeField(auto_now_add=True)
    response_code = models.IntegerField(null=True, blank=True)
    client = models.ForeignKey(Client)

    class Meta(object):
        app_label='djanalytics'


class Domain(models.Model):
    pattern = models.CharField(max_length=100)
    client = models.ForeignKey(Client)

    def __unicode__(self):
        return self.pattern

    class Meta(object):
        app_label='djanalytics'

