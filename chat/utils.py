from django import template
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.humanize.templatetags.humanize import naturaltime

register = template.Library()

@register.filter
def custom_naturaltime(value):
    if not value:
        return ""

    # Calculate the time difference between now and the value
    time_diff = now() - value

    # If the difference is less than a day, return the naturaltime output (e.g., "3 hours ago")
    if time_diff < timedelta(days=1):
        return naturaltime(value)

    # Otherwise, return the time difference in days only
    return f"{time_diff.days} days ago"
