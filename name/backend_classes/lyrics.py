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
        return 0
    
    def get_num_chorus(self):
        # split into paragraphs
        # check if any repeat
        return 0

    def get_variability(self):
        return 0

    def __analyze_lyrics(self):
        return 0

    def __split_into_verses(self):

        # split lyrics into separate verses
        # return as a list, each verse a string

        return []

