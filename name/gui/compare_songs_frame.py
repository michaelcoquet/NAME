""" Compare songs frame corresponding to the storyboards page 2
"""
import tkinter as tk

from .home_page_frame import HomePageFrame

class CompareSongsFrame(HomePageFrame):
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
        self.get_stats_button.grid_forget()

    def init_upper_grid(self):
        super().init_upper_grid()
        self.compare_songs_button["state"] = tk.DISABLED
        self.create_playlist_button["state"] = tk.NORMAL

    def init_lower_grid(self):
        super().init_lower_grid()
        self.similar_songs_button.grid_forget()

        self.get_stats_button = tk.Button(self.lower_grid, command=self.song_stats_cmd)
        self.get_stats_button["text"] = "Get Stats"
        self.get_stats_button.grid(row=0, column=2)

    def song_stats_cmd(self):
        """ command for song stats btn
        """
        self.switch_frame("Song Stats")
        # TODO: BACKEND - Return similarities of the two or more selected songs

        # TODO: GUI - Update the srcolledText widget in the song stats frame with the
        #             returned data
