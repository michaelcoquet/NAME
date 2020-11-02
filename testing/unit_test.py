from proof_of_concept import Playlist
from proof_of_concept import Song
from proof_of_concept import Member

def test_getSpotifyPlaylists():

    client_id = "0f34fcaccbd64596a108401d6b020f1e" # this is the spotifyAPI developer clientID for developers only
    client_secret = "b2d9c4f194224634bde7b616eb45c04a"
    redirect_uri = "https://example.com/callback"


    # this is a new spotify account created just for testing
    username = "vha6pttyppu7tnrc0l1j4k4de"

    me = Member(username=username, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)

    # print out each of the users saved playlists
    playlists = me.getSpotifyPlaylists()

    # check if the api returned the testing playlist
    assert playlists['items'][0]['name'] == "testing0"
    assert playlists['items'][1]['name'] == "testing1"
    assert playlists['items'][2]['name'] == "testing2"
