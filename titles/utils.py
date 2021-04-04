import datetime

from django.core.exceptions import ValidationError


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    if value < 1900 or value > datetime.datetime.now().year:
        raise ValidationError(
            ('%(value)s is not a correcrt year!'),
            params={'value': value},
        )
    return value
