from django import template
import hashlib
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def md5hash(email): # Only one argument.
    md5_hash = hashlib.md5(email.strip().lower().encode())
    return md5_hash.hexdigest()

