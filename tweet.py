import twitter
import urlparse
import oauth2 as oauth
import dbapi

request_token_url='https://api.twitter.com/oauth/request_token'
authorize_url='https://api.twitter.com/oauth/authorize'
access_token_url='https://api.twitter.com/oauth/access_token'

class PostTweet:

    def __init__(self, consumer_key, consumer_secret, access_token_key=None, access_token_secret=None):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token_key = access_token_key
        self.access_token_secret = access_token_secret
        self.consumer=oauth.Consumer(consumer_key, consumer_secret)

    def _authenticate(self, request):
            
        user = request.session.get('user')
        if user:
            p_obj = dbapi.get_profile(user)
            if  p_obj is not None:
                return twitter.Api(consumer_key=self.consumer_key, consumer_secret=self.consumer_secret, \
                                       access_token_key=p_obj.oauth_token, access_token_secret=p_obj.oauth_secret)

        token = oauth.Token(request.session['request_token']['oauth_token'],
                            request.session['request_token']['oauth_token_secret'])
        client = oauth.Client(self.consumer, token)
        resp, content = client.request(access_token_url, "POST")
        access_token_key = dict(urlparse.parse_qsl(content))

        screen_name = access_token_key['screen_name']
        request.session['screen_name'] = screen_name

        access_token = access_token_key['oauth_token']
        access_token_secret  = access_token_key['oauth_token_secret']

        user = dbapi.get_user(screen_name)
        if user is None:
            user = dbapi.create_user(screen_name,'%s@twitter.com' % screen_name, access_token_secret)
            dbapi.create_profile(user, access_token, access_token_secret) 

        request.session['user'] = user
        return twitter.Api(consumer_key=self.consumer_key, consumer_secret=self.consumer_secret, \
                               access_token_key=access_token, access_token_secret=access_token_secret)

    def get_authorize_url(self, request):
        client=oauth.Client(self.consumer)
        resp, content = client.request(request_token_url, "GET")
        request_token = dict(urlparse.parse_qsl(content))
        request.session['request_token'] = dict(urlparse.parse_qsl(content))
        return '%s?oauth_token=%s' % (authorize_url, request_token['oauth_token'])
