"""CMPT 370 Group 5 Project: NAME (Nearly Analogous Music Engine)
    Credits: Michael Coquet
             Elizabeth Reid
             Ben Camplin
             Laurence Craig Garcia
             Sean Warren
"""
import spotipy

class Playlist:
    def __init__(self, playlistID):
        self.ID = playlistID

    def addSong(self, user, playlistID, items):
        user.getSpotifyHook().playlist_add_items(playlist_id=playlistID, items=items, position=0)
