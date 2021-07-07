from django.shortcuts import render


# user_data = get_user_info(social)
# print("\n\n{}'s Profile:".format(user_data["display_name"]))
# current_track = get_playing_track(social)
# if current_track != None:
#     artists = []
#     for artist in current_track["item"]["artists"]:
#         artists.append(artist["name"])
#     print(
#         '\tCurrently Playing Track: "{}" --- '.format(
#             current_track["item"]["name"]
#         ),
#         end="",
#     )
#     print(*artists, sep=", ")
# print("\temail: {}".format(user_data["email"]))
# print(
#     "\t# of Followers: {}\n\n".format(user_data["followers"]["total"])
# )
# albums = get_saved_albums(social)
# albums_list = []
# for item in albums["items"]:
#     albums_list.append("\t\t" + item["album"]["name"])
# print("\tSaved Albums: ")
# print(*albums_list, sep="\n")

# tracks = get_saved_tracks(social)
# track_list = []
# artists = []
# for item in tracks["items"]:
#     for artist in item["track"]["artists"]:
#         artists.append(artist["name"])
#     track_str = '\t\t"{}"'.format(item["track"]["name"])
#     track_str = track_str + " --- " + ", ".join(artists)
#     artists = []
#     track_list.append(track_str)

# print("\tSaved Tracks:")
# print(*track_list, sep="\n")

# top_artists = get_top_artists(social)
# top_artists_list = []
# for item in top_artists["items"]:
#     top_artists_list.append("\t\t" + item["name"])
# print("\n\tTop Artists:")
# print(*top_artists_list, sep="\n")

# top_tracks = get_top_tracks(social)
# print("\tTop Tracks:")
# track_list = []
# artists = []
# for item in top_tracks["items"]:
#     for artist in item["artists"]:
#         artists.append(artist["name"])
#     track_str = '\t\t"{}"'.format(item["name"])
#     track_str = track_str + " --- " + ", ".join(artists)
#     artists = []
#     track_list.append(track_str)
# print(*track_list, sep="\n")

# recent_tracks = get_recently_played_tracks(social)
# print("\n\tRecently Played Tracks:")
# track_list = []
# artists = []
# for item in recent_tracks["items"]:
#     for artist in item["track"]["artists"]:
#         artists.append(artist["name"])
#     track_str = '\t\t"{}"'.format(item["track"]["name"])
#     track_str = track_str + " --- " + ", ".join(artists)
#     artists = []
#     track_list.append(track_str)
# print(*track_list, sep="\n")

# print("\tPlaylists:")
# playlists = get_playlists(social)
# playlist_names = []
# for item in playlists["items"]:
#     playlist_names.append("\t\t" + item["name"])
# print(*playlist_names, sep="\n")
# print("\n")
