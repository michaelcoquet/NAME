"""CMPT 370 Group 5 Project: NAME (Nearly Analogous Music Engine)
    Credits: Michael Coquet
             Elizabeth Reid
             Ben Camplin
             Laurence Craig Garcia
             Sean Warren
"""
import tkinter as tk

from .song_info_frame import SongInfoFrame


class SongStatsFrame(SongInfoFrame):
    """ Displays song stats, differnt from song info since this will show comparison of songs

    Args:
        tk (Frame): inherits song info frame
    """

    def grid_unmap(self):
        super().grid_unmap()
        self.sim_score_label.grid_remove()

    def grid_remember(self):
        super().grid_remember()
        self.create_playlist_button.grid_remove()
        self.compare_songs_button.grid_remove()
        self.get_song_info_button.grid_remove()
        self.remove_all_button.grid_remove()
        self.remove_button.grid_remove()
        self.similar_songs_button.grid_remove()
        self.filters_dropdown.grid_remove()
        self.song_search_entry.grid_remove()
        self.song_search_button.grid_remove()
        self.song_treeview.grid_remove()

        self.start_over_button.grid()
        self.sim_score_label.grid()
        self.song_info_scrolledtext.grid()

        self.song_info_scrolledtext.delete("1.0", "end")


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
        self.parent.switch_to_previous_frame()

    def display(self, t):
        self.sim_score_label["text"] = "These songs are " + str(t[0]) + "% similar"
        for song in t[1]:
            self.song_info_scrolledtext.insert("end", str(song) + "\n\n")
