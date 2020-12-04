""" TODO: fill in
"""
import tkinter as tk
import tkinter.scrolledtext as st

from .home_page_frame import HomePageFrame
from name.backend_classes.lyrics import Lyrics

class SongInfoFrame(HomePageFrame):
    """ TODO: fill in

    Args:
        tk ([type]): TODO: fill in
    """

    def grid_forget(self):
        super().grid_forget()
        self.song_info_scrolledtext.grid_forget()
        self.start_over_button.grid_forget()
        self.ply_from_ply_button.grid_forget()

    def init_middle_grid(self):
        """TODO: fill in
        """
        super().init_middle_grid()
        self.filters_dropdown.grid_forget()
        self.song_search_entry.grid_forget()
        self.song_search_button.grid_forget()
        self.song_treeview.grid_forget()

        self.song_info_scrolledtext = st.ScrolledText(self.middle_grid)
        self.song_info_scrolledtext.grid(row=0, column=0, sticky="nsew")
        self.song_lyrics_scrolledtext = st.ScrolledText(self.middle_grid)
        self.song_lyrics_scrolledtext.grid(row=0, column=1, sticky="nsew")

    def init_lower_grid(self):
        """TODO: fill in
        """
        super().init_lower_grid()
        self.remove_all_button.grid_forget()
        self.remove_button.grid_forget()
        self.similar_songs_button.grid_forget()

        self.start_over_button = tk.Button(self.lower_grid, text="Start Over",
            command=self.start_over_command)

        self.ply_from_ply_button = tk.Button(
            self.lower_grid,
            text="Make a new similar\nplaylist from this one",
            command=self.ply_from_ply_command
        )
        self.ply_from_ply_button.grid(row=0, column=2)

    def display_details(self, song):
        """gets the details of a song from another frame and displays it in the scrolledText
           widget

        Args:
            song (song):
        """
        # delete any details that might have already been in the display
        self.song_info_scrolledtext.delete("1.0", "end")
        # display new results
        self.song_info_scrolledtext.insert("end", song.__str__())
        # display the song lyrics in the other textbox
        self.song_lyrics_scrolledtext.delete("1.0", "end")
        lyrics_obj = Lyrics(song.song_name, song.song_artist[0].name)
        self.song_lyrics_scrolledtext.insert("end", "Lyrics:\n\n" + song.song_name + " - " +
                                                  song.song_artist[0].name +
                                                  ":\n\n" + lyrics_obj.get_lyrics())

    def start_over_command(self):
        """command for the start over button
        """
        self.switch_frame("Song Info Search")

    def ply_from_ply_command(self):
        """command for playlist from playlist button
        """
        # TODO: BACKEND - Do a search for similar songs to the songs in the currently selected
        #                 playlist
        self.open_search_progress()

    def song_select_dropdown_command(self, item):
        """ overrides parent song select dropdown command, dont super it though
        """
        super().song_select_dropdown_command(item)

        self.ply_from_ply_button.grid_forget()

        # pass the data to the scrolledText widget on the next screen
        self.display_details(self.song_object_list[0])

        # clear the list object after
        self.song_object_list.clear()
