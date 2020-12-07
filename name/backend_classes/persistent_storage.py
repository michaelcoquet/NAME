"""CMPT 370 Group 5 Project: NAME (Nearly Analogous Music Engine)
    Summary:  is a piece of software to compare songs using the Spotify API. NAME will help the
              user find other similar songs to the ones they are interested in, as well as
              detailed info about their favorite songs.
"""
import os
import base64
import json
import pymongo
from name.backend_classes.spotify_api_manager import SpotifyAPIManager
from name.backend_classes.playlist import Playlist
from name.backend_classes.group import Group
from name.backend_classes.song import Song
from name.backend_classes.song import Artist
from name.backend_classes.song import Album
from name.backend_classes.song import SongDetails


class PersistentStorage:
    """ class to handle the storage of data in json format (see wiki persistent storage)
    """

    def __init__(self, spotify_id):
        """ unencrypted_spotify_id : the users unencrypted spotify ID, this class will encrypt
                                     the id before saving to disk for privacy concerns
        """
        self.spotify_id = spotify_id

        # init database
        self.init_mongodb()

    def init_mongodb(self):
        """ this will check if the json file already exists and open it for reading/writing if
            it does, and create it if doesn't already exist
        """
        mdb_str = "mongodb+srv://cmpt370group5:pennywise_1640@namecluster.8pmis.mongodb.net/use\
r_db?retryWrites=true&w=majority"
        try:
            self.client = pymongo.MongoClient(mdb_str)
        except Exception as e:
            print(e)
            exit()

        self.db = self.client.user_db
        self.collection = self.db.user_collection

    def create_new_member(self):
        """ This will initiate a new user in the database, this will simply create a blank entry
            with a corresponding spotify id and will need to be loaded with users data in
            another step
        """
        if self.check_if_user_exists() == False:
            new_data = {
                "spotify_id": self.spotify_id,
                "current_playlist": {},
            }

            self.collection.insert_one(new_data)

    def check_if_user_exists(self):
        """ check if the user already has information stored

        Returns:
            exists (bool): true if user exists false otherwie
        """
        query = { "spotify_id": self.spotify_id }

        if self.collection.count_documents(query, limit = 1) > 0:
            return True
        else:
            return False

    def save_current_playlist(self, playlist_tracks):
        """ puts the active playlist in the input into the users persistent storage

        Args:
            playlist (Playlist): list of playlist objects to store
        """
        if self.check_if_user_exists():
            query = { "spotify_id": self.spotify_id }

            playlist_dict = {"name": "Current Playlist",
                        "owner": {"id": self.spotify_id},
                        "id": "temp_id",
                        "tracks": {"total": 25}}

            playlist = Playlist(playlist_dict, playlist_tracks)

            new_data = { "$set": {
               "spotify_id": self.spotify_id,
               "current_playlist": playlist.convert_to_json(),
            }}

            self.collection.update_one(query, new_data)

    def get_current_playlist(self):
        """ gets the current_playlist entry in the database, then converts to playlist object

        Returns:
            playlist_obj (Playlist): playlist object rebuilt from the json
        """

        query = { "spotify_id": self.spotify_id }

        doc = self.collection.find_one(query)

        return self.playlist_convert_from_json(doc["current_playlist"])

    def check_if_group_exists(self, group_id, group_name):
        """ check if the given group exists or not

        Args:
            group_id (int64): the id for the desired group
        """
        query_0 = { "group_id": group_id }
        query_1 = { "group_name": group_name } # make both id and name unique

        if self.collection.count_documents(query_0) > 0:
            return True
        elif self.collection.count_documents(query_1) > 0:
            return True
        else:
            return False

    def create_new_group(self, group_name, owner_id, invite_list):
        """ save a new empty group to the users file
        """
        query = { "group_counter": {"$exists": "true"} }
        if self.collection.count_documents(query, limit = 1) > 0:
            q = self.collection.find_one(query)
            q["group_counter"] = q["group_counter"] + 1
            self.collection.update_one(query, {"$set": { "group_counter": q["group_counter"]}})
        else:
            return False

        if self.check_if_group_exists(q["group_counter"], group_name) == False:
            new_group_data = {
                "group_id": q["group_counter"],
                "group_name": group_name,
                "owner_id": owner_id,
                "member_list": [owner_id],
                "invite_list": invite_list,
                "playlists": []
            }
            self.collection.insert_one(new_group_data)
        else:
            return False

        return True

    def update_group(self, group):
        """ update the given group

        Args:
            group (Group): the group to be updated
        """
        query = { "group_id": group.group_id }

        new_group_data = { "$set":
            {
                "group_id": group.group_id,
                "group_name": group.group_name,
                "owner_id": group.owner_id,
                "member_list": group.member_list,
                "invite_list": group.invite_list,
                "playlists": group.playlists
            }
        }

        self.collection.update_one(query, new_group_data)

    def get_users_groups(self):
        """ return all the users groups on file

        Returns:
            groups (Group[]): list of all Group objects on file
        """
        groups = []
        if self.check_if_user_exists():
            query = { "member_list": self.spotify_id }
            for group_dict in self.collection.find(query):
                new_group = Group(group_dict["group_name"],
                                  group_dict["owner_id"],
                                  group_dict["invite_list"],
                                  group_dict["member_list"])
                new_group.assign_id(group_dict["group_id"])
                groups.append(new_group)

        return groups

    def get_group(self, group_id):
        """ return the desired group object with given id

        Args:
            group_id (int64): the desired group object to return
        """
        query = { "group_id": group_id }

        doc = self.collection.find_one(query)

        return_group = Group(
            doc["group_name"],
            doc["owner_id"],
            doc["invite_list"],
            doc["member_list"]
        )
        return_group.update_playlists = self.get_group_playlists(group_id)
        return_group.assign_id(doc["group_id"])

        return return_group


    def save_group_playlist(self, group_id, group_name, playlist_tracks, playlist_name):
        """ method to save a new playlist to the group database
        Args:
            group_id: the id of the group
            group_name: the name of the group
            group_playlist: the new Playlist to add to the group's database
        """
        
        if self.check_if_group_exists(group_id, group_name):
            query = { "group_id": group_id }

            playlist_dict = {"name": playlist_name,
                        "owner": {"id": self.spotify_id},
                        "id": "temp_id",
                        "tracks": {"total": len(playlist_tracks)}
                        }

            group_playlist = Playlist(playlist_dict, playlist_tracks)

            new_data = { "$addToSet": {
                        "group_id": group_id,
                        "playlists": group_playlist.convert_to_json()
                        }}

            self.collection.update_one(query, new_data)

    def get_group_playlists(self, group_id):
        """ return the group's created playlists

        Args:
            group_id (int64): the desired group
        """
        query = { "group_id": group_id }

        doc = self.collection.find_one(query)

        return [self.playlist_convert_from_json(playlist) for playlist in doc["playlists"]]

    def find_invites(self):
        """ find group invites for the given member
        """
        query = { "invite_list": self.spotify_id }

        list_of_invites = []

        if self.check_if_user_exists():
            q_curs = self.collection.find(query)
            for doc in q_curs:
                list_of_invites.append({"group_id": doc["group_id"],
                                        "group_name": doc["group_name"]})

        return list_of_invites

    def playlist_convert_from_json(self, json_playlist):
        """ method to convert our playlist class from JSON format
        back to Playlist format

        Args:
            json_playlist: a playlist in json format
        """
        playlist_dict = {}
        playlist_dict["name"] = json_playlist["playlist_name"]
        playlist_dict["owner"] = json_playlist["playlist_owner"]
        playlist_dict["id"] = json_playlist["playlist_id"]
        playlist_dict["tracks"] = {"total": json_playlist["playlist_size"]}

        playlist_songs = []
        for song in playlist_dict["songs"]:
            playlist_songs.append(self.song_convert_from_json(song))

        return Playlist(playlist_dict, playlist_songs)

    def song_convert_from_json(self, json_song):
        """ method to convert our song class from JSON format
        back to Song format

        Args:
            json_song: a song in json format
        """
        song_dict = {}
        song_dict["name"] = json_song["song_name"]
        song_dict["id"] = json_song["id"]
        song_dict["artists"] = [self.artist_convert_from_json(artist) 
                                for artist in json_song["song_artist"]]
        song_dict["album"] = self.album_convert_from_json(json_song["album_details"])

        return Song(song_dict, json_song["song_details"])

    def artist_convert_from_json(self, json_artist):
        """ method to convert our artist class from JSON format
        back to Artist format

        Args:
            json_artist: an artist in json format
        """
        artist_dict = {}
        artist_dict["id"] = json_artist["artist_id"]
        artist_dict["name"] = json_artist["name"]

        return Artist(artist_dict)

    def album_convert_from_json(self, json_album):
        """ method to convert our album class from JSON format
        back to Album format

        Args:
            json_album: a album in json format
        """
        album_dict = {}
        album_dict["id"] = json_album["album_id"]
        album_dict["name"] = json_album["album_name"]
        album_dict["total_tracks"] = json_album["album_total_tracks"]
        album_dict["album_type"] = json_album["album_type"]

        return Album(album_dict)

# # testing

# # need to be logged into the test spotify account: cmpt370.group5@gmail.com account for these
# # tests to pass
# sp_manager = SpotifyAPIManager()
# sp_manager.link_spotify_account()

# sp_id = sp_manager.get_user_id()

# ps = PersistentStorage(sp_id)

#     # test 0: encrypt()
# unencrypted_text = "encrypt this testing message"
# encrypted_text = ps.encrypt(unencrypted_text)

# assert(encrypted_text != unencrypted_text)

#     # test 1: decrypt()
# assert(ps.decrypt(encrypted_text) == unencrypted_text)

#     # test 2: decrypting again after reinitialization
# ps = PersistentStorage(sp_id)
# assert(ps.decrypt(encrypted_text) == unencrypted_text)

#     # test 3: create new member
# ps.create_new_member()

#     # test 4: check if user exists
# assert(ps.check_if_user_exists())

#     # test 5: save_current_playlist
# playlists = sp_manager.get_member_playlists()

# ps.save_current_playlist(playlists[2])

# query_obj = {
#     "encrypted_spotify_id": ps.encrypted_spotify_id,
#     "current_playlist": dict(playlists[2]),
#     "groups": []
# }

# assert(ps.collection.count_documents(query_obj, limit=1) > 0)