import lyricsgenius
from lyricsgenius import genius

class genius_api_manager(object):

    def __init__(self):
        """Initialization function to authenticate the program's
        connection to the genius API
        """
        self.my_genius = lyricsgenius.Genius("F91niKdwkbdKfbtYZzg1IYm4xoze0Y2Pwu1P0q2WgU68ZydN"
                                              + "M0FdrpXQqXxD_-Td")

    def search_for_lyrics(self, song_name, song_artist):
        """Searches the Genius API and returns the song's lyrics
        returns None if no song or lyrics found.
        song_name: the name of the desired song
        song_artist: the desired song's artist
        """
        try:
            song_lyrics = self.my_genius.search_song(song_name, song_artist).lyrics
        except:
            #return None if no song or lyrics found
            return None
        return song_lyrics
    

test = genius_api_manager()
#print(test.search_for_lyrics("country roads", "John Denver"))
#print(test.search_for_lyrics("country roads", "Kanye"))
#print(test.search_for_lyrics("country roads", None))
#print(test.search_for_lyrics("7428394782309470892", "John Denver"))
#test.search_for_lyrics("7428394782309470892", "John Denver")






