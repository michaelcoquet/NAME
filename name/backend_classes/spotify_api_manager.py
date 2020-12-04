# imports
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials

from name.backend_classes.song import Artist
from name.backend_classes.song import Album
from name.backend_classes.song import Song
from name.backend_classes.song import SongDetails
from name.backend_classes.playlist import Playlist


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

    def search_songs(self, song_list, offset=0):
        """ Searches the spotify api for the given list of songs.
        song_list: list of songs to search for.
        offset: offset of song results to return. Defaults to 0, which
        would return the first page (e.g. first 10 songs).
        returns: a dictionary with the song titles from song list,
        as well as a list of dictionaries containing info for all
        the songs that were returned for that song title
        """
        search_results = {"query title": [],
                          "found songs": []}
        for song in song_list:
            search_results["query title"].append(song)
            result = self.spotify.search(q=song, limit=10, type="track", offset=offset)
            # go through list of found songs and save results
            # in the dictionary
            for found_song in result["tracks"]["items"]:
                song_info = {"name": found_song["name"],
                             "id": found_song["id"],
                             "artists": found_song["artists"],
                             "album": found_song["album"]}
                # get song details for the song
                song_details = self.get_audio_features(found_song["id"])
                # convert to a Song object
                song = Song(song_info, song_details)
                search_results["found songs"].append(song)
        return search_results

    def get_album(self, album_id):
        """ Given an album id, search for album info
        and return an Album object.
        album_id: string value of the album id
        returns: an album object.
        """
        album_data = self.spotify.album(album_id)
        album = Album(album_data)
        return album

    def get_artist(self, artist_id):
        """ Given an artist id, search for artist info
        and return an Artist object.
        artist_id: string value of the artist id
        returns: an artist object.
        """
        artist_data = self.spotify.artist(artist_id)
        artist = Artist(artist_data)
        return artist

    def get_audio_features(self, song_id):
        """ Gets audio features for the given song id
        song_id: a song id (string)
        returns: a SongDetails object
        """
        features = self.spotify.audio_features(tracks=[song_id])[0]
        song_details = SongDetails(features)
        return song_details

    def create_playlist_object(self, playlist_data):
        """ Given the json object Spotify returns as a playlist,
        convert it to one of our Playlist objects. 
        playlist_data: a json formatted spotify playlist
        """
        songs = self.spotify.playlist_items(playlist_data["id"])["items"]
        songs_list = []
        # Get the tracks of the playlist
        for song in songs:
            song_details = self.get_audio_features(song["track"]["id"])
            songs_list.append(Song(song["track"], song_details))
        # Convert into Playlist Object
        playlist = Playlist(playlist_data, songs_list)
        return playlist

    def get_member_playlists(self):
        """ Gets a list of all playlists for the current user.
        returns: a list of playlist objects
        """
        # make sure the auth token is valid and refresh if needed
        self.refresh_auth_token()
        # get the playlists
        user_id = self.get_user_id()
        playlists_data = self.spotify.user_playlists(user_id)
        # convert to a list of playlist objects
        playlist_list = []
        for playlist_data in playlists_data["items"]:
            playlist = self.create_playlist_object(playlist_data)
            playlist_list.append(playlist)
        return playlist_list

    def add_member_playlist(self, playlist):
        """" Saves the given playlist object to the
        the playlist owner's Spotify account.
        playlist: a playlist object
        returns: A copy of the new playlist object that was created
        (for verification purposes)
        """
        # Make sure the access token is valid and refresh if needed
        self.refresh_auth_token()
        # First, create a new empty playlist in spotify
        user_id = self.get_user_id()
        playlist_name = playlist.playlist_name
        description = "A N.A.M.E. similarity playlist"
        new_playlist = self.spotify.user_playlist_create(user=user_id, name=playlist_name, 
                                                         description=description)
        new_playlist_id = new_playlist["id"]
        # Get spotify track objects for each song in the given playlist
        song_ids = [song.song_id for song in playlist.songs]
        # Add all the tracks to the new playlist
        self.spotify.playlist_add_items(new_playlist_id, song_ids)
        return self.create_playlist_object(new_playlist)

    def get_recently_played_songs(self, limit):
        """ Gets a list of the current member's last played tracks
        limit: the total number of tracks to return
        returns: a list of up to the limit of song objects
        """
        # Make sure the access token is valid and refresh if needed
        self.refresh_auth_token()
        # Get recent tracks
        recent_tracks = self.spotify.current_user_recently_played(limit)
        # convert to song objects
        songs = []
        for track in recent_tracks["items"]:
            song_details = self.get_audio_features(track["track"]["id"])
            song = Song(track["track"], song_details)
            # don't add duplicates to the list
            if len(songs) == 0 or song.song_name not in [song.song_name for song in songs]:
                songs.append(song)
        return songs

    def get_top_songs(self):
        """ Gets a list of the current member's top tracks. 
        The maximum number that can be returned is 20.
        returns: at most a list of 20 song objects
        """
        # Make sure the access token is valid and refresh if needed
        self.refresh_auth_token()
        # Get top tracks
        top_tracks = self.spotify.current_user_top_tracks()
        # convert to song objects
        songs = []
        for track in top_tracks["items"]:
            song_details = self.get_audio_features(track["id"])
            song = Song(track, song_details)
            # don't add duplicates to the list
            if len(songs) == 0 or song.song_name not in [song.song_name for song in songs]:
                songs.append(song)
        return songs

    def get_top_artists(self):
        """ Gets a list of the current member's top artists.
        The maximum number that can be returned is 20. 
        returns: at most a list of 20 artist objects.
        """
        # Make sure the access token is valid and refresh if needed
        self.refresh_auth_token()
        # Get top artists
        top_artists = self.spotify.current_user_top_artists()
        # convert to artists objects
        artists = []
        for artist in top_artists["items"]:
            new_artist = self.get_artist(artist["id"])
            # don't add duplicates to the list
            if len(artists) == 0 or new_artist.name not in [artist.name for artist in artists]:
                artists.append(new_artist)
        return artists

    def get_song_genres(self, song):
        """ Given a song object, find all the genres
        associated with the song. 
        song: a song object
        returns: a list of genres (strings)
        """
        # to get genres, we need to look at the artist info
        artists = song.song_artist
        # get a list of genres for each artist
        genres = []
        for artist in artists:
            artist_info = self.spotify.artist(artist.artist_id)
            genres.extend(artist_info["genres"])
        return genres

    def refresh_auth_token(self):
        """ Checks to see if the member's auth token is
        expired or not. If it is expired, creates a new auth token.
        """
        token = self.auth_manager.get_cached_token()
        expired = self.auth_manager.is_token_expired(token)
        if expired:
            self.auth_manager.refresh_access_token(token["refresh_token"])
