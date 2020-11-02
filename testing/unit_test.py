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
    assert me.hasSpotifyAccount() == True

    # clear the cache now (effectively forgetting the linked account)
    clear_cache()
    # now try giving a username with a missing character 
    me.linkSpotifyAccount(username="ha6pttyppu7tnrc0l1j4k4de", client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
    
    assert me.hasSpotifyAccount() == False

    clear_cache()

# test adding a song to a spotify playlist
def test_addSong():
    # need a spotify track ID (Moonlight Sonata aka Piano Sonata No. 14, Op. 27 No. 2)
    track = ["7xfSCgVOkQJhVxnqzepATH"]
    
    # the cache was cleared in the previous test so must relink account
    me.linkSpotifyAccount(username=username, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)

    # # make sure the account is properly linked again
    assert me.hasSpotifyAccount() == True

    # Get the users playlists
    playlists = me.getSpotifyPlaylists()

    # choose the first playlist to add a track to (aka testing0)
    # assert that testing0 is indeed the first palylist
    assert playlists['items'][0]['name'] == "testing0"
    pl_ID = playlists['items'][0]['id']
    pl = Playlist(pl_ID)
    pl.addSong(me, pl_ID, track)

    # now we must return the tracks from the playlist and make sure the
    # first track is our new track
    response = me.getSpotifyHook().playlist_items(pl_ID,
                                    offset=0,
                                    fields='items.track.name,total',
                                    additional_types=['track'])
        
        
    assert response['items'][0]['track']['name'] == "Moonlight Sonata (First Movement from Piano Sonata No. 14, Op. 27 No. 2)"


    # finally clear the cache again so it doesnt cause problems
    # if the tests are ran again
    clear_cache()

def clear_cache():
    # delete the caches (probably not the proper or ideal way to do this but good enough for testing)
    if os.path.exists(".cache"):
        os.remove(".cache")
    else:
        print("The file does not exist")

