import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

"""CMPT 370 Group 5 Project: NAME (Nearly Analogous Music Engine)
    Summary:  is a piece of software to compare songs using the Spotify API. NAME will help the
              user find other similar songs to the ones they are interested in, as well as
              detailed info about their favorite songs.
"""
class Group:
    """
    A class to represent a group of freinds
    """
    def __init__(self, group_name, owner_id, member_list):
        """ initialize all fields

        group (json): the group representation from the database
        """
        self.group_id = None # this will be assigned
        self.group_name = group_name
        self.owner_id = owner_id

        self.member_list = member_list
        self.group_playlists = []

    def __iter__(self):
        member_string = [member for member in self.member_list]
        playlist_string = [plist for plist in self.group_playlists]
        group_string = {
            "group_id": self.group_id,
            "group_name": self.group_name,
            "owner_id": self.owner_id,
            "member_list": member_string,
            "group_playlists": playlist_string
        }
        yield from group_string.items()

    def assign_id(self, id):
        self.group_id = id

    def new_playlist(self):
        return 1

    def update_playlist(self):
        return 1

