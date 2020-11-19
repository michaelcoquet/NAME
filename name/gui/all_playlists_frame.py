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

    def grid_forget(self):
        super().grid_forget()
        self.list_from_list_button.grid_forget()
        self.song_sim_button.grid_forget()

    def init_upper_grid(self):
        super().init_upper_grid()
        self.all_playlists_button["state"] = tk.DISABLED
        self.latest_playlist_button["state"] = tk.NORMAL

    def init_middle_grid(self):
        super().init_middle_grid()
        self.get_song_info_button.grid_forget()

    def init_lower_grid(self):
        super().init_lower_grid()
        self.edit_button.grid_forget()
        self.save_spotify_button.grid_forget()

        self.list_from_list_button = tk.Button(
            self.lower_grid,
            text="Create new playlist\n from this playlist",
            command=self.list_from_list_command)
        self.list_from_list_button.grid(row=0, column=0)

        self.song_sim_button = tk.Button(
            self.lower_grid,
            text="get playlist\n song similarity",
            command=self.song_sim_command)
        self.song_sim_button.grid(row=0, column=2)

    def list_from_list_command(self):
        """comamnd for the create playlist from this playlist button
        """

        # TODO: connect with backend
        self.switch_frame("Create Sim Playlist")

    def song_sim_command(self):
        """command for the get playlist song similarity button
        """
        # TODO: connect to backend
        return 1
