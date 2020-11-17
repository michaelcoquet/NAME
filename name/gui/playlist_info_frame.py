""" TODO: fill in
"""
import tkinter as tk

from .member_home_frame import MemberHomeFrame


class PlaylistInfoFrame(MemberHomeFrame):
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
        self.song_sim_button = tk.Button(self.lower_grid)
        self.song_sim_button["text"] = "Song Similarity"
        self.song_sim_button.grid(row=0, column=1)
