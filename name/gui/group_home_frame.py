""" TODO: fill in
"""
import tkinter as tk
from tkinter import StringVar

from .name_frame import NameFrame


class GroupHomeFrame(NameFrame):
    """ TODO: fill in

    Args:
        tk ([type]): TODO: fill in
    """

    group_name = "TODO: change this"

    def grid_forget(self):
        super().grid_forget()
        self.edit_playlist_button.grid_forget()
        self.save_playlist_button.grid_forget()
        self.list_1_label.grid_forget()
        self.song_listbox.grid_forget()
        self.playlist_dropdown.grid_forget()
        self.new_playlist_button.grid_forget()
        self.group_song_stats_button.grid_forget()
        self.edit_group_button.grid_forget()

    def init_lower_grid(self):
        super().init_lower_grid()

        self.edit_playlist_button = tk.Button(
            self.lower_grid,
            text="Edit",
            command=self.edit_playlist_command
        )
        self.edit_playlist_button.grid(row=0, column=0, sticky="e")

        self.save_playlist_button = tk.Button(
            self.lower_grid,
            text="Save",
            command=self.save_playlist_command
        )
        self.save_playlist_button.grid(row=0, column=1, sticky="w")

    def init_middle_grid(self):
        super().init_middle_grid()

        self.song_listbox = tk.Listbox(self.middle_grid)
        self.song_listbox.grid(row=0, column=0, sticky="nsew")

        # TODO: add the proper filters to the dropdown list
        container_0 = tk.Frame(self.middle_grid)
        container_0.grid(row=0, column=1, sticky="n")

        self.list_1_label = tk.Label(container_0)
        self.list_1_label["text"] = "Group: " + self.group_name + "\nplaylists"
        self.list_1_label.grid(row=0, column=0)

        variable = StringVar(container_0)
        variable.set("Last Created Playlist") # default value
        self.playlist_dropdown = tk.OptionMenu(
            container_0,
            variable,
            "Last Created Playlist",
            "playlist 1",
            "playlist 2",
            "playlist 3",
            command=self.playlist_dropdown_command)
        self.playlist_dropdown.grid(row=1, column=0)

        self.new_playlist_button = tk.Button(
            container_0,
            text="New Playlist",
            command=self.new_playlist_command
        )
        self.new_playlist_button.grid(row=2, column=0)

        container_1 = tk.Frame(self.middle_grid)
        container_1.grid(row=0, column=2, sticky="n")

        self.group_song_stats_button = tk.Button(
            container_1,
            text="Get Group\nSong Stats",
            command=self.group_song_stats_command)
        self.group_song_stats_button.grid(row=0, column=0)

        self.edit_group_button = tk.Button(
            container_1,
            text="Edit\nGroup",
            command=self.edit_group_command
        )
        self.edit_group_button.grid(row=1, column=0)

    def init_upper_grid(self):
        super().init_upper_grid()
        self.list_1_label = tk.Label(self.upper_grid, text="Last Created\nPlaylist")
        self.list_1_label.grid(row=1, column=1)

    def edit_playlist_command(self):
        """ command for the edit playlist button
        """
        self.switch_frame("Playlist Edit")

    def edit_group_command(self):
        """ comamnd for the edit group button
        """
        self.switch_frame("Edit Group")

    def group_song_stats_command(self):
        """ command for the get group song stats button
        """
        self.switch_frame("Group Stats")

    def new_playlist_command(self):
        """ command for the new playlist button command
        """
        self.switch_frame("Edit Group Playlist")

    def playlist_dropdown_command(self):
        """ command for the playlist dropdown
        """
        return 1

    def save_playlist_command(self):
        """ command for the save playlist button
        """
        return 1