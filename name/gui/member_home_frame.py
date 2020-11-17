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

    def init_lower_grid(self):
        super().init_lower_grid()
        self.remove_all_button.grid_forget()
        self.similar_songs_button.grid_forget()

        self.edit_button = tk.Button(self.lower_grid)
        self.edit_button["text"] = "Edit"
        self.edit_button.grid(row=0, column=0)

        self.save_spotify_button = tk.Button(self.lower_grid)
        self.save_spotify_button["text"] = "Save to Spotify"
        self.save_spotify_button.grid(row=0, column=2)

    def init_upper_grid(self):
        super().init_upper_grid()
        self.create_playlist_button.grid_forget()
        self.compare_songs_button.grid_forget()
        self.get_song_info_button.grid_forget()
        self.song_search_entry.grid_forget()
        self.filters_dropdown.grid_forget()
        self.song_search_button.grid_forget()

        self.latest_playlist_button = tk.Button(self.upper_grid, state=tk.DISABLED)
        self.latest_playlist_button["text"] = "Latest Playlist"
        self.latest_playlist_button.grid(row=1, column=0)

        self.all_playlists_button = tk.Button(self.upper_grid)
        self.all_playlists_button["text"] = "All Playlists"
        self.all_playlists_button.grid(row=1, column=1)

        self.listening_habits_button = tk.Button(self.upper_grid)
        self.listening_habits_button["text"] = "Your Listening Habits"
        self.listening_habits_button.grid(row=1, column=2)
