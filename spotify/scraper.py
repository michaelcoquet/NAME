from django.core import serializers
from django.contrib.auth.decorators import login_required
from spotify.tasks import get_user_profile
from account.models import Profile


# TODO: Implement batch api calls to improve performance
# TODO: Unit testing
def user_profile(social_query):
    social_json = serializers.serialize("json", social_query.only())
    return get_user_profile.delay(social_json)
