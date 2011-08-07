from reTweet.gmodels import User

from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect

from tweet import PostTweet

from utils import pagination

tweet = PostTweet(consumer_key, consumer_secret, access_token_key=None, access_token_secret=None)        

def _process_tweet(tweet_list):
    tweet_dict = {}
    for i in tweet_list:
        if tweet_dict.get(i[1]) is None:
            tweet_dict.update({i[1]:1})
        else:
            tweet_dict.update({i[1]:tweet_dict.get(i[1]) + 1})

    import operator
    return max(tweet_dict.iteritems(), key=operator.itemgetter(1))

def home_page(request):

    context = RequestContext(request)
    if request.method=='POST':
        auth_url = tweet.get_authorize_url(request)
        return HttpResponseRedirect(auth_url)

    return render_to_response('index.html', context_instance=context)

def tweet_response(request):
    context = RequestContext(request)
    try:
        api = tweet._authenticate(request)
    except:
        return render_to_response('index.html', context_instance=context)
        
    tweet_list = []
    temp_list = []
    try:
        re_tweets = api.GetUserRetweets(count=100)
        following_list = api.GetFriends()
    except:
        return render_to_response('index.html', context_instance=context)

    if len(re_tweets) == 0:
        context['error'] = 'You never retweets.'
        return render_to_response('index.html', context_instance=context)

    [tweet_list.append(re.text) for re in re_tweets]
    [temp_list.append((i.split(': ')[-1], i.split(': ')[0].split(' ')[1])) for i in tweet_list]
    love_owner = _process_tweet(temp_list)
    page = request.GET.get('page')
    if page is not None:
        context['page'] = page

    context['following'] = [following.screen_name for following in following_list] 
    context['top_tweeted'] = love_owner[0]
    context['top_tweeted_count'] = love_owner[1]
    context['re_tweets'] = pagination(request, re_tweets, 25)
    context['screen_name'] = request.session['screen_name']
    return render_to_response('index.html', context_instance=context)

def twitter_logout(request):
    #logout(request)
    try:
        del request.session['user']
    except:
        pass

    return HttpResponseRedirect('/')

def test(request):
    context = RequestContext(request)
    return render_to_response('index1.html', context_instance=context)
