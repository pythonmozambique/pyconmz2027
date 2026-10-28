from django import template
from django.utils.translation import gettext

register = template.Library()


@register.filter(name="translate")
def translate(value):
    """Translate an English string stored in the database.

    The msgid must match the English seed text exactly.
    """
    if value is None:
        return ""
    return gettext(str(value))
