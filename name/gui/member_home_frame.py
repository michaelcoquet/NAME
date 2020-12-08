"""CMPT 370 Group 5 Project: NAME (Nearly Analogous Music Engine)
    Credits: Michael Coquet
             Elizabeth Reid
             Ben Camplin
             Laurence Craig Garcia
             Sean Warren
"""
import tkinter as tk

from .home_page_frame import HomePageFrame


class MemberHomeFrame(HomePageFrame):
    """ Main member home page frame that other corresponding member
        frames inherit

    Args:
        tk (Frame): Inherits the main home page
    """
    def grid_unmap(self):
        super().grid_unmap()
        self.edit_button.grid_remove()
        self.save_spotify_button.grid_remove()
        self.latest_playlist_button.grid_remove()
        self.all_playlists_button.grid_remove()
        self.listening_habits_button.grid_remove()
        self.get_song_info_button.grid_remove()

    def grid_remember(self):
        super().grid_remember()
        self.create_playlist_button.grid_remove()
        self.compare_songs_button.grid_remove()
        self.playlist_info_button.grid_remove()
        self.song_search_entry.grid_remove()
        self.filters_dropdown.grid_remove()
        self.song_search_button.grid_remove()
        self.similar_songs_button.grid_remove()
        self.remove_all_button.grid_remove()
        self.remove_button.grid_remove()

        self.edit_button.grid()
        self.save_spotify_button.grid()
        self.latest_playlist_button.grid()
        self.all_playlists_button.grid()
        self.listening_habits_button.grid()

        self.display_data(self.parent.song_object_list)

    def grid_init(self):
        super().grid_init()

    def init_lower_grid(self):
        super().init_lower_grid()
        self.remove_all_button.grid_remove()
        self.remove_button.grid_remove()
        self.similar_songs_button.grid_remove()

        self.edit_button = tk.Button(
            self.lower_grid,
            text="Edit",
            command=self.edit_command)
        self.edit_button.grid(row=0, column=0)

        self.save_spotify_button = tk.Button(
            self.lower_grid,
            text="Save to Spotify",
            command=self.save_to_spotify_command)
        self.save_spotify_button.grid(row=0, column=2)

        self.playlist_info_button = tk.Button(
            self.lower_grid,
            text="Playlist Info",
            command=self.playlist_info_command
        )
        self.playlist_info_button.grid(row=0, column=1)

    def init_middle_grid(self):
        super().init_middle_grid()
        container = tk.Frame(self.middle_grid)
        container.grid(row=0, column=1, sticky="n")
        self.get_song_info_button = tk.Button(
            container,
            text="Get Song Info",
            command=self.get_song_info_command)
        self.get_song_info_button.grid(row=0, column=0)

    def init_upper_grid(self):
        super().init_upper_grid()
        self.create_playlist_button.grid_remove()
        self.compare_songs_button.grid_remove()
        self.get_song_info_button.grid_remove()
        self.song_search_entry.grid_remove()
        self.filters_dropdown.grid_remove()
        self.song_search_button.grid_remove()

        self.latest_playlist_button = tk.Button(
            self.upper_grid,
            state=tk.DISABLED,
            text="Latest Playlist",
            command=self.latest_playlist_command
            )
        self.latest_playlist_button.grid(row=1, column=0)

        self.all_playlists_button = tk.Button(
            self.upper_grid,
            text="All Playlists",
            command=self.all_playlists_command
            )
        self.all_playlists_button.grid(row=1, column=1)

        self.listening_habits_button = tk.Button(
            self.upper_grid,
            text="Your Listening Habits",
            command=self.listening_habits_command)
        self.listening_habits_button.grid(row=1, column=2)

    def latest_playlist_command(self):
        """command for the latest playlist button
        """
        return 1

    def save_to_spotify_command(self):
        """command for the save to spotify button
        """
        self.switch_frame("Save Playlist")

    def all_playlists_command(self):
        """command for the all palylists button
        """
        self.switch_frame("All Playlists")

    def listening_habits_command(self):
        """command for the listening habits button
        """
        self.switch_frame("Listening Habits")
        # populate the listening habits page with info
        # top songs
        top_songs = self.parent.user.spotify_manager.get_top_songs()
        self.parent.frames[self.parent.get_frame_id("Listening Habits")].display_top_songs(top_songs)
        # recent songs
        recent_songs = self.parent.user.spotify_manager.get_recently_played_songs(limit=25)
        self.parent.frames[self.parent.get_frame_id("Listening Habits")].display_recent_songs(recent_songs)
        # top artists
        top_artists = self.parent.user.spotify_manager.get_top_artists()
        self.parent.frames[self.parent.get_frame_id("Listening Habits")].display_top_artists(top_artists)

    def edit_command(self):
        """command for the edit button
        """
        self.switch_frame("Playlist Edit")

    def playlist_info_command(self):
        """command for the playlist info button
        """
        self.switch_frame("Playlist Info")

    def get_song_info_command(self):
        """command for the get song info button
        """
        self.switch_frame("Song Info Member")

        song_list = []

        # get the song object(s) that are currently selected
        for song in self.parent.song_object_list:
            for selection in self.song_treeview.selection():
                tmp = [artist.name for artist in song.song_artist]
                tmp = ", ".join(tmp)
                if (
        song.song_name == self.song_treeview.item(selection)["values"][0] and
        tmp == self.song_treeview.item(selection)["values"][2]
                ):
                    # found a corresponding song object
                    song_list.append(song)

        self.parent.frames[self.parent.get_frame_id("Song Info Member")].display_details(song_list)

