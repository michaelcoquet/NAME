# track_avg averages the features of all the given tracks
def tracks_avg(tracks):
    features_avg = [0, 0, 0, 0, 0, 0, 0]
    # [danceability, energy, speechiness, acousticness, instrumentalness, liveness, valence]
    for track in tracks:
        zipped_features = zip(features_avg, track.feature.__repr__())
        features_avg = [x + y for (x, y) in zipped_features]

    features_avg = [x / len(tracks) for x in features_avg]
    return features_avg
