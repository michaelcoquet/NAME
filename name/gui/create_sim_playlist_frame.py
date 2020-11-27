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

        self.filters_dropdown = tk.Menubutton(self.upper_grid, text="Filters",
                                   indicatoron=True, borderwidth=1, relief="raised")
        menu = tk.Menu(self.filters_dropdown, tearoff=False)
        self.filters_dropdown.configure(menu=menu)
        self.filters_dropdown.grid(row=2, column=0)

        self.selected_filters = {}
        self.choices = (
                "duration_ms",
                "key",
                "tempo",
                "danceability",
                "energy",
                "loudness",
                "mode",
                "speechiness",
                "acousticness",
                "instrumentalness",
                "liveness",
                "valence",
                "time_signature"
                )
        for choice in self.choices:
            self.selected_filters[choice] = tk.IntVar(value=0)
            menu.add_checkbutton(label=choice, variable=self.selected_filters[choice],
                                 onvalue=1, offvalue=0,
                                 command=self.filter_command)

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
        """command for the create similar playlist button
        """
        # TODO: BACKEND - Search for songs that are similar to the songs in this playlist
        # TODO: GUI     - Update the listbox with a list of the songs in the original playlist
        self.open_search_progress()

    def filter_command(self):
        """ filter dropdown event command
        """
        return 0
