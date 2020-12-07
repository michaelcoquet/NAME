
from name.backend_classes.playlist import Playlist

class TemporaryStorage:
    """A class which will handle the temporary storage of a created
    playlist and store the list of songs in a text file.
    """
    def __init__(self, temp_playlist):
        """Initializes the temp_playlist class and converts playlist
        to a string.
        temp_playlist: A playlist object
        """
        self.temp_playlist = temp_playlist
        self.my_string = self.convert_to_string()

    def convert_to_string(self):
        """Retrieves the necessary data from the playlist object
        and converts it to a string for display in a file.
        """
        song_names = [i.song_name for i in self.temp_playlist.songs]
        to_print = "Playlist name: " + self.temp_playlist.playlist_name + "\n"
        to_print = to_print + "Songs: " + "\n"

        for song_name in song_names:
            to_print = to_print + "    " + song_name + "\n"
        
        return to_print
        
    def save_to_file(self):
        """Saves the current playlist to a .txt file with the same
        name as the playlist.
        """
        file_name = self.temp_playlist.playlist_name
        f = open(file_name + ".txt", "w")
        f.write(self.my_string)
        f.close()