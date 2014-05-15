from django.conf import settings

# path to prepend to all django-analytics urls 
BASE_PATH = getattr(settings, 'DJA_BASE_PATH', 'dja')

# client id to use for requests. must be set to use django-analytics
CLIENT_ID = getattr(settings, 'DJA_CLIENT_ID')
