import spotipy
from spotipy.oauth2 import SpotifyOAuth

class Member:

    def __init__(self, ID):
        self.ID = ID

    # Shows a user's playlists (code from the spotipy docs)
    def getSpotifyPlaylists(self):
        spotifyPlaylists = []
        
        scope = 'playlist-read-private'
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

        results = sp.current_user_playlists(limit=50)\

        for i, item in enumerate(results['items']):
            print("%d %s" % (i, item['name']))
        
        return spotifyPlaylists