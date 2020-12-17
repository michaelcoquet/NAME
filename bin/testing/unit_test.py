"""CMPT 370 Group 5 Project: NAME (Nearly Analogous Music Engine)
    Credits: Michael Coquet
             Elizabeth Reid
             Ben Camplin
             Laurence Craig Garcia
             Sean Warren
"""
import os
import time
import pytest

# from name.testing.proof_of_concept import User
# as we work on our app going forward, import classes from the appropriate folder(s)
from name.backend_classes import SongSimilarity
from name.backend_classes import SpotifyAPIManager
from name.backend_classes import Query
from name.backend_classes.song import Artist
from name.backend_classes.song import Album
from name.backend_classes.song import Song
from name.backend_classes.song import SongDetails
from name.backend_classes.playlist import Playlist
from name.backend_classes import Genius_Api_Manager
from name.backend_classes import Lyrics
from name.backend_classes import temporary_storage
from name.backend_classes import User
from name.backend_classes import Group

# Tests for the User class
# def test_setUserType_v1():
#     """
#     Test ID: User01. Normally setUserType would be called from within the Spotify API
#     after a User has linked/ unlinked their account. For this unit test, we simply check that
#     the User type is modified correctly.
#     """
#     user = User(type="Guest")
#     user.setUserType(type="Member")

#     assert user.type == "Member"


# def test_setUserType_v2():
#     """
#     Test ID: User02. Check that the user type is updated correctly from "Member" to "Guest".
#     """
#     user = User(type="Member")
#     user.setUserType(type="Guest")

#     assert user.type == "Guest"


# def test_isGuest_v1():
#     """
#     Test ID: User03. Check that the method returns True when the User type is Guest.
#     """
#     user = User(type="Guest")
#     assert user.isGuest() == True


# def test_isGuest_v2():
#     """
#     Test ID: User04. Check that the method returns False when the User type is not Guest.
#     """
#     user = User(type="Member")

#     assert user.isGuest() == False

def test_user_v1():
    """ Test ID: User01, User02 (add more test cases)
    Test if the methods are correctly returning the right values
    """
    a_user = User()

    # Test the default value for the User, whether the user is
    # logged in or not
    assert a_user.is_member() is False

    # Test for user logging into their spotify account
    result = a_user.link_spotify_account()
    assert result is True

    # Test for the function get_playlists()
    a_playlist = a_user.get_playlists()
    b_playlist = a_user.spotify_manager.get_member_playlists()
    for items_a, items_b in zip(a_playlist, b_playlist):
        items_a.playlist_id == items_b.playlist_id

    # Test for getting the spotify id of the member
    spotify_id = a_user.get_account_id()
    assert spotify_id == a_user.spotify_manager.get_user_id()

    # Test for member logging out
    a_user.logout()
    assert a_user.is_member() is False


def test_group_v1():
    """ Test ID:Group01, Group02, Group05, Group12, Group13. 
        Check if the methods are returning the correct data
    """
    test_group = ["group1", 'owner1', ["user1", "user2"], [6, 8]]
    
    # Initialize Group object
    a_group = Group(test_group[0], test_group[1], test_group[2], test_group[3])

    # Test for assigning the group id
    a_group.assign_id(1)
    assert a_group.group_id == 1

    # Test for getting the members of the group
    for members_a, members_b in zip(a_group.member_list, test_group[3]):
        assert members_a == members_b

    # Test for updating the playlists of the group
    # For testing purposes, we're just going to pass strings from a list
    list_of_playlist = ["Playlist1", "Playlist2", "Playlist3"]
    a_group.update_playlists(list_of_playlist)
    updated_playlist = a_group.group_playlists
    assert updated_playlist == list_of_playlist
    # Test for inviting a member to the group
    member_ids = [1, 35, 24, 5]
    a_group.invite_members(member_ids)
    for members in member_ids:
        assert members in a_group.invite_list

    # Test for an invited member accepting the invitation
    ACCEPTED_MEMBER = 1
    a_group.accept_invite(ACCEPTED_MEMBER)
    assert member_ids[0] in a_group.member_list

    # Test for an invited member declining the invitation
    # a_group.decline_invite(35)
    # assert member_ids[1] not in a_group.invite_list

    # Test for adding a new member
    NEW_MEMBER_ID = 10
    a_group.add_member(NEW_MEMBER_ID)
    assert NEW_MEMBER_ID in a_group.member_list

    # Test if the added member is successfully added to member list
    assert a_group.member_exists(NEW_MEMBER_ID) is True


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
        Test when the list of songs has one element, the user type is
        guest
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
        Test when the list of songs has one element, the user type is
        guest
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
        Ensure this works both before and after an account has been
        linked
    """
    # wait two seconds before running this test so that the API
    # doesn't reject the connection
    time.sleep(2)
    # First subtest
    spotify_api_manager = SpotifyAPIManager()
    # example album id for Bastille's Wild World album
    id = "1qKjUIVG8KmtYceDBWjfqE"
    album = spotify_api_manager.get_album(id)
    assert album.name == "Wild World (Complete Edition)"
    assert album.id == id
    # Second subtest
    account_link = spotify_api_manager.link_spotify_account()
    assert account_link == True
    album = spotify_api_manager.get_album(id)
    assert album.name == "Wild World (Complete Edition)"
    assert album.id == id



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
    id = "7EQ0qTo7fWT7DPxmxtSYEc"
    artist = spotify_api_manager.get_artist(id)
    assert artist.name == "Bastille"
    assert artist.id == id
    # Second subtest
    account_link = spotify_api_manager.link_spotify_account()
    assert account_link == True
    artist = spotify_api_manager.get_artist(id)
    assert artist.name == "Bastille"
    assert artist.id == id


def test_get_member_playlists():
    """ Test ID: Spotify11. Tests that the user's spotify
        playlists are correctly returned as a list of playlist
        objects.
        This also indirectly tests the helper function,
        create_playlist_object.
    """
    # wait two seconds before running this test so that the API
    # doesn't reject the connection
    time.sleep(2)
    spotify_api_manager = SpotifyAPIManager()
    spotify_api_manager.link_spotify_account()
    playlists = spotify_api_manager.get_member_playlists()
    # determine if a list of playlist objects are indeed returned
    # However, check manually if the details are correct
    assert len(playlists) != 0
    assert playlists[0].playlist_name != ""
    assert playlists[0].songs != []


# def test_add_member_playlist():
#     """ TestID: Spotify13. Tests that a new playlist can
#     be added to the member's spotify account. Comment
#     this test out after running once to avoid created a whole
#     bunch of copies of the same playlist
#     """
#     time.sleep(2)
#     spotify_api_manager = SpotifyAPIManager()
#     spotify_api_manager.link_spotify_account()
#     a_playlist = spotify_api_manager.spotify.playlist("5IkBS6w09oYhVIBRmAvHEv")
#     playlist = spotify_api_manager.create_playlist_object(a_playlist)
#     result = spotify_api_manager.add_member_playlist(playlist)
#     assert result != []
#     assert result.playlist_name == "Opera"
#     assert result.songs != []


def test_get_recently_played_songs():
    """ Test ID: Spotify18. Tests that recently
        played songs can be returned properly as a list of song
        objects.
    """
    # wait two seconds to avoid a timeout from the API
    time.sleep(2)
    spotify_api_manager = SpotifyAPIManager()
    spotify_api_manager.link_spotify_account()
    recent_songs = spotify_api_manager.get_recently_played_songs(10)
    assert len(recent_songs) > 0 and len(recent_songs) <= 10
    assert recent_songs[0].song_name != ""


def test_get_top_songs():
    """ Test ID: Spotify19. Tests that the users top songs
        can be returned properly as a list of song objects.
    """
    # wait two seconds to avoid a timeout from the API
    time.sleep(2)
    spotify_api_manager = SpotifyAPIManager()
    spotify_api_manager.link_spotify_account()
    top_songs = spotify_api_manager.get_top_songs()
    assert len(top_songs) > 0 and len(top_songs) <= 20
    assert top_songs[0].song_name != ""


def test_refresh_auth_token():
    """ Test ID: Spotify20. Tests that an auth token is
        properly collected from the cache and refreshed.
        Note that manual testing had to be done, since the tokens
        take an hour to expire.
    """
    # wait two seconds to avoid a timeout from the API
    time.sleep(2)
    spotify_api_manager = SpotifyAPIManager()
    spotify_api_manager.link_spotify_account()
    # try getting some user info
    id = spotify_api_manager.get_user_id()
    # try to refresh the token when it definitely won't be expired
    spotify_api_manager.refresh_auth_token()
    assert id == spotify_api_manager.get_user_id()


def test_get_top_artists():
    """ Test ID: Spotify21. Tests that the users top artists
        can be returned properly as a list of artist objects.
    """
    # wait two seconds to avoid a timeout from the API
    time.sleep(2)
    spotify_api_manager = SpotifyAPIManager()
    spotify_api_manager.link_spotify_account()
    top_artists = spotify_api_manager.get_top_artists()
    assert top_artists != []


def test_get_song_genres():
    """ Test ID: Spotify22. Tests that a list of genres
        are returned correctly for a given song object. Make sure
        this works whether or not the user is logged in to spotify.
    """
    # subtest 1: not logged in
    spotify_api_manager = SpotifyAPIManager()
    songs = spotify_api_manager.search_songs(["Highway to Hell"])
    song = songs["found songs"][0]
    genres = spotify_api_manager.get_song_genres(song)
    assert genres != []
    # rock should be here, so check to see if it is
    assert "rock" in genres
    # subtest 2: logged in
    spotify_api_manager.link_spotify_account()
    genres = spotify_api_manager.get_song_genres(song)
    assert genres != []
    assert "rock" in genres


# Tests for the Query class
def test_update_filter_list():
    """ Test ID: Query03 - Query07.
        Tests that filters can be added and removed from the
        filters list correctly.
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


def test_search_single_song_v1():
    """ Test ID: Query08. Tests that the query returns song results
        when a valid song is entered.
    """
    query = Query(["tempo", "key"])
    song = "Hello"
    assert query.search_single_song(song) != []


def test_search_single_song_v2():
    """ Test ID: Query09. Tests that the query returns an empty
        list when Spotify can't find the given song.
    """
    query = Query(["tempo", "key"])
    song = "hfjdkshfjsue"
    assert query.search_single_song(song) == []


def test_get_song_info():
    """ Test ID: Query 10. Tests that the query returns song
        info for the filter list when given a valid song object.
    """
    # First subtest: only one filter
    query = Query(["tempo"])
    song = "Hello"
    song = query.search_single_song(song)[0]
    song_info = query.get_song_info(song)
    assert list(song_info.keys()) == ["tempo"]
    assert song_info["tempo"] != None
    # Second subtest: multiple filters
    query.update_filter_list(["tempo", "key", "danceability"])
    song_info = query.get_song_info(song)
    assert list(song_info.keys()) == ["tempo", "key", "danceability"]
    assert song_info["tempo"] != None
    assert song_info["key"] != None
    assert song_info["danceability"] != None


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


def test_song_details_v2():
    """ A test for checking whether the passed in values
        are in the right range of the
        expected values for each audio features
    """
    audio_features = {"danceability": 0.527,"energy": 0.834,
                      "key": 1, "loudness": -5.531,
                      "mode": 1, "speechiness": 0.0447,
                      "acousticness": 0.00107, "instrumentalness": 0.000102,
                      "liveness": 0.0993, "valence": 0.422,
                      "tempo": 110.065, "duration_ms": 198333,
                      "time_signature": 4}

    song_details = SongDetails(audio_features)

    # https://open.spotify.com/track/0q5lnUuDhlogtYCOubNQhQ
    LONGEST_TRACK_DURATION = 15600000 
    # Test if the given value exceeds the expected value
    assert song_details.danceability <= 1
    assert song_details.key <= 12
    assert song_details.energy <= 1
    assert song_details.mode <= 1
    assert song_details.loudness <= 0
    assert song_details.speechiness <= 1
    assert song_details.acousticness <= 1
    assert song_details.instrumentalness <= 1
    assert song_details.liveness <= 1
    assert song_details.valence <= 1
    assert song_details.tempo <= 500
    assert song_details.duration <= LONGEST_TRACK_DURATION
    assert song_details.time_signature <= 7


def test_song_details_v3():
    """ A test where the given data is not correct.
        In this case if the given value is a string instead
        f an int.
    """
    audio_features = {"danceability": 0.527,"energy": 0.834,
                      "key": 1, "loudness": -5.531,
                      "mode": 1,"speechiness": 0.0447,
                      "acousticness": 0.00107,"instrumentalness": 0.000102,
                      "liveness": 0.0993, "valence": 0.422,
                      "tempo": 110.065, "duration_ms": 198333,
                      "time_signature": 4}

    song_details = SongDetails(audio_features)
    assert song_details.danceability != '0.527'
    assert song_details.key != '1'
    assert song_details.energy != '0.834'
    assert song_details.mode != '1'
    assert song_details.loudness != '-5.531'
    assert song_details.speechiness != '0.0447'
    assert song_details.acousticness != '0.00107'
    assert song_details.instrumentalness != '0.000102'
    assert song_details.liveness != '0.0993'
    assert song_details.valence != '0.422'
    assert song_details.tempo != '110.065'
    assert song_details.duration != '198333'
    assert song_details.time_signature != '4'


def test_song_v1():
    """ Test IDs: Song01, Album01-02, Artist01-02.
        Should return the correct
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
    assert song_obj.id == song["id"]
    assert song_obj.song_name == song["name"]
    # Subtest for the Artist class
    assert song_obj.song_artist[0].name == song["artists"][0]["name"]
    assert song_obj.song_artist[0].id == song["artists"][0]["id"]
    # Subtest for the Album class
    assert song_obj.album_details.name == song["album"]["name"]
    assert song_obj.album_details.id == song["album"]["id"]
    assert song_obj.album_details.type == song["album"]["album_type"]
    assert song_obj.album_details.size == song["album"]["total_tracks"]


def test_playlist_v1():
    """ Test ID: Playlist01-012. Test for the Playlist class,
        Test each method if it is returning the correct values
        after the object is instantiated
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


def test_playlist_v2():
    """
    A test when the given playlist is empty
    """
    a_playlist = {"name": "Empty Playlist",
                    "owner": {"display_name": "test1",
                            "id": "qwerty"},
                    "id": "asdaf",
                    "tracks": {"total": 0}
                    }

    playlist_obj = Playlist(a_playlist, playlist_tracks=[])

    assert playlist_obj.size == 0
    assert playlist_obj.songs == []



def test_genius_api_manager():
    """ Test ID: Genius01-03. Tests that the Genius API returns
        the correct lyrics for the requested song.
        Tests that no lyrics are returned if
        a song is an instrumental.
    """
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


def test_lyrics():
    """ Test ID: Lyrics01-08. Tests that the lyrics objects correctly
        interfaces with the Genius API Manager class and gets the
        correct lyrics. Tests the getter functions to make sure they
        return the correct info.
    """

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
    # clear cache on last test
    clear_cache()


# Cleanup
def clear_cache():
    """ delete the cache """
    if os.path.exists(".cache"):
        os.remove(".cache")
    else:
        print("The file does not exist")
