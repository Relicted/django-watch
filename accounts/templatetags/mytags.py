import re

from django import template
from django.core.urlresolvers import reverse, NoReverseMatch

register = template.Library()


@register.simple_tag(takes_context=True)
def active(context, pattern):
    url = reverse(pattern)
    if context.request.path == url:
        return 'active'
    return ''


@register.filter
def is_profile(value):
    profile = reverse('settings:profile')
    if value == profile:
        return True
    return False
