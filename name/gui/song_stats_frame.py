""" TODO: fill in
"""
import tkinter as tk
from .song_info_frame import SongInfoFrame


class SongStatsFrame(SongInfoFrame):
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
        self.create_playlist_button["state"] = tk.NORMAL
        self.compare_songs_button["state"] = tk.DISABLED
        self.sim_score_label = tk.Label(self.upper_grid, text="These songs are X% similar")
        self.sim_score_label.grid(row=2, column=1)
