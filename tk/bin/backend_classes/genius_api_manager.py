"""CMPT 370 Group 5 Project: NAME (Nearly Analogous Music Engine)
    Credits: Michael Coquet
             Elizabeth Reid
             Ben Camplin
             Laurence Craig Garcia
             Sean Warren
"""
import lyricsgenius
from lyricsgenius import genius

class Genius_Api_Manager(object):
    """ A class designed to interact with the Genius API and
        return the given songs lyrics in a string
    """

    def __init__(self, song_name, song_artist):
        """ Initialization function to authenticate the program's
            connection to the genius API
        """

        self.song_name = song_name
        self.song_artist = song_artist
        self.my_genius = lyricsgenius.Genius("F91niKdwkbdKfbtYZzg1IYm4xoze0Y2Pwu1P0q2WgU68ZydN"
                                              + "M0FdrpXQqXxD_-Td")
        # Disables progress messages in console
        self.my_genius.verbose = False

    def search_for_lyrics(self):
        """ Searches the Genius API and returns the song's lyrics
            returns a message if no song or lyrics found.
            song_name: the name of the desired song
            song_artist: the desired song's artist
        """
        try:
            song_lyrics = self.my_genius.search_song(self.song_name, self.song_artist).lyrics
            if(song_lyrics == "Instrumental"):
                return "No lyrics for this song were found"
        except:
            return "No lyrics for this song were found"
        return song_lyrics
