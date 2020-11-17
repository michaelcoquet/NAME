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

    def init_upper_grid(self):
        super().init_upper_grid()
        self.compare_songs_button["state"] = tk.NORMAL

        self.song_search_entry.delete(0,25)
        self.song_search_entry.insert(0, "Two or more songs")
