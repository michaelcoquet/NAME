import os
import time
import pytest

# from proof_of_concept import User
# as we work on our app going forward, import classes from the appropriate folder(s)
# from name.backend_classes import SongSimilarity
import name.backend_classes.spotify_api_manager import SpotifyAPIManager
from name.backend_classes.song import Artist
from name.backend_classes.song import Album
from name.backend_classes.song import Song
from name.backend_classes.song import SongDetails
from name.backend_classes.playlist import Playlist

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
    """ Test ID: SongSim01. Check that the method
    returns a value between 0 and 1.
    """
    song_similarity_calculator = SongSimilarity(["exampleSong"], ["duration_ms"])
    result = song_similarity_calculator.compare_all()

    assert (result >= 0 and result <= 1)


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
    spotify_api_manager = SpotifyAPIManager()
    result = spotify_api_manager.get_user_id()
    assert result == None


def test_get_user_id_v2():
    """ Test ID: Spotify07. Should return the current member
    ID when logged in to Spotify. 
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


def test_get_album_v1():
    """ Test ID: Spotify05. Tests that the method returns 
    the correct album object when given a valid artist id.
    Ensure this works both before and after an account has been linked
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
    # clean cache on last test
    clear_cache()

def test_song_details_v1():
    """ Test ID: SongDetails01 - SongDetails013
    Check if the class is returning the correct values for each
    of the audio features.
    """
    # Data to be passed in
    audio_features = {"danceability": 0.527,"energy": 0.834,
                      "key": 1, "loudness": -5.531,
                      "mode": 1,"speechiness": 0.0447,
                      "acousticness": 0.00107,"instrumentalness": 0.000102,
                      "liveness": 0.0993, "valence": 0.422,
                      "tempo": 110.065, "duration_ms": 198333,
                      "time_signature": 4}

    # Pass in a audio features object
    song_details = SongDetails(audio_features)
    # Test for every audio features of the song
    assert song_details.danceability == audio_features["danceability"]
    assert song_details.energy == audio_features["energy"]
    assert song_details.key == audio_features["key"]
    assert song_details.mode == audio_features["mode"]
    assert song_details.loudness == audio_features["loudness"]
    assert song_details.speechiness == audio_features["speechiness"]
    assert song_details.acousticness == audio_features["acousticness"]
    assert song_details.instrumentalness == audio_features["instrumentalness"]
    assert song_details.liveness == audio_features["liveness"]
    assert song_details.valence == audio_features["valence"]
    assert song_details.tempo == audio_features["tempo"]
    assert song_details.duration == audio_features["duration_ms"]
    assert song_details.time_signature == audio_features["time_signature"]

def test_song_v1():
    """ Test IDs: Song01, Album01-02, Artist01-02. Should return the correct 
    values for each of the attribute from the given data
    """
    # Data of the song
    song = {"name": 'Perfect',
            "id": "4j3X4KX8rURekAVIFUhI23",
            "artists": [
                        {"name": "Simple Plan",
                         "id": "2p4FqHnazRucYQHyDCdBrJ"
                         }   
                      ],
            "album": {
                    "album_type": "album",
                    "id": "3W6TEVlmaP22E4KvWY9HrS",
                    "name": "No Pads, No Helmets...Just Balls (15th Anniversary Tour Edition)",
                    "total_tracks": 19
                        }
            }
    # Audio features of the song
    audio_features = {"danceability": 0.494,"energy": 0.672,
                      "key": 3, "loudness": -4.877,
                      "mode": 1,"speechiness": 0.0405,
                      "acousticness": 0.0273,"instrumentalness": 0.0,
                      "liveness": 0.105, "valence": 0.557,
                      "tempo": 156.208, "duration_ms": 277027,
                      "time_signature": 4}

    # Create the Song object
    song_obj = Song(song, audio_features)
    # Test for Song class attributes, if it is returning the correct data
    assert song_obj.song_id == song["id"]
    assert song_obj.song_name == song["name"]
    # Subtest for the Artist class
    assert song_obj.song_artist[0].name == song["artists"][0]["name"]
    assert song_obj.song_artist[0].artist_id == song["artists"][0]["id"]
    # Subtest for the Album class
    assert song_obj.album_details.name == song["album"]["name"]
    assert song_obj.album_details.album_id == song["album"]["id"]
    assert song_obj.album_details.type == song["album"]["album_type"]
    assert song_obj.album_details.size == song["album"]["total_tracks"]

def test_playlist_v1():
    """
    Test ID: Playlist01-012. Test for the Playlist class, Test each method
    if it is returning the correct values after the object is instantiated
    """
    a_playlist = {"name": "My playlist",
                  "owner": {"display_name": "test1", 
                            "id": 'qwertyu'},
                  "id": "asdfghjqwer",
                  "tracks": {"total": 1}
                 }

    # an object to pass in
    song = {"name": 'Perfect',"id": "a1",
            "artists": [{"name": "","id": ""} ],
            "album": {"album_type": "a","id": "",
            "name": "","total_tracks": 19}}

    # an object to pass in
    audio_features = {"danceability": 0.494,"energy": 0.672,
                      "key": 3, "loudness": -4.877,
                      "mode": 1,"speechiness": 0.0405,
                      "acousticness": 0.0273,"instrumentalness": 0.0,
                      "liveness": 0.105, "valence": 0.557,
                      "tempo": 156.208, "duration_ms": 277027,
                      "time_signature": 4}

    # Convert the objects above into a Song object
    playlist_tracks = [Song(song, audio_features)]
    playlist_obj = Playlist(a_playlist, playlist_tracks)

    assert playlist_obj.playlist_name == a_playlist["name"]
    assert playlist_obj.playlist_owner == a_playlist["owner"]["id"]
    assert playlist_obj.playlist_id == a_playlist["id"]
    assert playlist_obj.songs == playlist_tracks
    assert playlist_obj.size == len(playlist_tracks)

    # Test for updating the playlist name
    new_name = "My playlist 2"
    playlist_obj.update_playlist_name(new_name)
    assert playlist_obj.playlist_name == new_name

    # # Test for adding songs to the playlist
    song2 = {"name": 'Perfect',"id": "a2",
            "artists": [{"name": "","id": ""}],
            "album": {"album_type": "a","id": "",
            "name": "","total_tracks": 19}}

    song2_obj = Song(song2, audio_features)
    playlist_obj.add_song(song2_obj)
    assert playlist_obj.songs.__contains__(song2_obj)
    # Test for the updated size of the playlist
    new_size = 2
    assert playlist_obj.size == new_size

    # Test for removing a song from the playlist
    playlist_obj.remove_song(song2["id"])
    assert not playlist_obj.songs.__contains__(song2["id"])

    # Test for getting the list of the audio features of each song
    song_feat = playlist_obj.get_song_features()
    assert song_feat[0] == audio_features


# Cleanup
def clear_cache():
    """ delete the cache """
    if os.path.exists(".cache"):
        os.remove(".cache")
    else:
        print("The file does not exist")
