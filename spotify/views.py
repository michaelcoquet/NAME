import requests, json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def get_token(social):
    return social.access_token


@login_required
def get_followers(social):
    url = "https://api.spotify.com/v1/me"
    headers = {
        "content-type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer %s" % (get_token(social)),
    }
    response = json.loads(requests.request("GET", url, headers=headers).text)
    return response["followers"]["total"]
