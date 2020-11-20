import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials


class SpotifyAPIManager:

    def __init__(self):
        """ Instantiation function. Sets up all required attributes
        for the authorization code flow.
        """
        self.client_id = "0e48c2ec84d3401e9262a2159a277d82"
        self.client_secret = "aa650130a5b544598f4b058bfd264b21"
        self.redirect_uri = "http://127.0.0.1:8080/callback/q"
        self.scopes = '''user-read-recently-played user-top-read playlist-modify-public
                        playlist-modify-private playlist-read-private'''
        # default auth manager for a guest
        self.auth_manager = SpotifyClientCredentials(client_id=self.client_id,
                                                     client_secret=self.client_secret)
        # sets the default connection to the API
        self.spotify = spotipy.Spotify(auth_manager=self.auth_manager)

    def link_spotify_account(self):
        """ Attempts to log in to Spotify.
        Returns: True if successful, False otherwise.
        """
        try:
            # reset the auth manager for Authorization
            self.auth_manager = SpotifyOAuth(client_id=self.client_id, 
                                             client_secret=self.client_secret,
                                             redirect_uri=self.redirect_uri,
                                             scope=self.scopes)
            # attempt to get log in credentials from a user
            response = self.auth_manager.get_auth_response(open_browser=True)
            code = self.auth_manager.parse_response_code(response)
            token = self.auth_manager.get_access_token(code, as_dict=False)
            # reset the connection to the API, providing the new auth value
            self.spotify = spotipy.Spotify(auth=token, auth_manager=self.auth_manager)
            return True
        except:
            print("Failed to link account.")
            # reset the auth manager back to the guest format
            self.auth_manager = SpotifyClientCredentials(client_id=self.client_id,
                                                         client_secret=self.client_secret)
            return False

    def get_user_id(self):
        """ Gets the user_id if the user is logged in to Spotify. """
        try:
            user_id = self.spotify.current_user()["id"]
            return user_id
        except:
            # Either the user is a guest, or the api request failed
            return None
 
    def search_songs(self, song_list):
        """ Searches the spotify api for the given list of songs.
        song_list: list of songs to search for.
        returns: a dictionary with the song titles from song list,
        as well as a list of dictionaries containing info for all
        the songs that were returned for that song title
        """
        search_results = {"query title": [],
                          "found songs": []}
        for song in song_list:
            search_results["query title"].append(song)
            result = self.spotify.search(q=song, limit=10, type="track")
            # go through list of found songs and save results
            # in the dictionary
            for found_song in result["tracks"]["items"]:
                # first get a nice list of artist names
                artists = [artist["name"] for artist in found_song["artists"]]
                song_info = {"name": found_song["name"],
                             "id": found_song["id"],
                             "artists": artists,
                             "album id": found_song["album"]["id"]}
                search_results["found songs"].append(song_info)
        return search_results
