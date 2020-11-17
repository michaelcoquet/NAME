""" TODO: fill in
"""
import tkinter as tk
from .member_home_frame import MemberHomeFrame


class AllPlaylistsFrame(MemberHomeFrame):
    """ TODO: fill in

    Args:
        tk ([type]): TODO: fill in
    """
    def __init__(self, parent, container):
        super().__init__(parent, container)
        self.container = container
        self.parent = parent

    def init_upper_grid(self):
        super().init_upper_grid()
        self.all_playlists_button["state"] = tk.DISABLED
        self.latest_playlist_button["state"] = tk.NORMAL

    def init_middle_grid(self):
        super().init_middle_grid()


    def init_lower_grid(self):
        super().init_lower_grid()
        self.edit_button.grid_forget()
        self.save_spotify_button.grid_forget()

        self.list_from_list_button = tk.Button(self.lower_grid)
        self.list_from_list_button["text"] = "Find Songs Similar \nto Selected Playlist"
        self.list_from_list_button.grid(row=0, column=0)

        self.song_sim_button = tk.Button(self.lower_grid)
        self.song_sim_button["text"] = "get playlist song similarity"
        self.song_sim_button.grid(row=0, column=2)
