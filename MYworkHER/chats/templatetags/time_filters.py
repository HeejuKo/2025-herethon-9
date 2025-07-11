from django import template
from django.utils import timezone

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

@register.filter
def smart_chat_time(value):
    if not value:
        return ''

    now = timezone.localtime()
    value = timezone.localtime(value)  # timezone-aware 처리

    if value.date() == now.date():
        # 오늘이면 → 오전/오후 시:분
        hour = value.hour
        minute = value.minute
        period = '오전' if hour < 12 else '오후'
        hour_12 = hour if 0 < hour <= 12 else (hour - 12 if hour > 12 else 12)
        return f"{period} {hour_12}:{minute:02d}"
    else:
        # 오늘이 아니면 → 7월 10일 형식
        return f"{value.month}월 {value.day}일"