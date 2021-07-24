from django.core import serializers
from spotify.tasks import scrape_user_profile


# TODO: Implement batch api calls to improve performance
# TODO: Unit testing
def user_profile(social_query):
    social_json = serializers.serialize("json", social_query.only())
    return scrape_user_profile(social_json)
