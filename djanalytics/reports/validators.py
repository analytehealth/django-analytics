import re

from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator

validate_type = RegexValidator(
    re.compile('^[a-zA-Z0-9_]+$'),
    _("Enter a valid 'type' consisting of letters, numbers, and/or underscores."),
    'invalid'
)

