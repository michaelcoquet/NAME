import json, base64, requests, webbrowser
from django.shortcuts import redirect, render
from requests.api import head
from social_core.exceptions import AuthAlreadyAssociated
from social_django.middleware import SocialAuthExceptionMiddleware
from django.conf import settings


class AuthAlreadyAssociatedMiddleware(SocialAuthExceptionMiddleware):
    """Redirect users to desired-url when AuthAlreadyAssociated exception occurs."""

    def process_exception(self, request, exception):
        if isinstance(exception, AuthAlreadyAssociated):
            if request.backend.name == "spotify":
                # The account the user is trying to log into
                # is already associated with another account
                # ask them if they would like to log out and
                # log back into the other account, or stay
                # logged into this account
                response = render(request, "account/already_exists.html")
                return response
        # else:
        #     url = "https://accounts.spotify.com/authorize"
        #     strategy = load_strategy()
        #     name = "spotify"
        #     redirect_uri = settings.SPOTIFY_REDIRECT_URI
        #     backend = load_backend(
        #         strategy=strategy, name=name, redirect_uri=redirect_uri
        #     )
        #     params = {
        #         "client_id": settings.SOCIAL_AUTH_SPOTIFY_KEY,
        #         "response_type": "code",
        #         "redirect_uri": settings.SPOTIFY_REDIRECT_URI,
        #         "scope": " ".join(settings.SOCIAL_AUTH_SPOTIFY_SCOPE),
        #         "state": request.GET.get("state"),
        #     }
        #     response = requests.get(url=url, params=params)
        #     print(response)
        #     url = "https://accounts.spotify.com/api/token"
        #     grant_type = "authorization_code"
        #     code = request.GET.get("code")
        #     redirect_uri = settings.SPOTIFY_REDIRECT_URI
        #     post_body = {
        #         "grant_type": str(grant_type),
        #         "code": str(code),
        #         "redirect_uri": str(redirect_uri),
        #         "client_id": str(settings.SOCIAL_AUTH_SPOTIFY_KEY),
        #         "client_secret": str(settings.SOCIAL_AUTH_SPOTIFY_SECRET),
        #     }
        #     auth_str = "{0}:{1}".format(
        #         settings.SOCIAL_AUTH_SPOTIFY_KEY, settings.SOCIAL_AUTH_SPOTIFY_SECRET
        #     )
        #     b64_auth_str = base64.urlsafe_b64encode(auth_str.encode("UTF-8")).decode(
        #         "ascii"
        #     )
        #     post_head = {
        #         "Authorization": "Basic {0}".format(b64_auth_str),
        #         "Content-Type": "application/x-www-form-urlencoded",
        #     }
        #     response = requests.post(url=url, data=post_body, headers=post_head)
        #     print(response)
