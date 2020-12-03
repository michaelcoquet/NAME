"""CMPT 370 Group 5 Project: NAME (Nearly Analogous Music Engine)
    Summary:  is a piece of software to compare songs using the Spotify API. NAME will help the
              user find other similar songs to the ones they are interested in, as well as
              detailed info about their favorite songs.
"""
import os
import pymongo
from name.backend_classes.spotify_api_manager import SpotifyAPIManager
from name.backend_classes.persistent_storage import PersistentStorage


class User:
    """
    A class to represent a user of the app
    """
    def __init__(self):
        """
        song: A song object containing the data of the song from Spotify
        """

        #instantiate the spotify api manager
        self.spotify_manager = None

        # for the database
        self.persistent_storage = None

        self.spotify_id = None
        self.has_account = False
        self.current_playlist = None # load local text file for a guest otherwise will load when
                                     # account is linked
        self.groups = []

    def __str__(self):
        """
        A string representation of the object
        """

    # def __repr__(self):


    # def __iter__(self):


    def create_group(self, group):
        """ creates a new group to add to the users entry in the database, the current user is
            the owner
        """
        self.groups.append(group)
        if self.persistent_storage.create_new_group(group.group_name,
            self.persistent_storage.spotify_id, group.member_list) == False:
            return False
        else:
            return True

    def get_account_id(self):
        """ return the users spotify id if theyre a member
        """
        if self.has_account:
            return self.spotify_id

    def has_account(self):
        """ returns true if the user doesn't have a spotify account linked, false if they do
        """
        return self.has_account

    def link_spotify_account(self):
        """ just wrap the spotify api manager

        Returns:
            bool : True if successful, false otherwise
        """
        # TODO: do this in a seperate thread to avoid crashing if the login fails
        self.spotify_manager = SpotifyAPIManager()
        if self.spotify_manager.link_spotify_account() == True:
            self.has_account = True
            self.spotify_id = self.spotify_manager.get_user_id()

            # must instantiate the db here now that we have a spotify id
            self.persistent_storage = PersistentStorage(self.spotify_id)

            # search the database for this user, if entry exists deserialize its entry into this
            # object if entry doesnt exist then create a new one
            if self.persistent_storage.check_if_user_exists():
                # deserialize here
                self.current_playlist = self.persistent_storage.get_current_playlist()
                self.groups = self.persistent_storage.get_users_groups()
                # check if they have any group invites already
                if self.persistent_storage.find_invites():
                    print("found some invites")
                else:
                    print("no invites")
            else:
                self.persistent_storage.create_new_member()
                # check if they have any group invites already
                if self.persistent_storage.find_invites():
                    print("found some invites")
                else:
                    print("no invites")
            return True
        else:
            return False

    def find_group_invites(self):
        """ search for groups that I am a member of but dont yet show up in this objects group
            list, indicating an unaccepted group invite
        """


    def logout(self):
        """ log out the current user
        """
        if self.has_account:
            self.has_account = 0
            self.spotify_manager = None
            if os.path.exists(".cache"):
                os.remove(".cache")