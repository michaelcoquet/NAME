""" TODO: fill in
"""
import tkinter as tk

from .song_info_frame import SongInfoFrame


class SongStatsFrame(SongInfoFrame):
    """ TODO: fill in

    Args:
        tk ([type]): TODO: fill in
    """

    def grid_unmap(self):
        super().grid_unmap()
        self.sim_score_label.grid_remove()

    def init_upper_grid(self):
        super().init_upper_grid()
        self.song_search_entry.grid_remove()
        self.song_search_button.grid_remove()
        self.filters_dropdown.grid_remove()

        self.create_playlist_button["state"] = tk.NORMAL
        self.compare_songs_button["state"] = tk.DISABLED

        self.sim_score_label = tk.Label(self.upper_grid, text="These songs are X% similar")
        self.sim_score_label.grid(row=2, column=1)

    def init_middle_grid(self):
        super().init_middle_grid()
        self.song_lyrics_scrolledtext.grid_remove()

    def init_lower_grid(self):
        super().init_lower_grid()

        self.start_over_button["command"] = self.start_over_command
        self.start_over_button.grid(row=0, column=0)

    def start_over_command(self):
        self.switch_frame("Compare Songs")

    def display(self, tuple):
        self.sim_score_label["text"] = "These songs are " + str(tuple[0]) + "% similar"
        for song in tuple[1]:
            self.song_info_scrolledtext.insert("end", str(song) + "\n\n")
