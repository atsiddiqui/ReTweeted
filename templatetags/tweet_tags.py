from django.template import Library

register = Library()

@register.filter
def get_owner(string):
    return string.split(': ')[0].split(' ')[1]

@register.filter
def get_text(string):
    return string.split(': ')[-1]

@register.filter
def get_time(string):
    return ' '.join(string.split(' ')[:3])

@register.filter
def clean_name(string):
    return string[1:]
