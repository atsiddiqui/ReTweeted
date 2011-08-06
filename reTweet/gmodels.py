__author__ = 'Shwetanka'

from google.appengine.ext import db

class User(db.Model):
    username = db.StringProperty(required=True, verbose_name='Username')
    user_id = db.StringProperty(required=True)
    first_name = db.StringProperty(verbose_name='First Name')
    last_name = db.StringProperty(verbose_name='Last Name')
    email = db.EmailProperty(verbose_name='Email')
    oauth_token = db.StringProperty()
    oauth_secret = db.StringProperty()
