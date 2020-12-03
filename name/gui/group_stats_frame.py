""" TODO: fill in
"""
import tkinter as tk

from .song_info_frame import SongInfoFrame


class GroupStatsFrame(SongInfoFrame):
    """ TODO: fill in

    Args:
        tk ([type]): TODO: fill in
    """

    # def grid_forget():
    #     super().grid_forget()
    def init_lower_grid(self):
        super().init_lower_grid()
        self.start_over_button.grid_forget()
        self.ply_from_ply_button.grid_forget()

    def init_middle_grid(self):
        super().init_middle_grid()
        self.song_info_scrolledtext.delete(1.0, tk.END)
        self.song_info_scrolledtext.insert(tk.INSERT,
        """\
Lots of group stats
    - sdf
    - as
    - ff
    - n
        """) # remove this when we get real results back

    def init_upper_grid(self):
        super().init_upper_grid()
        self.create_playlist_button.grid_forget()
        self.compare_songs_button.grid_forget()
        self.get_song_info_button.grid_forget()
        self.filters_dropdown.grid_forget()
        self.song_search_entry.grid_forget()
        self.song_search_button.grid_forget()

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
