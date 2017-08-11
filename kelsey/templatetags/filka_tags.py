from django import template


register = template.Library()


@register.filter(name='inv')
def inv(value):
    return -int(value)
