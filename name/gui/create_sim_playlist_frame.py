""" TODO: fill in
"""
import tkinter as tk
from tkinter import StringVar

from .name_frame import NameFrame


class CreateSimPlaylistFrame(NameFrame):
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
        self.new_list_entry.grid_forget()
        self.filters_dropdown.grid_forget()
        self.listbox_label.grid_forget()
        self.songs_listbox.grid_forget()
        self.cancel_button.grid_forget()
        self.sim_playlist_button.grid_forget()

    def init_upper_grid(self):
        super().init_upper_grid()
        self.new_list_entry = tk.Entry(self.upper_grid)
        self.new_list_entry.insert(0, "New Playlist Name")
        self.new_list_entry.grid(row=1, column=0)

        # TODO: add the proper filters to the dropdown list
        variable = StringVar(self.upper_grid)
        variable.set("Filters") # default value
        self.filters_dropdown = tk.OptionMenu(
            self.upper_grid,
            variable,
            "one",
            "two",
            "three",)
        self.filters_dropdown.grid(row=2, column=0, sticky="w")

        self.listbox_label = tk.Label(
            self.upper_grid,
            text="Original Playlist Songs:")
        self.listbox_label.grid(row=3, column=0)

    def init_middle_grid(self):
        super().init_middle_grid()
        self.songs_listbox = tk.Listbox(self.middle_grid)
        self.songs_listbox.grid(row=0, column=0, sticky="nsew")

    def init_lower_grid(self):
        super().init_lower_grid()

        self.cancel_button = tk.Button(
            self.lower_grid,
            text="Cancel",
            command=self.cancel_command)
        self.cancel_button.grid(row=0, column=0)

        self.sim_playlist_button = tk.Button(
            self.lower_grid,
            text="create similarity\nplaylist",
            command=self.sim_playlist_command)
        self.sim_playlist_button.grid(row=0, column=2)

    def cancel_command(self):
        """command for the cancel button
        """
        self.switch_frame("All Playlists")

    def sim_playlist_command(self):
        """command for the create similarity playlist button
        """

        # TODO: connect to backend to save to users spotify and also to the listbox
        return 1