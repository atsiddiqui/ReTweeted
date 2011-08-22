import logging
from reTweet.gmodels import User
from google.appengine.api import memcache
from django.utils import simplejson
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect

from tweet import PostTweet
from twitter import Status
from utils import pagination, non_followers

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
        request.session['followme'] = request.POST.get('follow-me')
        auth_url = tweet.get_authorize_url(request)
        return HttpResponseRedirect(auth_url)

    return render_to_response('home.html', context_instance=context)

def tweet_response(request):
    context = RequestContext(request)

    try:
        api = tweet._authenticate(request)
        follow_me = request.session.get('followme', None)
        user = request.session.get('user', None)
        try:
            if follow_me is not None and user is not None:
                api.CreateFriendship('retweetstats')
        except:
            pass
    except:
        return render_to_response('home.html', context_instance=context)
        
    tweet_list = []
    temp_list = []
    try:
        re_tweets = memcache.get("retweetsby")
        logging.info(re_tweets)
        if re_tweets is None:
            first_set_tweets = api.GetUserRetweets(count=100)
            if len(first_set_tweets) > 0 and len(first_set_tweets) > 100:
                last_retweet_id = first_set_tweets[-1].id
                next_set_retweets = api.GetUserRetweets(count=30, max_id = last_retweet_id)
                re_tweets = first_set_tweets + next_set_retweets
            else:
                re_tweets = first_set_tweets
            memcache.add("retweetsby", re_tweets, 10)
            logging.error("Memcache set failed.")

        following_list = memcache.get("following")
        if following_list is None:
            following_list = api.GetFriends()
            memcache.add("following", following_list, 10)

        follower_list = memcache.get("followers")
        if follower_list is None:
            follower_list = api.GetFollowers()
            memcache.add("followers", follower_list, 10)

    except:
        return render_to_response('home.html', context_instance=context)

    if len(re_tweets) == 0:
        context['error'] = 'You never retweets.'
        return render_to_response('index.html', context_instance=context)

    [tweet_list.append(re.text) for re in re_tweets]
    [temp_list.append((i.split(': ')[-1], i.split(': ')[0].split(' ')[1])) for i in tweet_list]
    love_owner = _process_tweet(temp_list)
    page = request.GET.get('page')
    if page is not None:
        context['page'] = page
 
    context['following'] = [str(following.screen_name) for following in following_list] 
    context['follower'] = len(follower_list)
    context['top_tweeted'] = love_owner[0]
    context['top_tweeted_count'] = love_owner[1]
    context['re_tweets'] = pagination(request, re_tweets, 25)
    context['screen_name'] = request.session['screen_name']
    
    return render_to_response('index.html', context_instance=context)

def retweeted_of_user(request, count=100):
    context = RequestContext(request)
    try:
        api = tweet._authenticate(request)
        parameters = {}
        parameters['count'] = count
        json = api._FetchUrl('http://api.twitter.com/1/statuses/retweets_of_me.json?include_entities=true', \
                                 parameters = parameters)
        data = api._ParseAndCheckTwitter(json)
        re_tweets = [Status.NewFromJsonDict(x) for x in data]

        following_list = memcache.get("following")
        if following_list is None:
            following_list = api.GetFriends()
            memcache.add("following", following_list, 10)

        follower_list = memcache.get("followers")
        if follower_list is None:
            follower_list = api.GetFollowers()
            memcache.add("followers", follower_list, 10)

    except:
        return render_to_response('home.html', context_instance=context)

    page = request.GET.get('page')
    if page is not None:
        context['page'] = page

    context['following'] = [str(following.screen_name) for following in following_list]
    context['follower'] = len(follower_list)

    context['re_tweets'] = pagination(request, re_tweets, 25)
    context['screen_name'] = request.session['screen_name']
    return render_to_response('retweeted-by.html', context_instance=context)

def get_friends(request):
    context = RequestContext(request)
    try:
        api = tweet._authenticate(request)

        following_list = memcache.get("following")
        if following_list is None:
            following_list = api.GetFriends()
            memcache.add("following", following_list, 10)
        
        follower_list = memcache.get("followers")
        if follower_list is None:
            follower_list = api.GetFollowers()
            memcache.add("followers", follower_list, 10)
    except:
        return render_to_response('home.html', context_instance=context)

    context['following'] = [str(following.screen_name) for following in following_list]
    context['follower'] = len(follower_list)


    context['friends'] = following_list
    context['screen_name'] = request.session['screen_name']
    return render_to_response('friends.html', context_instance=context)

def get_followers(request):
    context = RequestContext(request)
    api = tweet._authenticate(request)

    following_list = memcache.get("following")
    if following_list is None:
        following_list = api.GetFriends()
        memcache.add("following", following_list, 10)
        
    follower_list = memcache.get("followers")
    if follower_list is None:
        follower_list = api.GetFollowers()
        memcache.add("followers", follower_list, 10)
    
    context['following'] = [str(following.screen_name) for following in following_list]
    context['follower'] = len(follower_list)


    context['friends'] = follower_list
    context['screen_name'] = request.session['screen_name']
    return render_to_response('followers.html', context_instance=context)

def get_non_followers(request):
    context = RequestContext(request)
    api = tweet._authenticate(request)

    following_list = memcache.get("following")
    if following_list is None:
        following_list = api.GetFriends()
        memcache.add("following", following_list, 10)
        
    follower_list = memcache.get("followers")
    if follower_list is None:
        follower_list = api.GetFollowers()
        memcache.add("followers", follower_list, 10)
    
    context['following'] = [str(following.screen_name) for following in following_list]
    context['follower'] = len(follower_list)

    non_follower = non_followers(follower_list, following_list)
    context['friends'] = non_follower
    context['friends_count'] = len(non_follower)
    context['screen_name'] = request.session['screen_name']
    return render_to_response('non-followers.html', context_instance=context)

def friend_unfollow(request):
    if request.is_ajax():
        if request.method == "POST":
            screen_name = request.POST.get('screen_name')
            try:
                api = tweet._authenticate(request)
                api.DestroyFriendship(screen_name)
            except:
                return HttpResponse(simplejson.dumps({'success': 'false'}), mimetype='application/json')
        return HttpResponse(simplejson.dumps({'success': 'true'}), mimetype='application/json')

def friend_follow(request):
    if request.is_ajax():
        if request.method == "POST":
            screen_name = request.POST.get('screen_name')
            try:
                api = tweet._authenticate(request)
                api.CreateFriendship(screen_name)
            except:
                return HttpResponse(simplejson.dumps({'success': 'false'}), mimetype='application/json')
        return HttpResponse(simplejson.dumps({'success': 'true'}), mimetype='application/json')

def update_status(request):
    if request.is_ajax():
        if request.method == "POST":
            message = request.POST.get('message')
            try:
                api = tweet._authenticate(request)
                api.PostUpdate(message)
            except:
                return HttpResponse(simplejson.dumps({'success': 'false'}), mimetype='application/json')
        return HttpResponse(simplejson.dumps({'success': 'true'}), mimetype='application/json')

def twitter_logout(request):
    #logout(request)
    try:
        del request.session['user']
    except:
        pass

    return HttpResponseRedirect('/')

