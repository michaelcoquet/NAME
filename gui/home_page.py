"""The home screen for the app
"""
import time
import tkinter as tk
from tkinter import ttk
from tkinter import StringVar
from tkinter import Grid


class HomePage(tk.Frame):
    """ Could possibly be a splash screen but for now this is the home page screen

    Args:
        tk (Frame): main home page screen (no spotify account linked)
    """
    max_songs = 6

    # pylint: disable=too-many-instance-attributes
    # theres going to be lots of instance attributes for this class

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.win = None
        self.home_frame = None
        self.progress = None
        self.l_songs_found = None
        self.create_widgets()

    def create_widgets(self):
        """create the home page widgets
        """

        #make home frame
        self.home_frame = tk.Frame(self.master)
        self.home_frame.grid(row=0, column=0, sticky="nsew")

        upper_menu = tk.Frame(self.home_frame)
        upper_menu.grid(row=0, column=0, sticky="ew")
        lower_menu = tk.Frame(self.home_frame)
        lower_menu.grid(row=2, column=0, sticky="ew")

        #set up grid
        Grid.columnconfigure(self.home_frame, 0, weight=1)
        Grid.rowconfigure(self.home_frame, 1, weight=1)

        self.grid(padx="10", pady="10")

        self.link_spotify = tk.Button(upper_menu)
        self.link_spotify["text"] = "Login"
        self.link_spotify.grid(row=0, column=0)

        self.app_title = tk.Label(upper_menu)
        self.app_title["text"] = "N.A.M.E"
        self.app_title.grid(row=0, column=1)

        self.create_playlist = tk.Button(upper_menu, state=tk.DISABLED)
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
        self.song_search.insert(0, "Song title")
        self.song_search.grid(row=2, column=1)

        self.song_search_button = tk.Button(upper_menu)
        self.song_search_button["text"] = "Search"
        self.song_search_button.grid(row=2, column=2)

        self.song_listbox = tk.Listbox(self.home_frame)
        self.song_listbox.grid(row=1, column=0, sticky="nsew")

        self.remove_all = tk.Button(lower_menu)
        self.remove_all["text"] = "Remove all"
        self.remove_all.pack(side=tk.LEFT)

        self.create_similarity_playlist = tk.Button(lower_menu,
            text="Find Similar Songs", command=self.open_sim_progress)
        self.create_similarity_playlist.pack(side=tk.RIGHT)

    # function to open a new window
    # on a button click
    def open_sim_progress(self):
        """open a new window that updates the user on the progress of similarity playlist
           creation
        """
        self.grab_set()
        # Toplevel object which will
        # be treated as a new window
        self.win = tk.Toplevel(self)
        self.win.protocol("WM_DELETE_WINDOW", self.close_window)
        # sets the title of the
        # Toplevel widget
        self.win.title("Searching")

        l_1 = tk.Label(self.win, text="Finding Similar Songs!")
        l_1.pack(side=tk.TOP)

        self.l_songs_found = tk.Label(self.win, text="Songs found...   0/" \
                                            + str(self.max_songs))
        self.l_songs_found.pack(side=tk.TOP)

        self.progress = ttk.Progressbar(self.win, orient=tk.HORIZONTAL, length=200,
            mode="determinate")

        self.progress.pack(pady=10)

        cancel_btn = tk.Button(self.win, text="Cancel", command=self.close_window)
        cancel_btn.pack(side=tk.BOTTOM)

        self.search_update()

    def search_update(self):
        """TODO: connect with song similarity search
            This is where the song similarity search should be connected
            and progress bar updated
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



    def close_window(self):
        """override window closing event
        """
        self.progress.destroy()
        self.win.destroy()
        self.grab_release()
