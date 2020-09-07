from django import template
import hashlib
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def replacespacewith_(s): # Only one argument.
    return s.replace(' ', '_').lower()

