""" TODO: fill in
"""
import tkinter as tk
from tkinter import ttk

from .member_home_frame import MemberHomeFrame
from name.backend_classes.spotify_api_manager import SpotifyAPIManager
from name.backend_classes.checking_song_similarity import CheckingSongSimilarity

class AllPlaylistsFrame(MemberHomeFrame):
    """ TODO: fill in

    Args:
        tk ([type]): TODO: fill in
    """
    def __init__(self, parent, container):
        super().__init__(parent, container)
        self.container = container
        self.parent = parent

        self.playlists = []

    def grid_forget(self):
        super().grid_forget()
        self.list_from_list_button.grid_forget()
        self.song_sim_button.grid_forget()

    def init_upper_grid(self):
        super().init_upper_grid()
        self.all_playlists_button["state"] = tk.DISABLED
        self.latest_playlist_button["state"] = tk.NORMAL

    def init_middle_grid(self):
        super().init_middle_grid()
        self.get_song_info_button.grid_forget()

        # we dont have a song_treeview here so we need to make a playlist treeview
        self.song_treeview.grid_forget()
        self.playlist_treeview = ttk.Treeview(self.middle_grid)
        self.playlist_treeview["columns"] = ("Name", "Size", "Owner")

        self.playlist_treeview.column("#0", width=1, minwidth=1, stretch="no")
        self.playlist_treeview.column("Name", width=150, minwidth=150, stretch="yes")
        self.playlist_treeview.column("Size", width=90, minwidth=90, stretch="yes")
        self.playlist_treeview.column("Owner", width=80, minwidth=80, stretch="yes")

        self.playlist_treeview.heading("Name", text="Name", anchor="w")
        self.playlist_treeview.heading("Size", text="Size", anchor="w")
        self.playlist_treeview.heading("Owner", text="Owner", anchor="w")
        self.playlist_treeview.grid(row=0, column=0, sticky="nsew")

        # get a list of the current users spotify playlists if theyre logged in
        if self.parent.logged_in:
            plist = self.parent.spotify_manager.get_member_playlists()
            self.display_data(plist)

    def init_lower_grid(self):
        super().init_lower_grid()
        self.edit_button.grid_forget()
        self.save_spotify_button.grid_forget()

        self.list_from_list_button = tk.Button(
            self.lower_grid,
            text="Create new playlist\n from this playlist",
            command=self.list_from_list_command)
        self.list_from_list_button.grid(row=0, column=0)

        self.song_sim_button = tk.Button(
            self.lower_grid,
            text="get playlist\n song similarity",
            command=self.song_sim_command)
        self.song_sim_button.grid(row=0, column=2)

        self.latest_playlist_button["command"] = self.latest_playlist_command

    def list_from_list_command(self):
        """comamnd for the create playlist from this playlist button
        """

        # TODO: BAKCEND - Find songs that are similar to the songs in the selected playlist
        self.switch_frame("Create Sim Playlist")

    def display_data(self, api_results):
        """ take the playlist data (list of playlist objects) in and display it in the treeview
        """
        for playlist in api_results:
            self.playlist_treeview.insert("", "end", values=(playlist.playlist_name,
                            playlist.size, playlist.playlist_owner))
            self.playlists.append(playlist)

    def song_sim_command(self):
        """command for the get playlist song similarity button
        """
        # TODO: BACKEND - Get the similarity of the songs in the selected playlist

        # get the current working list of songs to be searched and pass it to the backend
        self.formatted_filters = self.convert_filters_list(self.selected_filters)
        search_object = CheckingSongSimilarity(self.formatted_filters)

        selected_items = self.playlist_treeview.selection()

        if len(selected_items) == 1:
            selected_name = self.playlist_treeview.item(selected_items[0])["values"][0]
            for item in  self.playlists:
                if item.playlist_name == selected_name:
                    result = search_object.get_songs_similarity_score(item.songs)
                    self.switch_frame("Song Stats")
                    d = [int(result), item.songs]
                    self.parent.frames[self.parent.get_frame_id("Song Stats")].display(d)
                    # result = search_object.random_search(item.songs)
                    # # switch to search results frame, and give it the results to be displayed
                    # self.switch_frame("Search Results")
                    # self.parent.frames[self.parent.get_frame_id("Search Results")].display_data(result)

    def latest_playlist_command(self):
        """command for the latest playlist button
        """
        self.switch_frame("Member Home")
