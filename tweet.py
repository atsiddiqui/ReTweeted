import twitter
import urlparse
import oauth2 as oauth


request_token_url='https://api.twitter.com/oauth/request_token'
authorize_url='https://api.twitter.com/oauth/authorize'


class PostTweet:

    def __init__(self, consumer_key, consumer_secret, access_token_key, access_token_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token_key = access_token_key
        self.access_token_secret = access_token_secret

    def _authenticate(self,):
        return twitter.Api(consumer_key=self.consumer_key, consumer_secret=self.consumer_secret, \
                               access_token_key=self.access_token_key, access_token_secret=self.access_token_secret)

    def get_authorize_url(self,):
        consumer=oauth.Consumer(self.consumer_key, self.consumer_secret)
        client=oauth.Client(consumer)
        resp, content = client.request(request_token_url, "GET")
        request_token = dict(urlparse.parse_qsl(content))
        return '%s?oauth_token=%s' % (authorize_url, request_token['oauth_token'])
