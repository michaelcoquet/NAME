import os
import time
import pytest

from name.testing.proof_of_concept import User
# as we work on our app going forward, import classes from the appropriate folder(s)
from name.backend_classes import SongSimilarity
from name.backend_classes import SpotifyAPIManager
from name.backend_classes import Query


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


# # Tests for the SongSimilarity class
# def test_compare_all():
#     """ Test ID: SongSim01. Check that the method
#     returns a value between 0 and 1.
#     """
#     # rewrite this test

#     assert (result >= 0 and result <= 1)


# Tests for the SpotifyAPIManager class
def test_linkSpotifyAccount():
    """ Test ID: Spotify14. Tests that the method returns
    True when valid credentials are provided, False if authorization
    is cancelled.
    """
    spotify_api_manager = SpotifyAPIManager()
    print("Enter these valid credentials into the popup window:")
    print("email: cmpt370.group5@gmail.com")
    print("password: pennywise_1640")
    result = spotify_api_manager.link_spotify_account()
    assert result == True


def test_get_user_id_v1():
    """ Test ID: Spotify08. Tests that the method returns
    None when the user is not logged in to Spotify.
    """
    # wait two seconds before running this test so that the API
    # doesn't reject the connection
    time.sleep(2)
    spotify_api_manager = SpotifyAPIManager()
    account_link = spotify_api_manager.link_spotify_account()
    assert account_link == True
    result = spotify_api_manager.get_user_id()
    # the user id for the cmpt370 spotify account
    assert result == "vha6pttyppu7tnrc0l1j4k4de"


def test_search_songs_v1():
    """ Test ID: Spotify15. Tests that the method returns
    a dictonary with an empty list when Spotify found no results.
    This function contains multiple subtests: 
    Test when the list of songs has one element, the user type is guest
    Test when the list has multiple elements, user type is guest
    Test when the list has one element, user type is member
    Test when the list has multiple elements, user type is member
    """
    # wait two seconds before running this test so that the API
    # doesn't reject the connection
    time.sleep(2)
    spotify_api_manager = SpotifyAPIManager()
    # first subtest
    song_list = ["hfhsjkhfs"]
    result = spotify_api_manager.search_songs(song_list)
    assert result["query title"] == ["hfhsjkhfs"]
    assert result["found songs"] == []
    # second subtest
    song_list = ["hfhsjkhfs", "uiosfios", "sywyquq"]
    result = spotify_api_manager.search_songs(song_list)
    assert result["query title"] == ["hfhsjkhfs", "uiosfios", "sywyquq"]
    assert result["found songs"] == []
    # third subtest
    account_link = spotify_api_manager.link_spotify_account()
    assert account_link == True
    song_list = ["hfhsjkhfs"]
    result = spotify_api_manager.search_songs(song_list)
    assert result["query title"] == ["hfhsjkhfs"]
    assert result["found songs"] == []
    # fourth subtest
    song_list = ["hfhsjkhfs", "uiosfios", "sywyquq"]
    result = spotify_api_manager.search_songs(song_list)
    assert result["query title"] == ["hfhsjkhfs", "uiosfios", "sywyquq"]
    assert result["found songs"] == []


def test_search_songs_v2():
    """ Test ID: Spotify16. Tests that the method returns
    a non-empty dictionary when results are expected.
    This function contains multiple subtests: 
    Test when the list of songs has one element, the user type is guest
    Test when the list has multiple elements, user type is guest
    Test when the list has one element, user type is member
    Test when the list has multiple elements, user type is member
    """
    # wait two seconds before running this test so that the API
    # doesn't reject the connection
    time.sleep(2)
    spotify_api_manager = SpotifyAPIManager()
    # first subtest
    song_list = ["Hello"]
    result = spotify_api_manager.search_songs(song_list)
    assert result["query title"] == ["Hello"]
    assert result["found songs"] != []
    # second subtest
    song_list = ["Running", "Technologic", "It's Time"]
    result = spotify_api_manager.search_songs(song_list)
    assert result["query title"] == ["Running", "Technologic", "It's Time"]
    assert result["found songs"] != []
    # third subtest
    account_link = spotify_api_manager.link_spotify_account()
    assert account_link == True
    song_list = ["Hello"]
    result = spotify_api_manager.search_songs(song_list)
    assert result["query title"] == ["Hello"]
    assert result["found songs"] != []
    # fourth subtest
    song_list = ["Running", "Technologic", "It's Time"]
    result = spotify_api_manager.search_songs(song_list)
    assert result["query title"] == ["Running", "Technologic", "It's Time"]
    assert result["found songs"] != []


def test_linkSpotifyAccount(username=username, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri):
    """
    Tests that the linkSpotifyAccount method runs without error
    """
    # wait two seconds before running this test so that the API
    # doesn't reject the connection
    time.sleep(2)
    # First subtest
    spotify_api_manager = SpotifyAPIManager()
    # example album id for Bastille's Wild World album
    album_id = "1qKjUIVG8KmtYceDBWjfqE"
    album = spotify_api_manager.get_album(album_id)
    assert album.name == "Wild World (Complete Edition)"
    assert album.album_id == album_id
    # Second subtest
    account_link = spotify_api_manager.link_spotify_account()
    assert account_link == True
    album = spotify_api_manager.get_album(album_id)
    assert album.name == "Wild World (Complete Edition)"
    assert album.album_id == album_id


def test_get_artist_v1():
    """ Test ID: Spotify03. Tests that the method returns 
    the correct artist object when given a valid artist id.
    Ensure this works both when the account is linked or not.
    """
    # wait two seconds before running this test so that the API
    # doesn't reject the connection
    time.sleep(2)
    # First subtest
    spotify_api_manager = SpotifyAPIManager()
    # Artist id for Bastille
    artist_id = "7EQ0qTo7fWT7DPxmxtSYEc"
    artist = spotify_api_manager.get_artist(artist_id)
    assert artist.name == "Bastille"
    assert artist.artist_id == artist_id
    # Second subtest
    account_link = spotify_api_manager.link_spotify_account()
    assert account_link == True
    artist = spotify_api_manager.get_artist(artist_id)
    assert artist.name == "Bastille"
    assert artist.artist_id == artist_id


# Tests for the Query class
def test_update_filter_list():
    """ Test ID: Query03 - Query07.
    Tests that filters can be added and removed from the filters list correctly.
    """
    filters = []
    query = Query(filters)
    assert query.filter_list == filters
    filters.append("tempo")
    query.update_filter_list(filters)
    assert query.filter_list == filters
    filters = ["key", "time_ms", "valence"]
    query.update_filter_list(filters)
    assert query.filter_list == filters
    filters.remove("key")
    query.update_filter_list(filters)
    assert query.filter_list == filters


# test adding a song to a spotify playlist
def test_addSong():
    # need a spotify track ID (Moonlight Sonata aka Piano Sonata No. 14, Op. 27 No. 2)
    track = ["7xfSCgVOkQJhVxnqzepATH"]

    # Get the users playlists
    playlists = me.getSpotifyPlaylists()


    # now we must return the tracks from the playlist and make sure the
    # first track is our new track
    response = me.getSpotifyHook().playlist_items(pl_ID,
                                    offset=0,
                                    fields='items.track.name,total',
                                    additional_types=['track'])


    assert response['items'][0]['track']['name'] == "Moonlight Sonata (First Movement from Piano Sonata No. 14, Op. 27 No. 2)"


def test_get_similarity_score():
    """ Test ID: Query 11. Tests that the method returns
    a valid similarity score list with
    values between 0 and 1.
    """
    # First subtest: only two songs, and only one filter
    filters = ["tempo"]
    query = Query(filters)
    seed_song = "Hello"
    songs = query.search_single_song(seed_song)
    score = query.get_similarity_score(songs[0:2])
    assert (score >= 0 and score <= 1)
    # Second subtest: 10 songs, one filter
    score = query.get_similarity_score(songs)
    assert (score >= 0 and score <= 1)
    # Third subtestL only two songs, multiple filters
    filters = ["tempo", "key", "danceability"]
    query.update_filter_list(filters)
    score = query.get_similarity_score(songs[0:2])
    print(score)
    assert (score >= 0 and score <= 1)
    # clear cache on last test
    clear_cache()


# Cleanup
def clear_cache():
    """ delete the cache """
    if os.path.exists(".cache"):
        os.remove(".cache")
    else:
        print("The file does not exist")
