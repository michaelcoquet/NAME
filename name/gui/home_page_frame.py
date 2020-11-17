"""The home frame for the app can be either member or guest for this frame
"""
import tkinter as tk
from tkinter import StringVar

from .name_frame import NameFrame


class HomePageFrame(NameFrame):
    """ Could possibly be a splash screen but for now this is the home page screen

    Args:
        tk (Frame): parent frame (root in this case)
    """
    # pylint: disable=too-many-instance-attributes
    # theres going to be lots of instance attributes for this class

    def __init__(self, parent, container):
        super().__init__(parent, container)
        self.parent = parent
        self.container = container

    def init_lower_grid(self):
        super().init_lower_grid()
        self.remove_all_button = tk.Button(self.lower_grid)
        self.remove_all_button["text"] = "Remove all"
        self.remove_all_button.grid(row=0, column=0)

        self.similar_songs_button = tk.Button(self.lower_grid)
        self.similar_songs_button["text"] = "Find Similar Songs"
        self.similar_songs_button.grid(row=0, column=2)

    def init_middle_grid(self):
        super().init_middle_grid()
        self.song_listbox = tk.Listbox(self.middle_grid)
        self.song_listbox.grid(row=0, column=0, sticky="nsew")


    def init_upper_grid(self):
        super().init_upper_grid()
        self.create_playlist_button = tk.Button(self.upper_grid)
        self.create_playlist_button["text"] = "Create Playlist"
        self.create_playlist_button["state"] = tk.DISABLED
        self.create_playlist_button.grid(row=1, column=0)

        self.compare_songs_button = tk.Button(self.upper_grid)
        self.compare_songs_button["text"] = "Compare Songs"
        self.compare_songs_button.grid(row=1, column=1)

        self.get_song_info_button = tk.Button(self.upper_grid)
        self.get_song_info_button["text"] = "Get Song Info"
        self.get_song_info_button.grid(row=1, column=2)

        # TODO: add the proper filters to the dropdown list
        variable = StringVar(self.upper_grid)
        variable.set("Filters") # default value
        self.filters_dropdown = tk.OptionMenu(self.upper_grid, variable, "one", "two", "three",
                                                    command=self.container.filter_function)
        self.filters_dropdown.grid(row=2, column=0)

        self.song_search_entry = tk.Entry(self.upper_grid)
        self.song_search_entry.insert(0, "Song title")
        self.song_search_entry.grid(row=2, column=1)

        # TODO: connect with backend song search function
        self.song_search_button = tk.Button(self.upper_grid)
        self.song_search_button["text"] = "Search"
        self.song_search_button.grid(row=2, column=2)

