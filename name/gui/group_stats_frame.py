"""CMPT 370 Group 5 Project: NAME (Nearly Analogous Music Engine)
    Credits: Michael Coquet
             Elizabeth Reid
             Ben Camplin
             Laurence Craig Garcia
             Sean Warren
"""
import tkinter as tk

from .song_info_frame import SongInfoFrame


class GroupStatsFrame(SongInfoFrame):
    """ TODO: fill in

    Args:
        tk ([type]): TODO: fill in
    """

    # def grid_forget():
    #     super().grid_remove()
    def init_lower_grid(self):
        super().init_lower_grid()
        self.start_over_button.grid_remove()

    def init_middle_grid(self):
        super().init_middle_grid()
        self.song_info_scrolledtext.delete(1.0, tk.END)

    def init_upper_grid(self):
        super().init_upper_grid()
        self.create_playlist_button.grid_remove()
        self.compare_songs_button.grid_remove()
        self.get_song_info_button.grid_remove()
        self.filters_dropdown.grid_remove()
        self.song_search_entry.grid_remove()
        self.song_search_button.grid_remove()

        self.playlists_button = tk.Button(
            self.upper_grid,
            text="Group Playlists",
            command=self.group_playlists_command
        )
        self.playlists_button.grid(row=1, column=0)

        self.edit_group_button = tk.Button(
            self.upper_grid,
            text="Edit Group",
            command=self.edit_group_command
        )
        self.edit_group_button.grid(row=1, column=1)

    def group_playlists_command(self):
        """command for the group playlists button
        """
        self.switch_frame("Group Home")

    def edit_group_command(self):
        """comamnd for the edit group button
        """
        self.switch_frame("Edit Group")
