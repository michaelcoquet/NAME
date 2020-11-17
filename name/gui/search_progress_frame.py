""" Search Progress frame corresponding to the storyboards page 1
"""
import time
import tkinter as tk
from tkinter import ttk

from .name_frame import NameFrame


class SearchProgressFrame(NameFrame):
    """ TODO: fill in

    Args:
        tk ([type]): TODO: fill in
    """
    def __init__(self, parent, container):
        super().__init__(parent, container)
        self.parent = parent
        self.container = container
        self.max_songs = self.container.max_songs
        self.win = None
        self.l_songs_found = None
        self.progress = None
        self.init_progress()

    def init_progress(self):
        """open a new window that updates the user on the progress of similarity playlist
           creation
        """
        l_1 = tk.Label(self.container, text="Finding Similar Songs!")
        l_1.grid(row=1, column=0)

        self.l_songs_found = tk.Label(self.container, text="Songs found...   0/" \
                                            + str(self.max_songs))
        self.l_songs_found.grid(row=2, column=0)

        self.progress = ttk.Progressbar(self.container, orient=tk.HORIZONTAL, length=200,
            mode="determinate")

        self.progress.grid(row=3, column=0, pady=10)

        cancel_btn = tk.Button(self.container, text="Cancel")
        cancel_btn.grid(row=4, column=0)

        self.search_update()

    def search_update(self):
        """ TODO: link this with the search function in a way that it can be updated likely will
                  require multithreading to avoid the app hanging during search, possibly fork()

                  for now just do a little simulation, notice the hang with time.sleep
        """
        count = 0
        self.progress.update()
        self.progress["maximum"] = 100
        time.sleep(1)

        self.progress['value'] = 20
        count = count + 1
        self.l_songs_found["text"] = "Songs found...   " + str(count) + "/" \
                                        + str(self.max_songs)
        self.progress.update()
        time.sleep(1)

        self.progress['value'] = 40
        count = count + 1
        self.l_songs_found["text"] = "Songs found...   " + str(count) + "/" \
                                        + str(self.max_songs)
        self.progress.update()
        time.sleep(1)

        self.progress['value'] = 50
        count = count + 1
        self.l_songs_found["text"] = "Songs found...   " + str(count) + "/" \
                                        + str(self.max_songs)
        self.progress.update()
        time.sleep(1)

        self.progress['value'] = 60
        count = count + 1
        self.l_songs_found["text"] = "Songs found...   " + str(count) + "/" \
                                        + str(self.max_songs)
        self.progress.update()
        time.sleep(1)

        self.progress['value'] = 80
        count = count + 1
        self.l_songs_found["text"] = "Songs found...   " + str(count) + "/" \
                                        + str(self.max_songs)
        self.progress.update()
        time.sleep(1)

        self.progress['value'] = 100
        count = count + 1
        self.l_songs_found["text"] = "Songs found...   " + str(count) + "/" \
                                        + str(self.max_songs)
        self.progress.update()
        time.sleep(1)
