import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials

class Playlist:
    """
    A class containing the details of the playlist from spotify
    """
    def __init__(self, playlist, playlist_tracks):
        """
        Instantiation function
        playlist: a playlist object from spotify
        playlist_tracks: a list of song objects containing the playlist tracks
        """
        self.playlist_name = playlist['name']
        self.playlist_owner = playlist['owner']['display_name']
        self.playlist_id = playlist['id']
        self.size = playlist['tracks']['total']
        self.songs = playlist_tracks

    def __iter__(self):
        playlist_string = {
                            "playlist_name": self.playlist_name
                          }
        song_string = []
        for song in self.songs:
            song_string.append(dict(song))
        song_dict = { "songs": song_string }
        playlist_dict = playlist_string | song_dict
        yield from playlist_dict.items()

    def add_song(self, song):
        """
        A function that adds song to the playlist,
        appends a song to the list of songs
        song: a song object to be added to the list
        """
        self.songs.append(song)
        self.size = self.size + 1

    def remove_song(self, song_id):
        """
        A function that removes a song from the playlist
        base on its index
        song_id: the id of the song to be removed from the playlist
        """
        # A temporary list for the song ids
        temp = []
        for i in self.songs:
            temp.append(i.song_id)

        if song_id in temp:
            song_index = temp.index(song_id)
            self.songs.pop(song_index)
            self.size = self.size - 1

    def __str__(self):
        return ("Playlist Name: {} \n"
                "Playlist ID: {} \n"
                "Owner: {} \n"
                "Size: {} \n"
                "Songs: {}").format(self.playlist_name, self.playlist_id,
                                    self.playlist_owner, self.size,
                                    [i.song_name for i in self.songs])


# # Testing
# # Just some random playlist
# test_playlist = '3xSYFlYjXkR8cK2plz82R0'
# client_id = '0e48c2ec84d3401e9262a2159a277d82'
# client_secret = 'aa650130a5b544598f4b058bfd264b21'
# auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
# spotify = spotipy.Spotify(auth_manager=auth_manager)

# # Get playlist and song from spotify
# playlist1 = spotify.playlist(test_playlist)
# song1 = spotify.track('4oVdhvxZrKQTM9ZsUIZa3S')
# a_song = S.Song(song1)
# # print(a_song)
# playlist_test = Playlist(playlist1)
# # May take a few seconds depending on the playlist size
# print(playlist_test)

# # Test for the playlist name
# expected = 'neck deep acoustic'
# test1 = playlist_test.playlist_name
# if expected != test1:
#     print("Test1: Error, did not meet the expected result")

# # Test for the playlist owner
# expected2 = 'annie'
# test2 = playlist_test.playlist_owner
# if expected2 != test2:
#     print("Test2: Error, did not meet the expected result")

# # Test for the playlist id
# expected3 = '3xSYFlYjXkR8cK2plz82R0'
# test3 = playlist_test.playlist_id
# if expected3 != test3:
#     print("Test3: Error, did not meet the expected result")

# # Test for the playlist size
# expected4 = 11
# test4 = playlist_test.size
# if expected4 != test4:
#     print("Test4: Error, did not meet the expected result")

# # Function tests

# # Test for adding a song to the playlist
# expected5 = a_song
# playlist_test.add_song(a_song)
# test5 = playlist_test.songs
# if expected5 not in test5:
#     print("Test5: Error, did not meet the expected result")

# # Test for removing a song from the playlist
# expected6 = a_song.song_name
# playlist_test.remove_song(a_song.song_id)
# test6 = playlist_test.songs
# if expected6 in test6:
#     print("Test6: Error, did not meet the expected result")
