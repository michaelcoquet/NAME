import lyricsgenius
from lyricsgenius import genius

class genius_api_manager(object):

    def __init__(self):
        """Account: The user's Spotify account"""
        self.my_genius = lyricsgenius.Genius("F91niKdwkbdKfbtYZzg1IYm4xoze0Y2Pwu1P0q2WgU68ZydNM0FdrpXQqXxD_-Td")

    def search_for_lyrics(self, song_name, song_artist):
        """TODO: this docstring"""
        song_lyrics = self.my_genius.search_song(song_name, song_artist).lyrics
        return song_lyrics
    

test = genius_api_manager()
print(test.search_for_lyrics("country roads", "John Denver"))





