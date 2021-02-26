from django import template

reg = template.Library()


def make_set(value):
    return set(value)


reg.filter("set", make_set)
