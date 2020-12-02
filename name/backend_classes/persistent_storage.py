"""CMPT 370 Group 5 Project: NAME (Nearly Analogous Music Engine)
    Summary:  is a piece of software to compare songs using the Spotify API. NAME will help the
              user find other similar songs to the ones they are interested in, as well as
              detailed info about their favorite songs.
"""
import os
import base64
import json
from spotify_api_manager import SpotifyAPIManager


class PersistentStorage:
    """ class to handle the storage of data in json format (see wiki persistent storage)
    """

    def __init__(self, unencrypted_spotify_id):
        """ unencrypted_spotify_id : the users unencrypted spotify ID, this class will encrypt
                                     the id before saving to disk for privacy concerns
        """
        self.unencrypted_spotify_id = unencrypted_spotify_id
        self.encrypted_spotify_id = self.encrypt(unencrypted_spotify_id)

        # init database
        self.init_json_file()

    def init_json_file(self):
        """ this will check if the json file already exists and open it for reading/writing if
            it does, and create it if doesn't already exist
        """
        if os.path.exists("database.json") == False:
            data = [
                {
                "encrypted_spotify_id": self.encrypted_spotify_id,
                "playlists": [],
                "groups": []
                }
            ]
            with open("database.json", "w") as json_file:
                json.dump(data, json_file)

    def create_new_member(self):
        """ This will initiate a new user in the database, this will simply create a blank entry
            with a corresponding spotify id and will need to be loaded with users data in
            another step
        """
        if self.check_if_user_exists() == False:
            new_data ={
                "encrypted_spotify_id": self.encrypted_spotify_id,
                "playlists": [],
                "groups": []
                }
            with open("database.json", "r+") as json_file:
                data = json.load(json_file)
                data.append(new_data)
                json_file.seek(0)
                json.dump(data, json_file)

    def check_if_user_exists(self):
        """ check if the user already has information stored

        Returns:
            exists (bool): true if user exists false otherwie
        """
        found = False
        with open("database.json") as json_file:
            data = json.load(json_file)
            for d in data:
                if(d["encrypted_spotify_id"] == self.encrypted_spotify_id):
                    found = True

        return found

    def load_all_playlists(self, playlists):
        """ puts all the playlists in the input into the users persistent storage
            should be used with the spotify api managers get_users_playlists() to load all the
            users playlist objects into the database

        Args:
            playlists (Playlist[]): list of playlist objects to store
        """
        if self.check_if_user_exists():
            with open("database.json") as json_file:
                data = json.load(json_file)
                for d in data:
                    if(d["encrypted_spotify_id"] == self.encrypted_spotify_id):
                        # found the correct users file now load their playlists with the input
                        # list
                        d["playlists"] = self.serialize_user_data(playlists)
                        # save it back to the json
                        with open("database.json", "w") as json_write:
                            json.dump(data, json_write)

                        break
        else:
            print("error: user doesnt exist yet, create it first")

    def serialize_user_data(self, playlists):
        serialized_user = {}
        serialized_user["encrypted_spotify_id"] = self.encrypted_spotify_id
        serialized_user["playlists"] = []
        serialized_user["groups"] = []
        playlist_strings = []
        for playlist in playlists:
            playlist_string = {}
            playlist_string["playlist_name"] = playlist.playlist_name
            playlist_string["playlist_id"] = playlist.playlist_id
            # serialize the songs now
            song_strings = []
            for song in playlist.songs:
                song_string = {}
                song_string["song_name"] = song.song_name
                song_string["song_id"] = song.song_id
                song_strings.append(song_string)
            # put the songs in the json format
            playlist_string["songs"] = song_strings
            playlist_strings.append(playlist_string)

        return playlist_strings

    def check_if_playlist_exists(self, playlist_id):
        """ check if a the given playlist id exists for a user in either spotify or json

        Args:
            playlist_id(string): the spotify id for the desired playlist
        """
        return 1

    def check_if_group_exists(self, group_id):
        """ check if the given group exists or not

        Args:
            group_id (integer): the id for the desired group
        """
        return 1

    def save_new_playlist(self, new_playlist):
        """ save a new playlist to the users file

        Args:
            new_playlist(Playlist): the new playlist to be saved to the users file
        """
        return 1

    def update_playlist(self, playlist_id):
        """ update a playlist in the users file

        Args:
            playlist_id(string): the spotify id for the desired playlist
        """
        return 1

    def get_users_playlists(self):
        """ return all the users playlists on file

        Returns:
            playlists (Playlist[]): list of all the users Playlist on file
        """
        return 1

    def get_playlist(self, playlist_id):
        """ return a given playlist if it exists

        Args:
            playlist_id (string): the id of the desired playlsit

        Returns:
            output_playlist (Playlist): the desired Playlist object
        """
        return 1

    def save_new_group(self, new_group):
        """ save a new group to the users file

        Args:
            new_group(Group): the new group to be save to the users file
        """
        return 1

    def update_group(self, group_id):
        """ update the given group

        Args:
            group_id (integer): the groups id to be updated
        """
        return 1

    def get_users_groups(self):
        """ return all the users groups on file

        Returns:
            groups (Group[]): list of all Group objects on file
        """
        return 1

    def get_group(self, group_id):
        """ return the given group if it exists

        Args:
            group_id (integer): the desired groups id

        Returns:
            output_group (Group): the desired Group object
        """
        return 1

    def encrypt(self, input):
        """ function to help encrypt the data that needs encrypting

        Args:
            input (string): the unencrypted input string to be encrypted

        Returns:
            output (string): the enrypted input string
        """
        return base64.b64encode(input.encode("utf-8")).decode("utf-8")

    def decrypt(self, input):
        """ function to help decrypt the data thats needs decrypting

        Args:
            input (string): the encrypted input string

        Returns:
            output (string): the unencrypted input string
        """
        return base64.b64decode(input.encode("utf-8")).decode("utf-8")


# testing

# need to be logged into the test spotify account: cmpt370.group5@gmail.com account for these
# tests to pass
sp_manager = SpotifyAPIManager()
sp_manager.link_spotify_account()

sp_id = sp_manager.get_user_id()

ps = PersistentStorage(sp_id)

    # test 0: encrypt()
unencrypted_text = "encrypt this testing message"
encrypted_text = ps.encrypt(unencrypted_text)

assert(encrypted_text != unencrypted_text)

    # test 1: decrypt()
assert(ps.decrypt(encrypted_text) == unencrypted_text)

    # test 2: decrypting again after reinitialization
ps = PersistentStorage(sp_id)
assert(ps.decrypt(encrypted_text) == unencrypted_text)

    # test 3: create new member
ps.create_new_member()

found = 0
with open("database.json") as json_file:
    data = json.load(json_file)
    for d in data:
        if(d["encrypted_spotify_id"] == ps.encrypt(sp_id)):
            found = 1

assert(found)

    # test 4: check if user exists
assert(ps.check_if_user_exists())

    # test 5: load_all_playlists
playlists = sp_manager.get_member_playlists()

ps.load_all_playlists(playlists)

found = 0
with open("database.json") as json_file:
    data = json.load(json_file)
    for d in data:
        if d["encrypted_spotify_id"] == ps.encrypt(sp_id):
            for playlist in d["playlists"]:
                if(playlist["playlist_name"] == "testing0"):
                    found = 1
assert(found)

