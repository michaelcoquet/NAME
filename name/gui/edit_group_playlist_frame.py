""" TODO: fill in
"""
import tkinter as tk
from tkinter import Grid

from .save_playlist_frame import SavePlaylistFrame


class EditGroupPlaylistFrame(SavePlaylistFrame):
    """ TODO: fill in

    Args:
        tk ([type]): TODO: fill in
    """

    def grid_unmap(self):
        super().grid_unmap()
        self.save_playlist_button.grid_remove()

    def grid_remember(self):
        super().grid_remember()

    def init_lower_grid(self):
        super().init_lower_grid()
        self.new_list_entry.grid_remove()

        self.save_playlist_button.grid_remove()

        self.save_playlist_button.grid(row=0, column=2, sticky="nsew")

    def init_middle_grid(self):
        super().init_middle_grid()

        container = tk.Frame(self.middle_grid)
        container.grid(row=0, column=2)

        l1 = tk.Label(container, text="Enter Songs")
        l1.grid(row=0, column=0, sticky="e")

        self.song_entry = tk.Entry(container, text="Song Title")
        self.song_entry.grid(row=1, column=0)

        self.add_button = tk.Button(container, text="Add", command=self.add_command)
        self.add_button.grid(row=1, column=1, sticky="e")

        Grid.rowconfigure(self.middle_grid, 0, weight=1)
        Grid.rowconfigure(self.middle_grid, 1, weight=100)

        l2 = tk.Label(self.middle_grid, text="Select Existing\nFriends Playlist")
        l2.grid(row=0, column=0, sticky="w")

        self.playlist_listbox = tk.Listbox(self.middle_grid)
        self.playlist_listbox.grid(row=1, column=0, sticky="nsw")

    def sim_playlist_command(self):
        self.open_search_progress()

    def cancel_command(self):
        self.switch_frame("Group Home")

    def add_command(self):
        """command for the add button
        """
        # TODO: BACKEND - search for the given song and return it from the api
        # TODO: GUI - add the title of the returned song to the playlist_listbox
        return 1
