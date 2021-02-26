from django import template

register = template.Library()


@register.filter(name="set")
def make_set(val):
    return set(val)
