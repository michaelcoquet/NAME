from django.core import serializers
from spotify.tasks import scrape_user_profile, scrape_tracks


def user_profile(social_query):
    social_json = serializers.serialize("json", social_query.only())
    return scrape_user_profile.delay(social_json)


# see docstring for scrape_tracks()
def track_data(csv_path):
    return scrape_tracks(csv_path)
