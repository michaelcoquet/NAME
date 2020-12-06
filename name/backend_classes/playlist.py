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
        self.playlist_owner = playlist['owner']['id']
        self.playlist_id = playlist['id']
        self.size = playlist['tracks']['total']
        self.songs = playlist_tracks

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

    def get_song_features(self):
        """
        A function that returns the audio features
        of each song inside the playlist
        """
        song_features = []
        # Get each song features of the song
        for items in self.songs:
            song_features.append(items.audio_features)

        return song_features

    def update_playlist_name(self, new_name):
        """
        A function that updates the name of the current playlist
        new_name : the new name of the playlist
        """
        self.playlist_name = new_name

    # Will implement soon
    def get_song_similarity(self):
        return "Not implemented yet"

    def convert_to_json(self):
        playlist_dict = {
                            "playlist_name": self.playlist_name,
                            "playlist_owner": {"id": self.playlist_owner},
                            "playlist_id": self.playlist_id,
                            "playlist_size": self.size
                          }
        song_list = []
        for song in self.songs:
            song_list.append(dict(song))
        playlist_dict["songs"] = song_list
        return playlist_dict

    def __str__(self):
        return ("Playlist Name: {} \n"
                "Playlist ID: {} \n"
                "Owner: {} \n"
                "Size: {} \n"
                "Songs: {}").format(self.playlist_name, self.playlist_id,
                                    self.playlist_owner, self.size,
                                    [i.song_name for i in self.songs])
