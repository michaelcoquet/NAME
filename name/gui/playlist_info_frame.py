"""CMPT 370 Group 5 Project: NAME (Nearly Analogous Music Engine)
    Credits: Michael Coquet
             Elizabeth Reid
             Ben Camplin
             Laurence Craig Garcia
             Sean Warren
"""
import tkinter as tk

from .member_home_frame import MemberHomeFrame


class PlaylistInfoFrame(MemberHomeFrame):
    """ TODO: fill in

    Args:
        tk ([type]): TODO: fill in
    """

    def grid_unmap(self):
        super().grid_unmap()
        self.song_sim_button.grid_remove()

    def init_lower_grid(self):
        super().init_lower_grid()
        self.song_sim_button = tk.Button(
            self.lower_grid,
            text="Song Similarity",
            command=self.song_sim_command)
        self.song_sim_button.grid(row=0, column=1)

        self.get_song_info_button["command"] = self.get_song_info_command

    def song_sim_command(self):
        """command for the song similarity button
        """

        # TODO: backen link required to sim searh based on the current playlist
        self.open_search_progress()

    def get_song_info_command(self):
        """command for the get song info button
        """
        self.switch_frame("Song Info")
