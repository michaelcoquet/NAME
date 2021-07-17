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

function makeConfig(datasets, type, labels, options) {
  var config = {
    type: type,
    data: {
      datasets: datasets,
      labels: labels,
    },
    options: options,
  };

  return config
}

window.onload = function () {
  var radar_options = {
    responsive: true,
  };
  var histo_options = {
    responsive: false,
    legend: {
      display: false
    },
    animation: {
      animateScale: true
    },
    scales: {
      xAxes: [{
        barThickness: 45
      }],
      yAxes: [{
        barPercentage: 1,
        categoryPercentage: 1,
        ticks: {
          beginAtZero: true
        }
      }]
    },
    tooltips: {

    }
  };

  var curr_track_cntxt = document.getElementById('current-track-radar').getContext('2d');
  var top_tracks_cntxt = document.getElementById('top-tracks-radar').getContext('2d');
  var last_tracks_cntxt = document.getElementById('recent-tracks-radar').getContext('2d');
  var liked_tracks_cntxt = document.getElementById('liked-tracks-radar').getContext('2d');
  var playlist_tracks_cntxt = document.getElementById('playlist-tracks-radar').getContext('2d');
  var album_tracks_cntxt = document.getElementById('saved-ablum-tracks-radar').getContext('2d');

  var danceability_dist_cntxt = document.getElementById('danceability-bar').getContext('2d');
  var energy_dist_cntxt = document.getElementById('energy-bar').getContext('2d');
  var key_dist_cntxt = document.getElementById('key-bar').getContext('2d');
  var loudness_dist_cntxt = document.getElementById('loudness-bar').getContext('2d');
  var mode_dist_cntxt = document.getElementById('mode-bar').getContext('2d');
  var speechiness_dist_cntxt = document.getElementById('speechiness-bar').getContext('2d');
  var acousticness_dist_cntxt = document.getElementById('acousticness-bar').getContext('2d');
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

  likedDataset = [makeDataset(profile.liked_tracks_analysis, 'rgba(255, 99, 132, 0.2)', 'Tracks')]

  playlistDataset = [makeDataset(profile.playlist_tracks_analysis, 'rgba(255, 99, 132, 0.2)', 'Tracks')]

  albumDataset = [makeDataset(profile.album_tracks_analysis, 'rgba(255, 99, 132, 0.2)', 'Tracks')]

  window.currentTrackRadar = new Chart(curr_track_cntxt, makeConfig(currentTrackDataset, "radar", radar_labels, radar_options));
  window.topTracksRadar = new Chart(top_tracks_cntxt, makeConfig(topDatasets, "radar", radar_labels, radar_options));
  window.lastTracksRadar = new Chart(last_tracks_cntxt, makeConfig(lastDatasets, "radar", radar_labels, radar_options));
  window.likedTracksRadar = new Chart(liked_tracks_cntxt, makeConfig(likedDataset, "radar", radar_labels, radar_options));
  window.playlistTracksRadar = new Chart(playlist_tracks_cntxt, makeConfig(playlistDataset, "radar", radar_labels, radar_options));
  window.albumTracksRadar = new Chart(album_tracks_cntxt, makeConfig(albumDataset, "radar", radar_labels, radar_options));

  danceability_dataset = [makeDataset(histo_data[0][0], 'rgba(255, 99, 132)', "Last 50 Tracks")];
  energy_dataset = [makeDataset(histo_data[0][1], 'rgba(255, 99, 132)', "Last 50 Tracks")];
  key_dataset = [makeDataset(histo_data[0][2], 'rgba(255, 99, 132)', "Last 50 Tracks")];
  loudness_dataset = [makeDataset(histo_data[0][3], 'rgba(255, 99, 132)', "Last 50 Tracks")];
  mode_dataset = [makeDataset(histo_data[0][4], 'rgba(255, 99, 132)', "Last 50 Tracks")];
  speechiness_dataset = [makeDataset(histo_data[0][5], 'rgba(255, 99, 132)', "Last 50 Tracks")];
  acousticness_dataset = [makeDataset(histo_data[0][6], 'rgba(255, 99, 132)', "Last 50 Tracks")];
  instrumentalness_dataset = [makeDataset(histo_data[0][7], 'rgba(255, 99, 132)', "Last 50 Tracks")];
  liveness_dataset = [makeDataset(histo_data[0][8], 'rgba(255, 99, 132)', "Last 50 Tracks")];
  valence_dataset = [makeDataset(histo_data[0][9], 'rgba(255, 99, 132)', "Last 50 Tracks")];
  tempo_dataset = [makeDataset(histo_data[0][10], 'rgba(255, 99, 132)', "Last 50 Tracks")];

  window.danceabilityBar = new Chart(danceability_dist_cntxt, makeConfig(danceability_dataset, "bar", histo_bins[0][0], histo_options));
  window.energyBar = new Chart(energy_dist_cntxt, makeConfig(energy_dataset, "bar", histo_bins[0][1], histo_options));
  window.keyBar = new Chart(key_dist_cntxt, makeConfig(key_dataset, "bar", histo_bins[0][2], histo_options));
  window.loudnessBar = new Chart(loudness_dist_cntxt, makeConfig(loudness_dataset, "bar", histo_bins[0][3], histo_options));
  window.modeBar = new Chart(mode_dist_cntxt, makeConfig(mode_dataset, "bar", histo_bins[0][4], histo_options));
  window.speechinessBar = new Chart(speechiness_dist_cntxt, makeConfig(speechiness_dataset, "bar", histo_bins[0][5], histo_options));
  window.acousticnessBar = new Chart(acousticness_dist_cntxt, makeConfig(acousticness_dataset, "bar", histo_bins[0][6], histo_options));
  window.instrumentalnessBar = new Chart(instrumentalness_dist_cntxt, makeConfig(instrumentalness_dataset, "bar", histo_bins[0][7], histo_options));
  window.livenessBar = new Chart(liveness_dist_cntxt, makeConfig(liveness_dataset, "bar", histo_bins[0][8], histo_options));
  window.valenceBar = new Chart(valence_dist_cntxt, makeConfig(valence_dataset, "bar", histo_bins[0][9], histo_options));
  window.tempoBar = new Chart(tempo_dist_cntxt, makeConfig(tempo_dataset, "bar", histo_bins[0][10], histo_options));
};