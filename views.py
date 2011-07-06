from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect

from tweet import PostTweet

import twitter
import urllib, urllib2

consumer_key = 'XtPv8lFbMNntm1hE5nzuw'                                                                                                                     
consumer_secret = 'd7pbKZHiyf7qbE2s9nO2PPLqVsQtVBPVzGoH3zN3k'                                                                                              
access_token_key = 
access_token_secret = 

tweet = PostTweet(consumer_key, consumer_secret, access_token_key, access_token_secret)        

def home_page(request):
    context = RequestContext(request)
    if request.method=='POST':
        auth_url = tweet.get_authorize_url()
        return HttpResponseRedirect(auth_url)

    return render_to_response('index.html', context_instance=context)

def tweet_response(request):
    context = RequestContext(request)
    api = tweet._authenticate()
    import pdb;pdb.set_trace()
    return render_to_response('index.html', context_instance=context)
