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

    def save_current_playlist(self, playlist):
        """ puts the active playlist in the input into the users persistent storage

        Args:
            playlist (Playlist): list of playlist objects to store
        """
        if self.check_if_user_exists():
           query = { "spotify_id": self.spotify_id }

           new_data = { "$set": {
               "spotify_id": self.spotify_id,
               "current_playlist": dict(playlist),
           }}

           self.collection.update_one(query, new_data)

    def get_current_playlist(self):
        """ gets the current_playlist entry in the database, then converts to playlist object

        Returns:
            playlist_obj (Playlist): playlist object rebuilt from the json
        """

        query = { "spotify_id": self.spotify_id }

        doc = self.collection.find_one(query)

        playlist_dict = {"name": "Current Playlist",
                        "owner": {"id": self.spotify_id},
                        "id": "temp_id",
                        "tracks": {"total": 25}}

        return Playlist(playlist_dict, doc["current_playlist"])

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

    def get_group_playlists(self, group_id):
        """ return the group's created playlists

        Args:
            group_id (int64): the desired group
        """
        query = { "group_id": group_id }

        doc = self.collection.find_one(query)

        return doc["playlists"]

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