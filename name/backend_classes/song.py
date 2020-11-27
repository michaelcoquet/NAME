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

    def __str__(self):
        """
        A string representation of the object
        """
        return ("Name: {} \n"
                "Artist: {} \n"
                "--Details--{}").format(self.song_name,
                                        [artist.name for artist in self.song_artist],
                                        self.audio_features)

    def __repr__(self):
        return self.song_name


class Artist:
    """
    A class that stores the data of each artist of the song
    """
    def __init__(self, artist):
        """
        artist: A list of artist object
        """
        self.artist = artist
        self.artist_id = artist['id']
        self.name = artist['name']

    # def __eq__(self, other):
    #     if self.artist_id == other.artist_id:
    #         return True

        # return False

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
