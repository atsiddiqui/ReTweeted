
from django.core.paginator import Paginator, InvalidPage, EmptyPage

def pagination(request, tweets, result_per_page):
    paginator = Paginator(tweets, result_per_page)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        tweets = paginator.page(page)
    except (EmptyPage, InvalidPage):
        tweets = paginator.page(paginator.num_pages)

    return tweets

def non_followers(followers_list, following_list):
    x = []
    [x.append(i) for i in following_list if i.AsDict().get('screen_name') \
         not in [j.AsDict().get('screen_name') for j in followers_list]]
    return x
