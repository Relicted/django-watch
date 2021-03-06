from django.core.urlresolvers import reverse

from django import template

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


@register.filter('fieldtype')
def fieldtype(field):
    return field.field.widget.__class__.__name__.lower()