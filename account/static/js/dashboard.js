// function makeDataset(data, backgroundColor, title) {
//     var dataset = {
//         data: data,
//         fill: true,
//         backgroundColor: backgroundColor,
//         borderColor: backgroundColor,
//         pointBorderColor: '#fff',
//         pointHoverBackgroundColor: '#fff',
//         pointHoverBorderColor: 'rgb(255, 99 132)',
//         label: title
//     }
//     return dataset
// }

// function makeConfig(datasets, type, labels) {
//     var config = {
//             type: type,
//             data: {
//                 datasets: datasets,
//                 labels: labels
//             },
//             options: {
//                 responsive: true,
//             },
//     };

//     return config
// }

// window.onload = function() {
//     var curr_track_cntxt = document.getElementById('current-track-radar').getContext('2d');
//     var top_tracks_cntxt = document.getElementById('top-tracks-radar').getContext('2d');
//     var last_tracks_cntxt = document.getElementById('recent-tracks-radar').getContext('2d');
//     var liked_tracks_cntxt = document.getElementById('liked-tracks-radar').getContext('2d');

//     var danceability_dist_cntxt = document.getElementById('danceability-bar').getContext('2d');
//     var energy_dist_cntxt = document.getElementById('energy-bar').getContext('2d');
//     var key_dist_cntxt = document.getElementById('key-bar').getContext('2d');
//     var loudness_dist_cntxt = document.getElementById('loudness-bar').getContext('2d');
//     var mode_dist_cntxt = document.getElementById('mode-bar').getContext('2d');
//     var speechiness_dist_cntxt = document.getElementById('speechiness-bar').getContext('2d');
//     var acousticiness_dist_cntxt = document.getElementById('acousticiness-bar').getContext('2d');
//     var instrumentalness_dist_cntxt = document.getElementById('instrumentalness-bar').getContext('2d');
//     var liveness_dist_cntxt = document.getElementById('liveness-bar').getContext('2d');
//     var valence_dist_cntxt = document.getElementById('valence-bar').getContext('2d');
//     var tempo_dist_cntxt = document.getElementById('tempo-bar').getContext('2d');

//     currentTrackDataset = [makeDataset({{ current_track.feature_repr|safe }}, 'rgba(255, 99, 132, 0.2)', '{{current_track.name|safe}}')];
//     top5Dataset = makeDataset({{ profile.top_tracks_analysis.0|safe }}, 'rgba(255, 145, 0, 0.2)', 'Top 5');
//     top25Dataset = makeDataset({{ profile.top_tracks_analysis.1|safe }}, 'rgba(52, 78, 173, 0.2)', 'Top 25');
//     top50Dataset = makeDataset({{ profile.top_tracks_analysis.2|safe }}, 'rgba(159, 52, 173, 0.2)', 'Top 50');
//     topDatasets = [top5Dataset, top25Dataset, top50Dataset];
    
//     last5Dataset = makeDataset({{ profile.recent_tracks_analysis.0|safe }}, 'rgba(255, 145, 0, 0.2)', 'Last 5');
//     last25Dataset = makeDataset({{ profile.recent_tracks_analysis.1|safe }}, 'rgba(52, 78, 173, 0.2)', 'Last 25');
//     last50Dataset = makeDataset({{ profile.recent_tracks_analysis.2|safe }}, 'rgba(159, 52, 173, 0.2)', 'Last 50');
//     lastDatasets = [last5Dataset, last25Dataset, last50Dataset];

//     likedDataset = [makeDataset({{ profile.liked_tracks_analysis|safe }},'rgba(255, 99, 132, 0.2)', 'Liked Tracks')];

//     window.currentTrackRadar = new Chart(curr_track_cntxt, makeConfig(currentTrackDataset, "radar", {{ labels|safe }}));
//     window.topTracksRadar = new Chart(top_tracks_cntxt, makeConfig(topDatasets, "radar", {{ labels|safe }}));
//     window.lastTracksRadar = new Chart(last_tracks_cntxt, makeConfig(lastDatasets, "radar", {{ labels|safe }}));
//     window.likedTracksRadar = new Chart(liked_tracks_cntxt, makeConfig(likedDataset, "radar", {{ labels|safe }}));

//     temp_labels = ["3.0", "4.0", "5.0", "6.0", "7.0", "8.0", "9.0"];
//     window.danceabilityBar = new Chart(danceability_dist_cntxt, makeConfig(currentTrackDataset, "bar", temp_labels));
//     window.energyBar = new Chart(energy_dist_cntxt, makeConfig(currentTrackDataset, "bar", temp_labels));
//     window.keyBar = new Chart(key_dist_cntxt, makeConfig(currentTrackDataset, "bar", temp_labels));
//     window.loudnessBar = new Chart(loudness_dist_cntxt, makeConfig(currentTrackDataset, "bar", temp_labels));
//     window.modeBar = new Chart(mode_dist_cntxt, makeConfig(currentTrackDataset, "bar", temp_labels));
//     window.speechinessBar = new Chart(speechiness_dist_cntxt, makeConfig(currentTrackDataset, "bar", temp_labels));
//     window.acousticinessBar = new Chart(acousticiness_dist_cntxt, makeConfig(currentTrackDataset, "bar", temp_labels));
//     window.instrumentalnessBar = new Chart(instrumentalness_dist_cntxt, makeConfig(currentTrackDataset, "bar", temp_labels));
//     window.livenessBar = new Chart(liveness_dist_cntxt, makeConfig(currentTrackDataset, "bar", temp_labels));
//     window.valenceBar = new Chart(valence_dist_cntxt, makeConfig(currentTrackDataset, "bar", temp_labels));
//     window.tempoBar = new Chart(tempo_dist_cntxt, makeConfig(currentTrackDataset, "bar", temp_labels));
// };

function makeDataset(data, backgroundColor, title) {
  var dataset = {
    data: data,
    fill: true,
    backgroundColor: backgroundColor,
    borderColor: backgroundColor,
    pointBorderColor: '#fff',
    pointHoverBackgroundColor: '#fff',
    pointHoverBorderColor: 'rgb(255, 99 132)',
    label: title
  }
  return dataset
}

function makeConfig(datasets, type, labels) {
  var config = {
        type: type,
        data: {
            datasets: datasets,
            labels: labels
        },
        options: {
            responsive: true,
        },
  };
  
  return config
}
  
window.onload = function() {
    var curr_track_cntxt = document.getElementById('current-track-radar').getContext('2d');
    var top_tracks_cntxt = document.getElementById('top-tracks-radar').getContext('2d');
    var last_tracks_cntxt = document.getElementById('recent-tracks-radar').getContext('2d');
    var liked_tracks_cntxt = document.getElementById('liked-tracks-radar').getContext('2d');
    
    var danceability_dist_cntxt = document.getElementById('danceability-bar').getContext('2d');
    var energy_dist_cntxt = document.getElementById('energy-bar').getContext('2d');
    var key_dist_cntxt = document.getElementById('key-bar').getContext('2d');
    var loudness_dist_cntxt = document.getElementById('loudness-bar').getContext('2d');
    var mode_dist_cntxt = document.getElementById('mode-bar').getContext('2d');
    var speechiness_dist_cntxt = document.getElementById('speechiness-bar').getContext('2d');
    var acousticiness_dist_cntxt = document.getElementById('acousticiness-bar').getContext('2d');
    var instrumentalness_dist_cntxt = document.getElementById('instrumentalness-bar').getContext('2d');
    var liveness_dist_cntxt = document.getElementById('liveness-bar').getContext('2d');
    var valence_dist_cntxt = document.getElementById('valence-bar').getContext('2d');
    var tempo_dist_cntxt = document.getElementById('tempo-bar').getContext('2d');

    currentTrackDataset = [makeDataset(current_track.feature_repr, 'rgba(255, 99, 132, 0.2)', current_track.name)];
    top5Dataset = makeDataset(profile.top_tracks_analysis[0], 'rgba(255, 145, 0, 0.2)', 'Top 5');
    top25Dataset = makeDataset(profile.top_tracks_analysis[1], 'rgba(52, 78, 173, 0.2)', 'Top 25');
    top50Dataset = makeDataset(profile.top_tracks_analysis[2], 'rgba(159, 52, 173, 0.2)', 'Top 50');
    topDatasets = [top5Dataset, top25Dataset, top50Dataset];
    
    last5Dataset = makeDataset(profile.recent_tracks_analysis[0], 'rgba(255, 145, 0, 0.2)', 'Last 5');
    last25Dataset = makeDataset(profile.recent_tracks_analysis[1], 'rgba(52, 78, 173, 0.2)', 'Last 25');
    last50Dataset = makeDataset(profile.recent_tracks_analysis[2], 'rgba(159, 52, 173, 0.2)', 'Last 50');
    lastDatasets = [last5Dataset, last25Dataset, last50Dataset];

    likedDataset = [makeDataset(profile.liked_tracks_analysis,'rgba(255, 99, 132, 0.2)', 'Liked Tracks')]

    window.currentTrackRadar = new Chart(curr_track_cntxt, makeConfig(currentTrackDataset, "radar", radar_labels));
    window.topTracksRadar = new Chart(top_tracks_cntxt, makeConfig(topDatasets, "radar", radar_labels));
    window.lastTracksRadar = new Chart(last_tracks_cntxt, makeConfig(lastDatasets, "radar", radar_labels));
    window.likedTracksRadar = new Chart(liked_tracks_cntxt, makeConfig(likedDataset, "radar", radar_labels));

    testDataSet = [makeDataset(current_track.feature_repr, 'rgba(255, 99, 132)', "TEST NAME")];
    temp_labels = ["3.0", "4.0", "5.0", "6.0", "7.0", "8.0", "9.0"];
    window.danceabilityBar = new Chart(danceability_dist_cntxt, makeConfig(testDataSet, "bar", temp_labels));
    window.energyBar = new Chart(energy_dist_cntxt, makeConfig(testDataSet, "bar", temp_labels));
    window.keyBar = new Chart(key_dist_cntxt, makeConfig(testDataSet, "bar", temp_labels));
    window.loudnessBar = new Chart(loudness_dist_cntxt, makeConfig(testDataSet, "bar", temp_labels));
    window.modeBar = new Chart(mode_dist_cntxt, makeConfig(testDataSet, "bar", temp_labels));
    window.speechinessBar = new Chart(speechiness_dist_cntxt, makeConfig(testDataSet, "bar", temp_labels));
    window.acousticinessBar = new Chart(acousticiness_dist_cntxt, makeConfig(testDataSet, "bar", temp_labels));
    window.instrumentalnessBar = new Chart(instrumentalness_dist_cntxt, makeConfig(testDataSet, "bar", temp_labels));
    window.livenessBar = new Chart(liveness_dist_cntxt, makeConfig(testDataSet, "bar", temp_labels));
    window.valenceBar = new Chart(valence_dist_cntxt, makeConfig(testDataSet, "bar", temp_labels));
    window.tempoBar = new Chart(tempo_dist_cntxt, makeConfig(testDataSet, "bar", temp_labels));
};