import time
from django.template import Library

register = Library()

@register.filter
def get_owner(string):
    return string.split(': ')[0].split(' ')[1]

@register.filter
def get_text(string):
    temp = string.split(': ')
    if len(temp) > 0:
        temp.pop(0)
        string = ': '.join(temp)
    return string

@register.filter
def get_time(string):
    try:
        time_struct = time.strptime(string, "%a %b %d %H:%M:%S +0000 %Y")
        return '%s/%s/%s' %(time_struct.tm_mday, time_struct.tm_mon, time_struct.tm_year)
    except:
        return ' '.join(string.split(' ')[:3])

@register.filter
def clean_name(string):
    return string[1:]

@register.filter
def get_count(count, page):
    if page:
        return int(count) + (int(page) - 1)*25
    return

@register.filter
def get_followers(screen_name, following_list):
    if following_list:
        if screen_name in following_list:
            return False
        else:
            return True
    return
