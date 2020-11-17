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


class Guest(User):

    def __init__(self):
        """playList: a temporary Play list for the guest"""
        super().__init__(None) 
        self.playlist = None


    def save_temp_playlist(playlist):
        """Saves a a guest's playlist as a text file"""

        #When persistant storage is set up
        #this will export a text file
        
        return None

    def set_temp_playlist(playlist):
        """Sets a temporary playlist for the Guest"""
        self.playlist = playlist






