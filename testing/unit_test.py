import os
import pytest
from proof_of_concept import Playlist
from proof_of_concept import Song
from proof_of_concept import User

# hardcoding for testing purposes
client_id = "0f34fcaccbd64596a108401d6b020f1e" # this is the spotifyAPI developer clientID for developers only
client_secret = "b2d9c4f194224634bde7b616eb45c04a"
redirect_uri = "https://example.com/callback"
username = "vha6pttyppu7tnrc0l1j4k4de"
# this is a new spotify account created just for testing
me = User()

def test_getSpotifyPlaylists():
    me.linkSpotifyAccount(username=username, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)

    # print out each of the users saved playlists
    playlists = me.getSpotifyPlaylists()

    # check if the api returned the testing playlist
    assert playlists['items'][0]['name'] == "testing0"
    assert playlists['items'][1]['name'] == "testing1"
    assert playlists['items'][2]['name'] == "testing2"

def test_hasSpotifyAccount():
    # should still have a linked spotify account if the previous test passed
    # so just a simple assert is required
    assert me.isGuest == False

    # clear the cache now (effectively forgetting the linked account)
    clear_cache()

    # now try giving a username with a missing character 
    # the isGuest should now be True
    me.linkSpotifyAccount(username="ha6pttyppu7tnrc0l1j4k4de", client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
    assert me.isGuest == True

    # finally clear the cache again so it doesnt cause problems
    # if the tests are ran again
    clear_cache()
    
def clear_cache():
    # delete the caches (probably not the proper or ideal way to do this but good enough for testing)
    if os.path.exists(".cache"):
        os.remove(".cache")
    else:
        print("The file does not exist")