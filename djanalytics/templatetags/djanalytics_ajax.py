from django import template
from djanalytics import settings
from django.template.loader import render_to_string

register = template.Library()

def djanalytics_ajax():
    return render_to_string(
        'djanalytics/djajax.html',
        {
            'dja_base_path': settings.BASE_PATH,
            'dja_client_id': settings.CLIENT_ID
        }
    )

register.simple_tag(djanalytics_ajax)