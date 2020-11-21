import song as S
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials

class Playlist:
    """
    A class containing the details of the playlist from spotify
    """
    def __init__(self, playlist):
        """
        Instantiation function
        playlist: a playlist object from spotify
        """
        self.playlist_name = playlist['name']
        self.playlist_owner = playlist['owner']['display_name']
        self.playlist_id = playlist['id']
        self.size = playlist['tracks']['total']
        self.songs = [S.Song(i['track']) for i in playlist['tracks']['items']] # Store each track of the playlist into a list of songs

    def add_song(self, song):
        """
        A function that adds song to the playlist,
        appends a song to the list of songs
        """
        self.songs.append(song)
        self.size = self.size + 1

    # TODO:
    def remove_song(self, song_id):
        pass

    def __str__(self):
        return ("Playlist Name: {} \n"
                "Playlist ID: {} \n"
                "Owner: {} \n"
                "Size: {} \n"
                "Songs: {}").format(self.playlist_name, self.playlist_id,
                                    self.playlist_owner, self.size,
                                    [i.song_name for i in self.songs])


# # Testing

# test_playlist = '37i9dQZF1DWSWllk9RmgZM'
# client_id = '0e48c2ec84d3401e9262a2159a277d82'
# client_secret = 'aa650130a5b544598f4b058bfd264b21'
# auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
# spotify = spotipy.Spotify(auth_manager=auth_manager)

# # Get playlist from spotify
# playlist1 = spotify.playlist(test_playlist)

# playlist_test = Playlist(playlist1)
# # May take a few seconds depending on the playlist size
# print(playlist_test)

# # Test for the playlist name
# expected = 'This Is Post Malone'
# test1 = playlist_test.playlist_name
# if expected != test1:
#     print("Test1: Error, did not meet the expected result")

# # Test for the playlist owner
# expected2 = 'Spotify'
# test2 = playlist_test.playlist_owner
# if expected2 != test2:
#     print("Test2: Error, did not meet the expected result")

# # Test for the playlist id
# expected3 = '37i9dQZF1DWSWllk9RmgZM'
# test3 = playlist_test.playlist_id
# if expected3 != test3:
#     print("Test3: Error, did not meet the expected result")

# # Test for the playlist size
# expected4 = 45
# test4 = playlist_test.size
# if expected4 != test4:
#     print("Test4: Error, did not meet the expected result")