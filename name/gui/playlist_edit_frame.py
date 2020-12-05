""" TODO: fill in
"""
import tkinter as tk

from .home_page_frame import HomePageFrame


class PlaylistEditFrame(HomePageFrame):
    """ TODO: fill in

    Args:
        tk ([type]): TODO: fill in
    """

    def grid_forget(self):
        super().grid_forget()
        # self.delete_playlist_button.grid_forget()
        self.done_button.grid_forget()


    def init_lower_grid(self):
        super().init_lower_grid()
        self.similar_songs_button.grid_forget()

        self.done_button = tk.Button(
            self.lower_grid,
            text="Done",
            command=self.done_command)
        self.done_button.grid(row=0, column=2)

    def init_upper_grid(self):
        super().init_upper_grid()
        self.create_playlist_button.grid_forget()
        self.get_song_info_button.grid_forget()
        self.compare_songs_button.grid_forget()

        # self.filters_dropdown.grid_forget()
        # self.song_search_entry.grid_forget()
        # self.song_search_button.grid_forget()

    def delete_command(self):
        """command for the delete button
        """

        # TODO: add logic to delete the selected song from the playlist being edited
        return 1

    def done_command(self):
        """command for the done button
        """
        # TODO: save changes back tot he listbox on member home frame
        self.switch_frame("Group Home")
