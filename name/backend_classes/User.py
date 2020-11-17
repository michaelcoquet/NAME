class User:
    """Base class for the Member and Guest classes"""

    def __init__(self, account):
        """Account: The user's Spotify account"""
        self.account = account

    def has_spotify_account(self):
        """If account is not null, User is a Member and returns
        True, otherwise returns False
        """
        return self.account is not None

    def is_guest(self):
        """If account is null, User is a Guest and returns
        True, otherwise returns False
        """
        return self.account is None








