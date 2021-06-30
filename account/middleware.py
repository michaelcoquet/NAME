from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import logout
from social_core.exceptions import AuthAlreadyAssociated
from social_django.middleware import SocialAuthExceptionMiddleware


class AuthAlreadyAssociatedMiddleware(SocialAuthExceptionMiddleware):
    """Redirect users to desired-url when AuthAlreadyAssociated exception occurs."""

    def process_exception(self, request, exception):
        if isinstance(exception, AuthAlreadyAssociated):
            if request.backend.name == "spotify":
                message = "This spotify account is already in use."
                logout(request)
                return redirect("/social-auth/login/spotify/")
