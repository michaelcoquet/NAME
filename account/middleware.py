from django.shortcuts import render
from social_core.exceptions import AuthAlreadyAssociated
from social_django.middleware import SocialAuthExceptionMiddleware


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
