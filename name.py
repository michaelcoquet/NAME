"""CMPT 370 Group 5 Project: NAME
    Summary: TODO: fill in summary of app
"""
import tkinter as tk
from tkinter import StringVar

class Name(tk.Frame):
    """ Could possibly be a splash screen but for now this is the home page screen

    Args:
        tk (Frame): main home page screen (no spotify account linked)
    """

    # pylint: disable=too-many-instance-attributes
    # theres going to be lots of instance attributes for this class

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        """create the home page widgets
        """
        self.grid(padx="10", pady="10",sticky="NEWS")

        self.link_spotify = tk.Button(self)
        self.link_spotify["text"] = "Login"
        self.link_spotify.grid(padx="4",row=0, column=0, sticky="WE")

        self.app_title = tk.Label(self)
        self.app_title["text"] = "N.A.M.E"
        self.app_title.grid(row=0, column=1, sticky="WE")

        self.create_playlist = tk.Button(self)
        self.create_playlist["text"] = "Create Playlist"
        self.create_playlist.grid(row=1, column=0, sticky="WE")

        self.compare_songs = tk.Button(self)
        self.compare_songs["text"] = "Compare Songs"
        self.compare_songs.grid(row=1, column=1, sticky="WE")

        self.get_song_info = tk.Button(self)
        self.get_song_info["text"] = "Get Song Info"
        self.get_song_info.grid(row=1, column=2, sticky="WE")

        self.song_search = tk.Entry(self)
        self.song_search.insert(0, "Find a Song")
        self.song_search.grid(row=2, column=1, sticky="WE")

        self.song_search_button = tk.Button(self)
        self.song_search_button["text"] = "Search"
        self.song_search_button.grid(row=3, column=2, sticky="WE")

        variable = StringVar(self)
        variable.set("Filters") # default value
        self.filters_dropdown = tk.OptionMenu(self, variable, "one", "two", "three")
        self.filters_dropdown.grid(row=3, column=0, sticky="WE")

        self.song_listbox = tk.Listbox(self)
        self.song_listbox.grid(row=4, column=1, sticky="WE")

        self.remove_all = tk.Button(self)
        self.remove_all["text"] = "Remove all"
        self.remove_all.grid(row=9, column=0, sticky="WE")

        self.create_similarity_playlist = tk.Button(self)
        self.create_similarity_playlist["text"] = "Create Similarity Playlist"
        self.create_similarity_playlist.grid(row=9, column=2, sticky="WE")


root = tk.Tk()
app = Name(master=root)
app.mainloop()
