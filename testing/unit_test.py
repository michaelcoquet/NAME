from proof_of_concept import Playlist
from proof_of_concept import Song
from proof_of_concept import Member

def test_getSpotifyPlaylists():
    # this is a new spotify accound created just for testing
    testID = "5480f378c09e460a99ff860bf9f25a70"
    secret = "c0c8a8f94e934fa7931f7b4f22ea710b"
    redirect = "https://example.com/callback"

    me = Member(testID, secret, redirect)

    # print out each of the users saved playlists
    playlists = me.getSpotifyPlaylists()
    
    # check if the api returned the testing playlist
    assert playlists['items'][0]['name'] == "testing"
