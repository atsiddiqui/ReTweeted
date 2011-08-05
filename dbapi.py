from models import Profile
from django.contrib.auth.models import User

def get_profile(user):
    try:
        return Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        return None
    
def get_user(username):
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        return None

def create_user(username, twitter_name, secret_key):
    return User.objects.create_user(username, twitter_name, secret_key)

def create_profile(user, oauth_token, secret_token):
    profile = Profile()
    profile.user = user
    profile.oauth_token = oauth_token
    profile.oauth_secret = secret_token
    profile.save()
    return

