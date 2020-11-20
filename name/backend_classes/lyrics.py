import name.backend_classes.genius_api_manager as genius_manager


class Lyrics(object):

    def __init__(self, song_name, song_artist):

        # Call the genius_api_manager and get lyrics
        lyrics_object = genius_manager.Genius_Api_Manager(song_name, song_artist)

        self.__song_lyrics = lyrics_object.search_for_lyrics()
        self.__song_name = song_name
        self.__song_artist = song_artist
        self.__num_words = 0
        self.__num_chorus = 0
        self.__num_verse = 0
        self.__variability_score = 0

    def get_lyrics(self):
        return self.__song_lyrics

    def get_num_words(self):
        words = self.__song_lyrics.split()
        return len(words)

    def get_num_verse(self):

        number_verses = 0

        for word in self.__song_lyrics:
            if("[Verse" in word):
                number_verses += 1

        return number_verses
    
    def get_num_chorus(self):

        number_chorus = 0

        for word in self.__song_lyrics:
            if("[Chorus]" in word):
                number_chorus += 1

        return number_chorus

    def get_variability(self):
        return 0

    def __analyze_lyrics(self):
        return 0


