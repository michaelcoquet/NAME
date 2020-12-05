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

    def grid_unmap(self):
        super().grid_unmap()
        self.song_info_scrolledtext.grid_remove()
        self.start_over_button.grid_remove()

    def init_upper_grid(self):
        super().init_upper_grid()
        self.create_playlist_button["state"] = tk.NORMAL
        self.get_song_info_button["state"] = tk.DISABLED
        self.filters_dropdown.grid_remove()
        self.song_search_entry.grid_remove()
        self.song_search_button.grid_remove()

    def init_middle_grid(self):
        """TODO: fill in
        """
        super().init_middle_grid()
        self.filters_dropdown.grid_remove()
        self.song_search_entry.grid_remove()
        self.song_search_button.grid_remove()
        self.song_treeview.grid_remove()

        self.song_info_scrolledtext = st.ScrolledText(self.middle_grid)
        self.song_info_scrolledtext.grid(row=0, column=0, sticky="nsew")
        self.song_lyrics_scrolledtext = st.ScrolledText(self.middle_grid)
        self.song_lyrics_scrolledtext.grid(row=0, column=1, sticky="nsew")

    def init_lower_grid(self):
        """TODO: fill in
        """
        super().init_lower_grid()
        self.remove_all_button.grid_remove()
        self.remove_button.grid_remove()
        self.similar_songs_button.grid_remove()

        self.start_over_button = tk.Button(self.lower_grid, text="Start Over",
            command=self.start_over_command)

        self.start_over_button.grid(row=0, column=0)

    def display_details(self, song):
        """gets the details of a song from another frame and displays it in the scrolledText
           widget

        Args:
            song (song):
        """
        # delete any details that might have already been in the display
        self.song_info_scrolledtext.configure(state="normal")
        self.song_info_scrolledtext.delete("1.0", "end")
        # display new results
        self.song_info_scrolledtext.insert("end", song.__str__())
        # make sure the text can't be edited within the app
        self.song_info_scrolledtext.configure(state="disabled")
        # display the song lyrics in the other textbox
        self.song_lyrics_scrolledtext.configure(state="normal")
        self.song_lyrics_scrolledtext.delete("1.0", "end")
        lyrics_obj = Lyrics(song.song_name, song.song_artist[0].name)
        if lyrics_obj.get_lyrics() != None:
            self.song_lyrics_scrolledtext.insert("end", "Lyrics:\n\n" + song.song_name + " - " +
                                                  song.song_artist[0].name +
                                                  ":\n\n" + lyrics_obj.get_lyrics())
        else:
            self.song_lyrics_scrolledtext.insert("end", "Couldn't find lyrics for this song \n")
        self.song_lyrics_scrolledtext.configure(state="disabled")

    def start_over_command(self):
        """command for the start over button
        """
        self.switch_frame("Song Info Search")

    def song_select_dropdown_command(self, item):
        """ overrides parent song select dropdown command, dont super it though
        """
        super().song_select_dropdown_command(item)

        self.ply_from_ply_button.grid_remove()

        # pass the data to the scrolledText widget on the next screen
        self.display_details(self.song_object_list[0])

        # clear the list object after
        self.song_object_list.clear()
