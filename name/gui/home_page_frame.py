"""CMPT 370 Group 5 Project: NAME (Nearly Analogous Music Engine)
    Credits: Michael Coquet
             Elizabeth Reid
             Ben Camplin
             Laurence Craig Garcia
             Sean Warren
"""
import tkinter as tk
from tkinter import ttk
from tkinter import StringVar
from time import sleep
import threading

from .name_frame import NameFrame
from name.backend_classes.checking_song_similarity import CheckingSongSimilarity


class HomePageFrame(NameFrame):
    """ Could possibly be a splash screen but for now this is the home page screen

    Args:
        tk (Frame): parent frame (root in this case)
    """

    # pylint: disable=too-many-instance-attributes
    # theres going to be lots of instance attributes for this class

    def __init__(self, parent, container, user):
        super().__init__(parent, container, user)
        self.frame_id = self.parent.get_frame_id("Home Page")

        self.parent.song_object_list = []

        self.formatted_filters = []

    def grid_unmap(self):
        super().grid_unmap()
        self.remove_all_button.grid_remove()
        self.remove_button.grid_remove()
        self.similar_songs_button.grid_remove()
        self.song_treeview.grid_remove()
        self.create_playlist_button.grid_remove()
        self.compare_songs_button.grid_remove()
        self.get_song_info_button.grid_remove()
        self.filters_dropdown.grid_remove()
        self.song_search_entry.grid_remove()
        self.song_search_button.grid_remove()

    def grid_remember(self):
        super().grid_remember()
        self.remove_all_button.grid()
        self.remove_button.grid()
        self.similar_songs_button.grid()
        self.song_treeview.grid()
        self.create_playlist_button.grid()
        self.compare_songs_button.grid()
        self.get_song_info_button.grid()
        self.filters_dropdown.grid()
        self.song_search_entry.grid()
        self.song_search_button.grid()

        self.display_data(self.parent.song_object_list)

    def grid_init(self):
        super().grid_init()
        self.song_search_entry.delete(0, "end")
        self.song_search_entry.insert(0, "Find a Song")
        self.display_data(self.parent.song_object_list)

    def init_lower_grid(self):
        super().init_lower_grid()
        placeholder_frame = tk.Frame(self.lower_grid)
        placeholder_frame.grid(row=0, column=0)
        self.remove_all_button = tk.Button(
            placeholder_frame,
            text="Remove All",
            command=self.remove_all_command)
        self.remove_all_button.grid(row=0, column=0)

        self.remove_button = tk.Button(
            placeholder_frame,
            text="Remove",
            command=self.remove_command)
        self.remove_button.grid(row=0, column=1)

        self.similar_songs_button = tk.Button(
            self.lower_grid,
            text="Find Similar Songs",
            command=self.similar_songs_command)
        self.similar_songs_button.grid(row=0, column=2)

    def init_middle_grid(self):
        super().init_middle_grid()
        self.song_treeview = ttk.Treeview(self.middle_grid)
        self.song_treeview["columns"] = ("Title", "Album", "Artist")

        # set up widths of columns
        self.song_treeview.column("#0", width=1, minwidth=1, stretch="no")
        self.song_treeview.column(
            "Title",
            width=300,
            minwidth=300,
            stretch="yes"
        )
        self.song_treeview.column(
            "Album",
            width=150,
            minwidth=150,
            stretch="yes"
        )
        self.song_treeview.column(
            "Artist",
            width=150,
            minwidth=150,
            stretch="yes"
        )

        # set up headings for the columns
        self.song_treeview.heading("Title", text="Title", anchor="w")
        self.song_treeview.heading("Album", text="Album", anchor="w")
        self.song_treeview.heading("Artist", text="Artist(s)", anchor="w")
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

        self.filters_dropdown = tk.Menubutton(
            self.upper_grid,
            text="Filters",
            indicatoron=True,
            borderwidth=1,
            relief="raised"
        )
        menu = tk.Menu(self.filters_dropdown, tearoff=False)
        self.filters_dropdown.configure(menu=menu)
        self.filters_dropdown.grid(row=2, column=0)

        self.selected_filters = {}
        self.choices = [
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
                ]
        for choice in self.choices:
            self.selected_filters[choice] = tk.IntVar(value=0)
            menu.add_checkbutton(
                label=choice,
                variable=self.selected_filters[choice],
                onvalue=1, offvalue=0,
                command=self.filter_command
            )

        self.song_search_entry = tk.Entry(
            self.upper_grid,
            text="Song Title")
        self.song_search_entry.grid(row=2, column=1)

        self.song_search_button = tk.Button(
            self.upper_grid,
            command=self.song_search_command,
            text="Search")
        self.song_search_button.grid(row=2, column=2)

        # bind the focus events to the given functions to allow automatically
        # selectall text on click
        self.song_search_entry.bind(
            "<FocusIn>",
            self.song_search_entry_callback
        )

        # also bind the return key to the song_search_command
        self.parent.bind("<Return>", self.song_search_command_bind)

    def song_search_entry_callback(self, event):
        self.song_search_entry.delete(0, tk.END)

    def song_search_command_bind(self, event):
        self.song_search_command()

    def display_data(self, song_list):
        """display the given song list in the latest playlist treeview

        Args:
            song_list (list): list of songs that will appear in the treeview
        """
        # clear the treeview first to avoid ghosting
        self.song_treeview.delete(*self.song_treeview.get_children())
        artists_string_list = []
        for song in song_list:
            for artist in song.song_artist:
                artists_string_list.append(artist.name)
            artists_string = ", ".join(artists_string_list)

            artists_string_list.clear()

            self.song_treeview.insert(
                "",
                "end",
                values=(
                    song.song_name,
                    song.album_details.name,
                    artists_string
                )
            )

    def filter_command(self):
        """ Filters available for the user to search with
            link the users choice of filter with the search function
        """
        self.formatted_filters = self.convert_filters_list(self.selected_filters)
        self.query_object.update_filter_list(self.formatted_filters)

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
        # run the single song search function with will connect with the
        # back end
        self.start_single_search(self.song_search_entry.get())

    def create_playlist_command(self):
        """command for the create playlist button, just brings us back to the
           home page
        """
        self.switch_frame("Home Page")

    def similar_songs_command(self):
        # if no songs have been entered yet, display the error popup
        if len(self.parent.song_object_list) < 1:
            message = "You must enter at least one song!"
            self.enter_more_songs_popup(message)
        else:
            get_similar_songs = threading.Thread(
                target=self.threaded_similar_songs,
                daemon=True
            )
            get_similar_songs.start()
            self.loading_screen()

    def loading_screen(self):
        self.grab_set()
        popup = tk.Toplevel(self)
        popup.title("Loading...")

        message = """Finding similar songs! This may take several minutes. \
Feel free to close this
        window and try out some of the other features while you wait."""

        label = tk.Label(popup, text=message)
        label.grid(row=0, column=0)

        button = ttk.Button(popup, text="Close", command=popup.destroy)
        button.grid(row=1, column=0)
        self.grab_release()

    def threaded_similar_songs(self):
        """command for the find similar songs button
        """
        # disable the button while this is running
        self.similar_songs_button.configure(state="disabled")
        # get the current working list of songs to be searched and pass it to
        # the backend
        self.formatted_filters = self.convert_filters_list(self.selected_filters)
        search_object = CheckingSongSimilarity(self.formatted_filters)

        results = search_object.random_search(self.parent.song_object_list)

        # clear the treeview and working playlist (song_object_list)
        self.song_treeview.delete(*self.song_treeview.get_children())
        self.parent.song_object_list.clear()
        self.parent.song_object_list = results
        # switch to search results frame, and give it the results to be
        # displayed
        self.parent.switch_to_previous_frame()

        # enable the button again
        self.similar_songs_button.configure(state="normal")

    def enter_more_songs_popup(self, text):
        """ In the case that not enough songs are entered
        for the task, display this popup
        text: the specific message to be displayed in the popup
        """
        self.grab_set()
        popup = tk.Toplevel(self)
        popup.title("Not enough songs")

        label = tk.Label(popup, text=text)
        label.grid(row=0, column=0)

        button = ttk.Button(popup, text="Okay", command=popup.destroy)
        button.grid(row=1, column=0)
        self.grab_release()

    def convert_filters_list(self, tk_filters):
        """ convert the original dict of filters into something the backend
            can use

        Args:
            tk_filters (dict): the dictionary of selected filters

        return:
            formated_filters (list): list of the string names of the selected
            filters
        """
        formated_filters = []

        found = 0
        for item in self.choices:
            if self.selected_filters[item].get() == 1:
                formated_filters.append(item)
                found = 1

        if found == 0:
            return self.choices
        else:
            return formated_filters

    def song_select_dropdown_command(self, item):
        """ overrides parent song select dropdown command
        """
        # make sure the user has actually made a selection
        if self.song_selection.get() != self.song_selection_default:
            # get the item that is currently selected in the OptionMenu dropdow
            item = self.song_selection.get()
        artists_string_list = []

        # search the original list of song objects returned from the API for
        # the item
        for song in self.api_search_results:
            # build string for comparison to find object probably a better way
            # to do this
            for artist in song.song_artist:
                artists_string_list.append(artist.name)
            artists_string = ", ".join(artists_string_list)

            artists_string_list.clear()

            comp_str = song.song_name + "  -  " + artists_string

            if item == comp_str:
                # add this song to the list of songs
                self.parent.song_object_list.append(song)
                # this is the correct item add it to the treeview
                self.song_treeview.insert(
                    "",
                    "end",
                    values=(
                        song.song_name,
                        song.album_details.name,
                        artists_string
                    )
                )
                break

        # close the popup window after the user makes a selection
        self.close_single_search_window()

    def remove_command(self):
        """ command for the remove song button, can potentially have multiple
            songs selected
        """
        selected_items = self.song_treeview.selection()
        for item in selected_items:
            # must now search through list of songs in the working list for the
            # selected items and remove them from the list
            for song in self.parent.song_object_list:
                # found the song in the song object list, delete it
                if song.song_name == self.song_treeview.item(item)["values"][0]:
                    self.parent.song_object_list.remove(song)

            # delete the item from the treeview
            self.song_treeview.delete(item)

    def remove_all_command(self):
        """comamnd for the rmeove all button
        """
        for item in self.song_treeview.get_children():
            self.song_treeview.delete(item)

        self.parent.song_object_list.clear()
