from django import template

register = template.Library()

@register.filter
def format_korean_datetime(value):
    if not value:
        return ''

    month = value.month
    day = value.day
    hour = value.hour
    minute = value.minute

    period = '오전' if hour < 12 else '오후'
    hour_12 = hour if 0 < hour <= 12 else (hour - 12 if hour > 12 else 12)

    return f"{month}월 {day}일 {period} {hour_12}:{minute:02d}"