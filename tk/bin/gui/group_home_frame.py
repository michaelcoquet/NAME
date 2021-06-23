"""CMPT 370 Group 5 Project: NAME (Nearly Analogous Music Engine)
    Credits: Michael Coquet
             Elizabeth Reid
             Ben Camplin
             Laurence Craig Garcia
             Sean Warren
"""
import tkinter as tk
from tkinter import StringVar
from tkinter import ttk

from bin.backend_classes.persistent_storage import PersistentStorage
from .home_page_frame import HomePageFrame
from .name_frame import NameFrame


class GroupHomeFrame(NameFrame):
    """ The main group home page frame that other frames inherit from
        NameFrame

    Args:
        tk (Frame): Inherits the template frame
    """
    def __init__(self, parent, container, user):
        super().__init__(parent, container, user)

    def grid_unmap(self):
        super().grid_unmap()

    def grid_remember(self):
        super().grid_remember()
        self.edit_playlist_button.grid()
        self.save_playlist_button.grid()
        self.playlist_dropdown.grid()
        self.new_playlist_button.grid()
        self.edit_group_button.grid()

        self.display_data(self.parent.song_object_list)

        ps = PersistentStorage(self.user.spotify_id)
        if self.user.active_group != None:
            playlists = ps.get_group_playlists(self.user.active_group.group_id)
            self.refresh_playlist_menu(playlists)

    def display_data(self, song_list):
        """display the given song list in the latest playlist treeview

        Args:
            song_list (list): list of songs that will appear in the
                              treeview
        """
        # clear the treeview first to avoid ghosting
        self.plist_song_treeview.delete(*self.plist_song_treeview.get_children())
        artists_string_list = []
        for song in song_list:
            for artist in song.song_artist:
                artists_string_list.append(artist.name)
            artists_string = ", ".join(artists_string_list)

            artists_string_list.clear()

            self.plist_song_treeview.insert("", "end", values=(song.song_name,
                                        song.album_details.name, artists_string))

    def init_lower_grid(self):
        super().init_lower_grid()

        self.edit_playlist_button = tk.Button(
            self.lower_grid,
            text="Edit Playlist",
            command=self.edit_playlist_command
        )
        self.edit_playlist_button.grid(row=0, column=0, sticky="e")

        self.save_playlist_button = tk.Button(
            self.lower_grid,
            text="Save to group",
            command=self.save_playlist_command
        )
        self.save_playlist_button.grid(row=0, column=1, sticky="w")

    def init_middle_grid(self):
        super().init_middle_grid()

        self.plist_song_treeview = ttk.Treeview(self.middle_grid)
        self.plist_song_treeview["columns"] = ("Title", "Album", "Artist")

        # set up widths of columns
        self.plist_song_treeview.column("#0", width=1, minwidth=1, stretch="no")
        self.plist_song_treeview.column("Title", width=300, minwidth=300, stretch="yes")
        self.plist_song_treeview.column("Album", width=150, minwidth=150, stretch="yes")
        self.plist_song_treeview.column("Artist", width=150, minwidth=150, stretch="yes")

        #set up headings for the columns
        self.plist_song_treeview.heading("Title", text="Title", anchor="w")
        self.plist_song_treeview.heading("Album", text="Album", anchor="w")
        self.plist_song_treeview.heading("Artist", text="Artist(s)", anchor="w")
        self.plist_song_treeview.grid(row=0, column=0, sticky="nsew")

        container_1 = tk.Frame(self.middle_grid)
        container_1.grid(row=0, column=2, sticky="n")

        self.edit_group_button = tk.Button(
            container_1,
            text="Edit\nGroup",
            command=self.edit_group_command
        )
        self.edit_group_button.grid(row=1, column=0)

    def refresh_playlist_menu(self, playlists):
        """ a function which refreshes the playlist menu

        Args:
            playlists (Playlist[]): refreshes the menuoptions with a
            the new playlist list
        """
        menu = self.playlist_dropdown["menu"]
        menu.delete(0, "end")
        for playlist in playlists:
            name = playlist.playlist_name
            menu.add_command(
                label=name,
                command=lambda value=name: self.intermediate_playlist_select_command(value)
            )

        # menu.add_command(
        #     label="Working Playlist",
        #     command=lambda value=name:
        #         self.intermediate_playlist_select_command("Working Playlist")
        # )

        self.display_data(self.parent.song_object_list)
        self.user.active_group.playlists = playlists

    def intermediate_playlist_select_command(self, item):
        self.playlist_dropdown_command(item)
        self.playlist_select.set(item)

    def init_upper_grid(self):
        super().init_upper_grid()

        container_0 = tk.Frame(self.upper_grid)
        container_0.grid(row=1, column=1)

        self.l_group_name = tk.Label(container_0)
        self.l_group_name.grid(row=0, column=1)
        self.l_group_name.configure(font=("Helvetica BOLD", 18))

        self.l_playlist_select = tk.Label(container_0, text="Playlist Select:")
        self.l_playlist_select.grid(row=1, column=0)

        self.playlist_select = StringVar(container_0)
        self.playlist_select.set("Working Playlist") # default value
        self.playlist_dropdown = tk.OptionMenu(
            container_0,
            self.playlist_select,
            "Working Playlist",
            command=self.playlist_dropdown_command)
        self.playlist_dropdown.grid(row=1, column=1)

        self.new_playlist_button = tk.Button(
            container_0,
            text="New Playlist",
            command=self.new_playlist_command
        )
        self.new_playlist_button.grid(row=1, column=2)

    def display_group(self, group):
        self.user.active_group = group
        self.l_group_name["text"] = group.group_name

    def edit_playlist_command(self):
        """ command for the edit playlist button
        """
        self.switch_frame("Edit Group Playlist")

    def edit_group_command(self):
        """ comamnd for the edit group button
        """
        self.switch_frame("Edit Group")
        id = self.parent.get_frame_id("Edit Group")
        self.parent.frames[id].display_group(self.user.active_group)

    def group_song_stats_command(self):
        """ command for the get group song stats button
        """
        self.switch_frame("Group Stats")

    def new_playlist_command(self):
        """ command for the new playlist button command
        """
        self.parent.song_object_list.clear()
        self.display_data(self.parent.song_object_list)
        self.playlist_select.set("Working Playlist")

    def playlist_dropdown_command(self, item):
        """ command for the playlist dropdown
        """
        # check which playlist was selected and load it into the treeview
        if item == "Working Playlist":
            self.display_data(self.parent.song_object_list)
        else:
            for playlist in self.user.active_group.playlists:
                if playlist.playlist_name == item:
                    # found the right playlist diplay the songs
                    self.display_data(playlist.songs)

    def save_playlist_command(self):
        """ command for the save playlist button
        """
        self.switch_frame("Save Playlist")
