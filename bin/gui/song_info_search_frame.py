"""CMPT 370 Group 5 Project: NAME (Nearly Analogous Music Engine)
    Credits: Michael Coquet
             Elizabeth Reid
             Ben Camplin
             Laurence Craig Garcia
             Sean Warren
"""
import tkinter as tk

from .home_page_frame import HomePageFrame


class SongInfoSearchFrame(HomePageFrame):
    """ This will search for an individual song no lists of songs then
        pass that to the next frame to be displayed

    Args:
        tk (Frame): Inherits the main home page frame
    """

    def grid_remember(self):
        super().grid_remember()
        self.remove_all_button.grid_remove()
        self.remove_button.grid_remove()
        self.similar_songs_button.grid_remove()
        self.song_treeview.grid_remove()
        self.filters_dropdown.grid_remove()

    def init_upper_grid(self):
        """ inits upper grid
        """
        super().init_upper_grid()
        self.get_song_info_button["state"] = tk.DISABLED
        self.create_playlist_button["state"] = tk.NORMAL

        self.song_search_button["command"] = self.song_search_command

        self.song_search_entry.delete(0,25)
        self.song_search_entry.insert(0, "Song title")
        self.filters_dropdown.grid_remove()

    def init_middle_grid(self):
        """ inits middle grid
        """
        super().init_middle_grid()
        self.song_treeview.grid_remove()

    def init_lower_grid(self):
        """ inits lower grid
        """
        super().init_lower_grid()
        self.remove_all_button.grid_remove()
        self.remove_button.grid_remove()
        self.similar_songs_button.grid_remove()

    def song_search_command(self):
        """ command for song search button
        """
        # Do a search for the info (artist, album, year, etc.) for the song
        #            given in the text song_search_entry widget

        self.start_single_search(self.song_search_entry.get())

    def song_select_dropdown_command(self, item):
        """ override inherited function
        """
        super().song_select_dropdown_command(item)

        self.switch_frame("Song Info")
        f = self.parent.get_frame_id("Song Info")

        # pass the data to the scrolledText widget on the next screen
        s = self.parent.song_object_list[len(self.parent.song_object_list) - 1]
        self.parent.frames[f].display_details(s)

        # delete last item in the song_object_list so it doesnt carry over to
        #  other pages
        del self.parent.song_object_list[-1]

