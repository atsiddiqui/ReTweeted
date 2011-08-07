
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
