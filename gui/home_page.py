"""The home screen for the app
"""
import tkinter as tk
from tkinter import StringVar
from tkinter import Grid

class HomePage(tk.Frame):
    """ Could possibly be a splash screen but for now this is the home page screen

    Args:
        tk (Frame): main home page screen (no spotify account linked)
    """

    # pylint: disable=too-many-instance-attributes
    # theres going to be lots of instance attributes for this class
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        """create the home page widgets
        """

        #make home frame
        home_frame = tk.Frame(self.master)
        home_frame.grid(row=0, column=0, sticky="nsew")

        upper_menu = tk.Frame(home_frame)
        upper_menu.grid(row=0, column=0, sticky="ew")
        lower_menu = tk.Frame(home_frame)
        lower_menu.grid(row=2, column=0, sticky="ew")

        #set up grid
        Grid.columnconfigure(home_frame, 0, weight=1)
        Grid.rowconfigure(home_frame, 1, weight=1)

        self.grid(padx="10", pady="10")

        self.link_spotify = tk.Button(upper_menu)
        self.link_spotify["text"] = "Login"
        self.link_spotify.grid(row=0, column=0)

        self.app_title = tk.Label(upper_menu)
        self.app_title["text"] = "N.A.M.E"
        self.app_title.grid(row=0, column=1)

        self.create_playlist = tk.Button(upper_menu)
        self.create_playlist["text"] = "Create Playlist"
        self.create_playlist.grid(row=1, column=0)

        self.compare_songs = tk.Button(upper_menu)
        self.compare_songs["text"] = "Compare Songs"
        self.compare_songs.grid(row=1, column=1)

        self.get_song_info = tk.Button(upper_menu)
        self.get_song_info["text"] = "Get Song Info"
        self.get_song_info.grid(row=1, column=2)

        variable = StringVar(upper_menu)
        variable.set("Filters") # default value
        self.filters_dropdown = tk.OptionMenu(upper_menu, variable, "one", "two", "three")
        self.filters_dropdown.grid(row=2, column=0)

        self.song_search = tk.Entry(upper_menu)
        self.song_search.insert(0, "Find a Song")
        self.song_search.grid(row=2, column=1)

        self.song_search_button = tk.Button(upper_menu)
        self.song_search_button["text"] = "Search"
        self.song_search_button.grid(row=2, column=2)

        self.song_listbox = tk.Listbox(home_frame)
        self.song_listbox.grid(row=1, column=0, sticky="nsew")

        self.remove_all = tk.Button(lower_menu)
        self.remove_all["text"] = "Remove all"
        self.remove_all.pack(side=tk.LEFT)

        self.create_similarity_playlist = tk.Button(lower_menu)
        self.create_similarity_playlist["text"] = "Create Similarity Playlist"
        self.create_similarity_playlist.pack(side=tk.RIGHT)
