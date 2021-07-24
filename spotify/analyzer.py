# track_avg averages the features of all the given tracks
def tracks_avg(track_json):
    features_avg = [0, 0, 0, 0, 0, 0, 0]
    # [danceability, energy, speechiness, acousticness, instrumentalness, liveness, valence]
    for track in track_json:
        zipped_features = zip(features_avg, track.feature.__repr__("base"))
        features_avg = [x + y for (x, y) in zipped_features]

    if len(track_json) > 0:
        features_avg = [x / len(track_json) for x in features_avg]
        return features_avg
    else:
        return 0
