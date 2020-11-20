import lyricsgenius
from lyricsgenius import genius

class Genius_Api_Manager(object):

    def __init__(self, song_name, song_artist):
        """Initialization function to authenticate the program's
        connection to the genius API
        """
        self.song_name = song_name
        self.song_artist = song_artist
        self.my_genius = lyricsgenius.Genius("F91niKdwkbdKfbtYZzg1IYm4xoze0Y2Pwu1P0q2WgU68ZydN"
                                              + "M0FdrpXQqXxD_-Td")

    def search_for_lyrics(self):
        """Searches the Genius API and returns the song's lyrics
        returns None if no song or lyrics found.
        song_name: the name of the desired song
        song_artist: the desired song's artist
        """
        try:
            song_lyrics = self.my_genius.search_song(self.song_name, self.song_artist).lyrics
        except:
            #return None if no song or lyrics found
            return None
        return song_lyrics
    

test = Genius_Api_Manager("country roads", "John Denver")
print(test.search_for_lyrics())

#Old format tests below, ignore for now

#print(test.search_for_lyrics("country roads", "John Denver"))
#print(test.search_for_lyrics("country roads", "Kanye"))
#print(test.search_for_lyrics("country roads", None))
#print(test.search_for_lyrics("7428394782309470892", "John Denver"))
#test.search_for_lyrics("7428394782309470892", "John Denver")







