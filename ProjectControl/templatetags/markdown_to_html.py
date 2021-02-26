from django import template

register = template.Library()


@register.filter(name="markdown_split")
def split_to_divs(val):
    return "<div>" + val.replace("\n", "</div><div>") + "</div>"
