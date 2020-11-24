"""The home frame for the app can be either member or guest for this frame
"""
import tkinter as tk
from tkinter import ttk
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
        self.frame_id = self.parent.get_frame_id("Home Page")

    def grid_forget(self):
        super().grid_forget()
        self.remove_all_button.grid_forget()
        self.similar_songs_button.grid_forget()
        self.song_treeview.grid_forget()
        self.create_playlist_button.grid_forget()
        self.compare_songs_button.grid_forget()
        self.get_song_info_button.grid_forget()
        self.filters_dropdown.grid_forget()
        self.song_search_entry.grid_forget()
        self.song_search_button.grid_forget()

    def grid_remember(self):
        super().grid_remember()
        self.song_search_entry.delete(0, "end")
        self.song_search_entry.insert(0, "Find a Song")

    def init_lower_grid(self):
        super().init_lower_grid()
        self.remove_all_button = tk.Button(
            self.lower_grid,
            text="Remove All")
        self.remove_all_button.grid(row=0, column=0)

        self.similar_songs_button = tk.Button(
            self.lower_grid,
            text="Find Similar Songs",
            command=self.similar_songs_command)
        self.similar_songs_button.grid(row=0, column=2)

    def init_middle_grid(self):
        super().init_middle_grid()
        self.song_treeview = ttk.Treeview(self.middle_grid)
        self.song_treeview["columns"] = ("Title", "Album", "Artist(s)")

        # set up widths of columns
        self.song_treeview.column("#0", width=1, minwidth=1, stretch=tk.NO)
        self.song_treeview.column("Title", width=300, minwidth=300, stretch=tk.NO)
        self.song_treeview.column("Album", width=150, minwidth=150, stretch=tk.NO)
        self.song_treeview.column("Artist(s)", width=150, minwidth=150, stretch=tk.NO)

        #set up headings for the columns
        self.song_treeview.heading("Title", text="Title", anchor="w")
        self.song_treeview.heading("Album", text="Album", anchor="w")
        self.song_treeview.heading("Artist(s)", text="Artist(s)", anchor="w")
        self.song_treeview.grid(row=0, column=0, sticky="nsew")

    def init_upper_grid(self):
        super().init_upper_grid()
        self.create_playlist_button = tk.Button(
            self.upper_grid,
            text="Create Playlist",
            state=tk.DISABLED,
            command=self.create_playlist_command)
        self.create_playlist_button.grid(row=1, column=0)

        self.compare_songs_button = tk.Button(
            self.upper_grid,
            command=self.compare_songs_command,
            text="Compare Songs")
        self.compare_songs_button.grid(row=1, column=1)

        self.get_song_info_button = tk.Button(
            self.upper_grid,
            text="Get Song Info",
            command=self.song_info_command)
        self.get_song_info_button.grid(row=1, column=2)

        self.filters_dropdown = tk.Menubutton(self.upper_grid, text="Filters",
                                   indicatoron=True, borderwidth=1, relief="raised")
        menu = tk.Menu(self.filters_dropdown, tearoff=False)
        self.filters_dropdown.configure(menu=menu)
        self.filters_dropdown.grid(row=2, column=0)

        self.selected_filters = {}
        self.choices = (
                "duration_ms",
                "key",
                "tempo",
                "danceability",
                "energy",
                "loudness",
                "mode",
                "speechiness",
                "acousticness",
                "instrumentalness",
                "liveness",
                "valence",
                "time_signature"
                )
        for choice in self.choices:
            self.selected_filters[choice] = tk.IntVar(value=0)
            menu.add_checkbutton(label=choice, variable=self.selected_filters[choice],
                                 onvalue=1, offvalue=0,
                                 command=self.filter_command)

        self.song_search_entry = tk.Entry(
            self.upper_grid,
            text="Song Title")
        self.song_search_entry.grid(row=2, column=1)

        # TODO: connect with backend song search function
        self.song_search_button = tk.Button(
            self.upper_grid,
            command=self.song_search_command,
            text="Search")
        self.song_search_button.grid(row=2, column=2)

    def filter_command(self):
        """ Filters available for the user to search with
            TODO: link the users choice of filter with the search function for now just return
                  anything
        """
        self.query_object.update_filter_list(self.selected_filters)

    def compare_songs_command(self):
        """ command when compare songs btn is pushed
        """
        self.switch_frame("Compare Songs")

    def song_info_command(self):
        """ command for get song info button
        """
        self.switch_frame("Song Info Search")

    def song_search_command(self):
        """command for the song search button
        """
        # run the single song search function with will connect with the back end
        self.start_single_search(self.song_search_entry.get(), self.selected_filters)

    def create_playlist_command(self):
        """command for the create playlist button, just brings us back to the home page
        """
        self.switch_frame("Home Page")

    def similar_songs_command(self):
        """command for the find similar songs button
        """
        self.open_search_progress()
