from django import template
from django.db.models.aggregates import Count

from ..models import User

register = template.Library()

@register.simple_tag
def get_user(name):
    return User.objects.get(name=name)