from django import template
from django.utils import timezone


register = template.Library()



@register.filter
def cut_and_split(value):
    return value.replace(' ', '').split(',')

@register.filter
def cut_and_lower(value):
    return value.replace(' ', '_').lower()
