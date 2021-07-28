from spotify.models import Track

# track_avg averages the features of all the given tracks
def tracks_avg(tracks_json):
    features_avg = [0, 0, 0, 0, 0, 0, 0]
    # [danceability, energy, speechiness, acousticness, instrumentalness, liveness, valence]
    for track in tracks_json:
        track_query = Track.objects.filter(id=track["id"])
        if track_query.count() > 0:
            track_query = track_query.get()
            feature = track_query.feature
            feature = [
                feature["danceability"] * 100,
                feature["energy"] * 100,
                feature["speechiness"] * 100,
                feature["acousticness"] * 100,
                feature["instrumentalness"] * 100,
                feature["liveness"] * 100,
                feature["valence"] * 100,
            ]
            zipped_features = zip(features_avg, feature)
            features_avg = [x + y for (x, y) in zipped_features]

    if len(tracks_json) > 0:
        features_avg = [x / len(tracks_json) for x in features_avg]
        return features_avg
    else:
        return 0
