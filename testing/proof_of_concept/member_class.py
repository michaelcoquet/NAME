import spotipy
from spotipy.oauth2 import SpotifyOAuth

class Member:

    def __init__(self, ID, SECRET, REDIRECT):
        self.client_id = ID
        self.client_secret = SECRET
        self.redirect_uri = REDIRECT

    # Shows a user's playlists (code from the spotipy docs)
    def getSpotifyPlaylists(self):
        scope = 'playlist-read-private'
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(self.client_id, self.client_secret, self.redirect_uri, scope=scope))

        return sp.current_user_playlists(limit=50)
