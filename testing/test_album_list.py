import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

birdy_uri = 'spotify:artist:6WUBKShvmIaeJZAevA33sR'
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

results = spotify.artist_albums(birdy_uri, album_type='album')
albums = results['items']

expected = ['My Dear Little Angle', 'Waste & Tragedy', 'the smalls', 'To Each A Zone']
test_list = []

while results['next']:
    results = spotify.next(results)
    albums.extend(results['items'])

for album in albums:
    test_list.append(album['name'])


if test_list == expected:
    print("Success: album list matches expected results")
else:
    print("Failure: album list for artist doesn't match expected results")