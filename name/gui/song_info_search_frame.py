""" TODO: fill in
"""
import tkinter as tk

from .home_page_frame import HomePageFrame


class SongInfoSearchFrame(HomePageFrame):
    """ TODO: fill in

    Args:
        tk ([type]): TODO: fill in
    """
    def __init__(self, parent, container):
        super().__init__(parent, container)
        self.container = container
        self.parent = parent

    def init_upper_grid(self):
        """TODO: fill in
        """
        super().init_upper_grid()
        self.get_song_info_button["state"] = tk.DISABLED
        self.create_playlist_button["state"] = tk.NORMAL

        self.song_search_button["command"] = self.song_search_command

        self.song_search_entry.delete(0,25)
        self.song_search_entry.insert(0, "Song title")

    def init_middle_grid(self):
        """TODO: fill in
        """
        super().init_middle_grid()
        self.song_treeview.grid_forget()

    def init_lower_grid(self):
        """TODO: fill in
        """
        super().init_lower_grid()
        self.remove_all_button.grid_forget()
        self.similar_songs_button.grid_forget()

    def song_search_command(self):
        """ command for song search button
        """
        # TODO: BACKEND - Do a search for the info (artist, album, year, etc.) for the song
        #            given in the text song_search_entry widget

        # hide this button for the next frame since its not used
        self.start_single_search(self.song_search_entry.get(), self.selected_filters)
        self.switch_frame("Song Info")
        f = self.parent.get_frame_id("Song Info")
        self.parent.frames[f].ply_from_ply_button.grid_forget()

        # TODO: GUI - Update the song_info_scrolledtext in the song_info_frame

    def song_select_dropdown_function(self, item):
        """ override inherited function
        """
        # for i in self.api_search_results:
        print("HELLO")