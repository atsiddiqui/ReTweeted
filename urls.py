from django.conf.urls.defaults import *
import os
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from views import home_page, tweet_response, twitter_logout

urlpatterns = patterns('',
    # Example:
    url(r'^$', home_page, name='home-page'),
    url(r'tweet/$', tweet_response, name='tweet-response'),
    url(r'logout/$', twitter_logout, name='twitter-logout'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', 
       {'document_root': os.path.join(os.path.dirname(__file__), "static")}),

)
