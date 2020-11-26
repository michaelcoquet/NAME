import os
import pytest
from proof_of_concept import Playlist
from proof_of_concept import Song
from proof_of_concept import User
# as we work on our app going forward, import classes from the appropriate folder(s)
from name.backend_classes import SongSimilarity
from name.backend_classes import Genius_Api_Manager
from name.backend_classes import Lyrics

# Tests for the User class
def test_setUserType_v1():
    """
    Test ID: User01. Normally setUserType would be called from within the Spotify API
    after a User has linked/ unlinked their account. For this unit test, we simply check that
    the User type is modified correctly.
    """
    user = User(type="Guest")
    user.setUserType(type="Member")

    assert user.type == "Member"

def test_setUserType_v2():
    """
    Test ID: User02. Check that the user type is updated correctly from "Member" to "Guest".
    """
    user = User(type="Member")
    user.setUserType(type="Guest")

    assert user.type == "Guest"

def test_isGuest_v1():
    """
    Test ID: User03. Check that the method returns True when the User type is Guest.
    """
    user = User(type="Guest")

    assert user.isGuest() == True

def test_isGuest_v2():
    """
    Test ID: User04. Check that the method returns False when the User type is not Guest.
    """
    user = User(type="Member")

    assert user.isGuest() == False

# Tests for the SongSimilarity class
def test_compare_all():
    """
    Test ID: SongSim01. Check that the method returns a value between 0 and 1.
    """
    songSimilarityCalculator = SongSimilarity(["exampleSong"],["duration_ms"])
    result = songSimilarityCalculator.compare_all()#

    assert (result >= 0 and result <= 1)

# The following list of tests are more complicated: we likely will need to rewrite these later to match up
# better with the test plan, but for now they illustrate how to test methods that use the Spotify API.


# hardcoding for testing purposes
client_id = "0f34fcaccbd64596a108401d6b020f1e" # this is the spotifyAPI developer clientID for developers only
client_secret = "b2d9c4f194224634bde7b616eb45c04a"
redirect_uri = "https://example.com/callback"
username = "vha6pttyppu7tnrc0l1j4k4de" # this is a new spotify account created just for testing

me = User(type="Guest")

def test_linkSpotifyAccount(username=username, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri):
    """
    Tests that the linkSpotifyAccount method runs without error
    """
    me.linkSpotifyAccount(username=username, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)

    assert me.isGuest() == False

def test_getSpotifyPlaylists():
    """
    If the above test passes, we do not need to link to Spotify again. Here we test if we can access
    playlists from the linked account.
    """
    # print out each of the users saved playlists
    playlists = me.getSpotifyPlaylists()

    # check if the api returned the testing playlist
    assert playlists['items'][0]['name'] == "testing0"
    assert playlists['items'][1]['name'] == "testing1"
    assert playlists['items'][2]['name'] == "testing2"

# test adding a song to a spotify playlist
def test_addSong():
    # need a spotify track ID (Moonlight Sonata aka Piano Sonata No. 14, Op. 27 No. 2)
    track = ["7xfSCgVOkQJhVxnqzepATH"]

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


    # finally clear the cache so it doesnt cause problems
    # if the tests are ran again
    clear_cache()

#### Tests for genius_api_manager
def test_genius_api_manager():
    genius = Genius_Api_Manager("40:1", "Sabaton")
    test_lyrics = genius.search_for_lyrics()
    test_lyrics = test_lyrics.split()
    # Check to see if a fairly unique word known to be in the song
    # exists in the returned string
    assert "mortars" in test_lyrics

    # Empty song name and artist test
    genius = Genius_Api_Manager("", "")
    test_lyrics = genius.search_for_lyrics()
    assert test_lyrics == "No lyrics for this song were found"

    # Instrumental song test
    genius = Genius_Api_Manager("1812 overture", "Tchaikovsky")
    test_lyrics = genius.search_for_lyrics()
    assert test_lyrics == "No lyrics for this song were found"

#### Tests for Lyrics class
def test_lyrics():
    # Test to see if the lyrics class is successfully working
    # with the genius api class to get the lyrics
    lyrics_class = Lyrics("Country Roads", "John Denver")
    test_lyrics = lyrics_class.get_lyrics()
    test_lyrics = test_lyrics.split()
    # Check to see if a fairly unique word known to be in the song
    # exists in the returned string
    assert "Shenandoah" in test_lyrics

    # Test to see correct number of chorus is returned
    assert lyrics_class.get_num_chorus() == 3

    # Empty song name and artist test
    lyrics_class = Lyrics("", "")
    test_lyrics = lyrics_class.get_lyrics()
    assert test_lyrics is None

    # Test to see if correct number of words is returned
    lyrics_class = Lyrics("It's a beautiful day", "Queen")
    assert lyrics_class.get_num_words() == 66

    # Test to see correct number of chorus is returned when 0
    assert lyrics_class.get_num_chorus() == 0

    # Test to see correct number of verses is returned
    assert lyrics_class.get_num_verse() == 2

    # Test to see if variability is correct
    assert lyrics_class.get_variability() == 0

def clear_cache():
    # delete the caches (probably not the proper or ideal way to do this but good enough for testing)
    if os.path.exists(".cache"):
        os.remove(".cache")
    else:
        print("The file does not exist")

