#import genius_api_manager as genius_manager
#from genius_api_manager import Genius_Api_Manager as genius_manager
from . import Genius_Api_Manager



class Lyrics(object):
    """A class which obtains a song's lyrics and can return
    all necessary information.
    """
    def __init__(self, song_name, song_artist):
        """Initializes the lyrics objects by getting information
        from the lyrics api manager
        song_name: name of the song
        song_artist: artist associated with the song
        """

        # Call the genius_api_manager and get lyrics
        lyrics_object = Genius_Api_Manager(song_name, song_artist)

        self.__song_lyrics = lyrics_object.search_for_lyrics()
        self.__song_name = song_name
        self.__song_artist = song_artist
        self.__num_words = 0
        self.__num_chorus = 0
        self.__num_verse = 0
        self.__variability_score = 0

    def get_lyrics(self):
        """Get song lyrics and return as a string"""

        #If Song is instrumental it has no lyrics but the API
        #Still returns a string so it must be changed
        if(self.__song_lyrics == "Instrumental" or self.__song_lyrics == "No lyrics for this song were found"):
            self.__song_lyrics = None

        return self.__song_lyrics

    def get_song_artist(self):
        return self.__song_artist

    def get_num_words(self):
        """Calculates the number of words in the song's lyrics and
        ignores any irrelevant headers
        """
        number_words = 0

        words = self.get_lyrics().split()
        for word in words:
            if("[" not in word and "]" not in word):
                number_words += 1

        return number_words

    def get_num_verse(self):
        """Calculates the total number of verses in the song"""

        number_verses = 0

        words = self.get_lyrics().split()
        for word in words:
            if("[Verse" in word):
                number_verses += 1

        return number_verses
    
    def get_num_chorus(self):
        """Calculates the total number of choruses in the song"""

        number_chorus = 0

        words = self.get_lyrics().split()
        for word in words:
            if("[Chorus]" in word):
                number_chorus += 1

        return number_chorus

    def get_variability(self):
        """Calculates variability, whatever that means"""
        return 0

    def __analyze_lyrics(self):
        """Analyze the song, I did all the analyzing in the
        respective get functions instead of here by accident,
        will refactor later
        """
        return 0


# Basic tests, will be formalized into pytest unit tests later



#test = Lyrics("It's a beautiful day", "Queen")
#print(test.get_lyrics())
#print("\n")
#print("Number of choruses: ", test.get_num_chorus())
#print("Number of verses: ", test.get_num_verse())
#print("Number of words: ", test.get_num_words())