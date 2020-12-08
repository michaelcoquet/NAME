"""CMPT 370 Group 5 Project: NAME (Nearly Analogous Music Engine)
    Credits: Michael Coquet
             Elizabeth Reid
             Ben Camplin
             Laurence Craig Garcia
             Sean Warren
"""
import tkinter as tk
from tkinter import Grid

from .home_page_frame import HomePageFrame


class EditGroupPlaylistFrame(HomePageFrame):
    """ TODO: fill in

    Args:
        tk ([type]): TODO: fill in
    """

    def grid_unmap(self):
        super().grid_unmap()

    def grid_remember(self):
        super().grid_remember()
        self.similar_songs_button.grid_remove()
        self.create_playlist_button.grid_remove()
        self.compare_songs_button.grid_remove()
        self.get_song_info_button.grid_remove()

    def init_lower_grid(self):
        super().init_lower_grid()
        self.similar_songs_button.grid_remove()

        container = tk.Frame(self.lower_grid)
        container.grid(row=0, column=2)

        self.similar_songs_group_button = tk.Button(
            container,
            text="Find Similar Songs",
            command=self.similar_songs_command)
        self.similar_songs_group_button.grid(row=0, column=0, padx=10)

        self.done_button = tk.Button(container, text="Done", command=self.done_command)
        self.done_button.grid(row=0, column=1, padx=10)

    def init_middle_grid(self):
        super().init_middle_grid()

    def done_command(self):
        """command for the done button
        """
        self.parent.switch_to_previous_frame()