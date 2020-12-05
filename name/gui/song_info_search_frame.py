""" TODO: fill in
"""
import tkinter as tk

from .home_page_frame import HomePageFrame


class SongInfoSearchFrame(HomePageFrame):
    """ TODO: fill in

    Args:
        tk ([type]): TODO: fill in
    """

    def grid_remember(self):
        super().grid_remember()
        self.remove_all_button.grid_remove()
        self.remove_button.grid_remove()
        self.similar_songs_button.grid_remove()
        self.song_treeview.grid_remove()
        self.filters_dropdown.grid_remove()

    def init_upper_grid(self):
        """TODO: fill in
        """
        super().init_upper_grid()
        self.get_song_info_button["state"] = tk.DISABLED
        self.create_playlist_button["state"] = tk.NORMAL

        self.song_search_button["command"] = self.song_search_command

        self.song_search_entry.delete(0,25)
        self.song_search_entry.insert(0, "Song title")
        self.filters_dropdown.grid_remove()

    def init_middle_grid(self):
        """TODO: fill in
        """
        super().init_middle_grid()
        self.song_treeview.grid_remove()

    def init_lower_grid(self):
        """TODO: fill in
        """
        super().init_lower_grid()
        self.remove_all_button.grid_remove()
        self.remove_button.grid_remove()
        self.similar_songs_button.grid_remove()

    def song_search_command(self):
        """ command for song search button
        """
        # TODO: BACKEND - Do a search for the info (artist, album, year, etc.) for the song
        #            given in the text song_search_entry widget

        # hide this button for the next frame since its not used
        self.start_single_search(self.song_search_entry.get(), {})

        # TODO: GUI - Update the song_info_scrolledtext in the song_info_frame

    def song_select_dropdown_command(self, item):
        """ override inherited function
        """
        super().song_select_dropdown_command(item)

        self.switch_frame("Song Info")
        f = self.parent.get_frame_id("Song Info")

        # pass the data to the scrolledText widget on the next screen
        s = self.parent.song_object_list[len(self.parent.song_object_list) - 1]
        self.parent.frames[f].display_details(s)

        # delete last item in the song_object_list so it doesnt carry over to other pages
        del self.parent.song_object_list[-1]
