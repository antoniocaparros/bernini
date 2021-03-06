from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_price(value):
    if value < 0.0:
        raise ValidationError(
            _('%(value)s is not a positive number'),
            params={'value': value},
        )