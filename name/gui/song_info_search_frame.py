""" TODO: fill in
"""
import tkinter as tk

from .home_page_frame import HomePageFrame


class SongInfoSearchFrame(HomePageFrame):
    """ TODO: fill in

    Args:
        tk ([type]): TODO: fill in
    """
    def __init__(self, parent, container):
        super().__init__(parent, container)
        self.container = container
        self.parent = parent

    def init_upper_grid(self):
        """TODO: fill in
        """
        super().init_upper_grid()
        self.get_song_info_button["state"] = tk.DISABLED
        self.create_playlist_button["state"] = tk.NORMAL

        self.song_search_button["command"] = self.song_search_command

    def init_middle_grid(self):
        """TODO: fill in
        """
        super().init_middle_grid()
        self.song_listbox.grid_forget()

    def init_lower_grid(self):
        """TODO: fill in
        """
        super().init_lower_grid()
        self.remove_all_button.grid_forget()
        self.similar_songs_button.grid_forget()

    def song_search_command(self):
        """ command for song search button
        """
        self.switch_frame("Song Info")