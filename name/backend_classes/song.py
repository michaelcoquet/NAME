import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class Song:
    """
    A class for Song that stores the collected data
    from Spotify.
    """
    def __init__(self, song, song_details):
        """
        song: A song object containing the data of the song from Spotify
        """
        self.song_name = song['name']
        self.song_id = song['id']
        self.song_artist = [Artist(artist) for artist in song['artists']]
        self.album_details = Album(song['album'])
        self.audio_features = song_details

    # Placeholder function until spotify api manager implements it
    # def get_audio_features(self):
    #     client_id='805b88ab14814deea1ae9a0f650b12fc'
    #     client_secret='c20fae8240cb44e0aa720ed23053f307'
    #     auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    #     sp = spotipy.Spotify(auth_manager=auth_manager)
    #     features = sp.audio_features(self.song_id)
    #     return features[0]

    # def __eq__(self, other):
    #     """
    #     A utility function that compares whether the two objects are equal
    #     """
    #     if self.song_id == other.song_id:
    #         return True

    #     return False

    def __str__(self):
        """
        A string representation of the object
        """
        return ("Name: {} \n"
                "Artist: {} \n"
                "--Details--{}").format(self.song_name, self.song_artist.name,
                                        self.audio_features)

    def __repr__(self):
        return self.song_name


class Artist:
    """
    A class that stores the data of an artist collected from Spotify
    """
    def __init__(self, artist):
        """
        artist: An artist objects containing the data of the song's artist
        """
        self.artist = artist
        self.artist_id = artist["id"]
        self.name = artist["name"]

    def __eq__(self, other):
        if self.artist_id == other.artist_id:
            return True

        return False

    def __str__(self):
        return f"{self.artist_id,self.name}"


class Album:
    """
    A class that stores the data of an album collected from Spotify
    """
    def __init__(self, album):
        """
        album: an album object containing the data of the song's album
        """
        self.album_id = album['id']
        self.name = album['name']
        self.size = album['total_tracks']
        self.type = album['album_type']

    def __eq__(self, other):
        if self.album_id == other.album_id:
            return True

        return False

    def __str__(self):
        return ("Album Name: {} \n"
                "Album Type: {} \n"
                "Album Id: {} \n"
                "Total songs: {} ").format(self.name,  self.type,
                                           self.album_id, self.size)


class SongDetails:
    """
    Class for storing the audio features of the song
    """
    def __init__(self, details):
        """
        details: an object containing the audio features of the song
        """
        self.duration = details['duration_ms']
        self.key = details['key']
        self.tempo = details['tempo']
        self.danceability = details['danceability']
        self.energy = details['energy']
        self.loudness = details['loudness']
        self.mode = details['mode']
        self.speechiness = details['speechiness']
        self.acousticness = details['acousticness']
        self.instrumentalness = details['instrumentalness']
        self.liveness = details['liveness']
        self.valence = details['valence']
        self.time_signature = details['time_signature']

    def __str__(self):
        return ("\nDuration: {} \n"
                "Key: {} \n"
                "Tempo: {} \n"
                "Danceability: {} \n"
                "Energy: {} \n"
                "Loudness: {} \n"
                "Mode: {} \n"
                "Speechiness: {} \n"
                "Acousticness: {} \n"
                "Instrumentalness: {} \n"
                "Liveness: {} \n"
                "Valence: {} \n"
                "Time Signature: {}").format(self.duration, self.key,
                                              self.tempo, self.danceability,
                                              self.energy, self.loudness,
                                              self.mode, self.speechiness,
                                              self.acousticness, self.instrumentalness,
                                              self.liveness, self.valence,
                                              self.time_signature)


# Testing

# client_id = '0e48c2ec84d3401e9262a2159a277d82'
# client_secret = 'aa650130a5b544598f4b058bfd264b21'
# auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
# spotify = spotipy.Spotify(auth_manager=auth_manager)

# # a random song
# song1 = '4oVdhvxZrKQTM9ZsUIZa3S'
# test_song = spotify.track(song1)
# a_song = Song(test_song)

# # Test for song name
# expected = 'December'
# test1 = a_song.song_name
# if expected != test1:
#     print("Test1: Error, did not meet the expected result")

# # Test for song id
# expected2 = '4oVdhvxZrKQTM9ZsUIZa3S'
# test2 = a_song.song_id
# if expected2 != test2:
#     print("Test2: Error, did not meet the expected result")

# # Test for song artists
# test3 = a_song.song_artist

# # Test for song