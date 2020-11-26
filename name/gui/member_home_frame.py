""" TODO: fill in
"""
import tkinter as tk

from .home_page_frame import HomePageFrame


class MemberHomeFrame(HomePageFrame):
    """ TODO: fill in

    Args:
        tk ([type]): TODO: fill in
    """
    def __init__(self, parent, container):
        super().__init__(parent, container)
        self.container = container
        self.parent = parent

    def grid_forget(self):
        super().grid_forget()
        self.edit_button.grid_forget()
        self.save_spotify_button.grid_forget()
        self.latest_playlist_button.grid_forget()
        self.all_playlists_button.grid_forget()
        self.listening_habits_button.grid_forget()
        self.get_song_info_button.grid_forget()

    def init_lower_grid(self):
        super().init_lower_grid()
        self.remove_all_button.grid_forget()
        self.similar_songs_button.grid_forget()

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
        self.get_song_info_button = tk.Button(
            self.middle_grid,
            text="Get Song Info",
            command=self.get_song_info_command)
        self.get_song_info_button.grid(row=0, column=1, sticky="n")

    def init_upper_grid(self):
        super().init_upper_grid()
        self.create_playlist_button.grid_forget()
        self.compare_songs_button.grid_forget()
        self.get_song_info_button.grid_forget()
        self.song_search_entry.grid_forget()
        self.filters_dropdown.grid_forget()
        self.song_search_button.grid_forget()

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
        # TODO: BACKEND - add logic to fetch the users latest playlist form persistent
        #       storage and load into the listbox
        return 1

    def save_to_spotify_command(self):
        """command for the save to spotify button
        """

        # TODO: BACKEND add logic to save this latest playlist (the one currently being
        # displayed) to the users spotify account
        return 1

    def all_playlists_command(self):
        """command for the all palylists button
        """
        self.switch_frame("All Playlists")

    def listening_habits_command(self):
        """command for the listening habits button
        """
        self.switch_frame("Listening Habits")

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
        self.switch_frame("Song Info")