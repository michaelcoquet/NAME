import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth

class User:
    def linkSpotifyAccount(self, username, client_id, client_secret, redirect_uri):
        self.username = username
        self.scopes = "playlist-read-private playlist-modify-private playlist-modify-public"
        self.auth_manager = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=self.scopes)

        try:      
            response = self.auth_manager.get_auth_response(open_browser=True)
            code = self.auth_manager.parse_response_code(response)
            self.token_info = self.auth_manager.get_access_token(code, as_dict=False)
            self.token = self.token_info
            self.spotify = spotipy.Spotify(auth = self.token)
        except:
            print("Error: invalid username")        

    # Shows a user's playlists (code from the spotipy docs)
    def getSpotifyPlaylists(self):
        return self.spotify.user_playlists(self.username, limit=50)

    def hasSpotifyAccount(self):
        try:
            self.getSpotifyPlaylists()
        except:
            return False
        
        return True

    def getSpotifyHook(self):
        return self.spotify