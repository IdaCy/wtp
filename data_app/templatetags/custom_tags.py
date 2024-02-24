from django import template

register = template.Library()


@register.simple_tag
def to(value, end):
    """Generates a range of numbers for iteration in templates."""
    return range(value, end + 1)
