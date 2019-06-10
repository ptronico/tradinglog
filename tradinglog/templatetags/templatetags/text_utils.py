import markdown as md

from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()


@register.filter()
@stringfilter
def markdown(text):
    """Converts a markdown string into html."""
    return md.markdown(text)
