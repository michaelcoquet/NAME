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

    def grid_forget(self):
        super().grid_forget()
        self.sim_score_label.grid_forget()

    def init_upper_grid(self):
        super().init_upper_grid()
        self.song_search_entry.grid_forget()
        self.song_search_button.grid_forget()
        self.filters_dropdown.grid_forget()

        self.create_playlist_button["state"] = tk.NORMAL
        self.compare_songs_button["state"] = tk.DISABLED

        self.sim_score_label = tk.Label(self.upper_grid, text="These songs are X% similar")
        self.sim_score_label.grid(row=2, column=1)

    def init_middle_grid(self):
        super().init_middle_grid()
        self.song_lyrics_scrolltext.grid_forget()

        # load song data here
        # TODO: make it look better in a table or something, fine for the demo
        for song in self.parent.song_object_list:
            self.song_info_scrolledtext.insert("end", str(song) + "\n\n")

    def init_lower_grid(self):
        super().init_lower_grid()
        self.ply_from_ply_button.grid_forget()

        self.start_over_button["command"] = self.start_over_command
        self.start_over_button.grid(row=0, column=0)

    def start_over_command(self):
        self.switch_frame("Compare Songs")

    def display_data(self, tuple):
        self.sim_score_label["text"] = "These songs are " + str(tuple[0]) + "% similar"
