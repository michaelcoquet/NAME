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
    def __init__(self, group_name, owner_id, invite_list, member_list):
        """ initialize all fields

        group (json): the group representation from the database
        """
        self.group_id = None # this will be assigned
        self.group_name = group_name
        self.owner_id = owner_id

        self.member_list = member_list

        self.invite_list = invite_list

        self.group_playlists = []

    def __iter__(self):
        member_string = [member for member in self.member_list]
        invite_string = [invite for invite in self.invite_list]
        playlist_string = [plist for plist in self.playlists]
        group_string = {
            "group_id": self.group_id,
            "group_name": self.group_name,
            "owner_id": self.owner_id,
            "invite_list": invite_string,
            "member_list": member_string,
            "playlists": playlist_string
        }
        yield from group_string.items()

    def assign_id(self, id):
        self.group_id = id

    def new_playlist(self):
        return 1

    def update_playlist(self):
        return 1

    def update_playlists(self, playlists):
        """ give a list of playlist objects to replace group_playlists with
            helpful for making new group objects or loading them from storage

        Args:
            playlists (Playlist[]): new list of group playlists
        """
        self.group_playlists = playlists

    def invite_members(self, member_ids):
        """ send invites to the following members

        Args:
            member_ids (int64[]): list of member ids to send invites to
        """
        for member_id in member_ids:
            self.invite_list.append(member_id)

    def accept_invite(self, member_id):
        """ the member with member_id accepted the invitation, take action

        Args:
            member_id (int64): member_id who accepted the invitation to this group
        """
        # remove the member from the invite list
        for id in self.invite_list:
            if id == member_id:
                self.invite_list.remove(id)
                # add them to the member list
                self.member_list.append(id)

    def decline_invite(self, member_id):
        """ the member with emmber_id declined the invitation, take action

        Args:
            member_id (int64): member_id who declined the invitation to this group
        """
        # remove the member from the invite list, but dont add them to the member list
        return 1

    def add_member(self, member_id):
        """ add a member to the list

        Args:
            member_id (string): unencrypted spotify id
        """
        self.member_list.append(member_id)

    def member_exists(self, member_id):
        """ check if the member already exists in the list
        """
        for member in self.member_list:
            if member == member_id:
                return True

        return False
