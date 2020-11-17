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
    """Class which is used by a user with no Spotify account"""


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


class Member(User):
    """Class which is used by User's who have successfully signed into
       a Spotify account
    """

    def __init__(self, account):
        """account: The User's Spotify account"""
        super().__init__(account)
        self.stored_playlists = []
        self.spotify_id = ""  # Get from spotify api when it is set up
        self.group_ids = []
        self.group_list = []

        # playlists and groups from previous sessions will be added here
        # if they exist, once the systems are created


    def link_account(self):
        return 0

    def verify_link(self):
        return False

    def create_group(self):
        """Once the group class is created, call it here
        to create a new group and add it to group_list
        """
        return None

    def get_account_id(self):
        """Returns the user's Spotify ID"""
        return self.spotify_id

    def get_group_list(self):
        """Get list of groups the user is currently a member of"""
        return self.group_list

    def get_playlist(self, name):
        """Search through stored playlists and return the playlist if
        found, otherwise return None
        name: Name of desired playlist
        """

        for playlist in self.stored_playlists:
            if playlist.name == name:
                return playlist

        return None

    def create_playlist(self, name):
        """Create a new playlist with the desired name and add to
        the User's stored playlists
        """
        # This should be moved to User class, as Guest can create
        # playlists as well

        # create new playlist object with name
        # add desired songs
        # add to stored_playlists
        pass

    def get_listening_habits(self, habits):
        """Get the desired User's listening habits
        habits: a list of desired habits to get
        """
        # Get the user's listening habits from api
        listening_habits = []
        
        # Return the raw data
        return listening_habits


