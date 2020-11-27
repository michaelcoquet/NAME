""" TODO: fill in
"""
import tkinter as tk
import tkinter.scrolledtext as st

from .home_page_frame import HomePageFrame


class SongInfoFrame(HomePageFrame):
    """ TODO: fill in

    Args:
        tk ([type]): TODO: fill in
    """
    def __init__(self, parent, container):
        super().__init__(parent, container)
        self.container = container
        self.parent = parent

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

        self.song_info_scrolledtext.insert(tk.INSERT,
        """\
Lots of song details
    - sdf
    - as
    - ff
    - n
        """) # remove this when we get real results back

    def init_lower_grid(self):
        """TODO: fill in
        """
        super().init_lower_grid()
        self.remove_all_button.grid_forget()
        self.similar_songs_button.grid_forget()

        self.start_over_button = tk.Button(self.lower_grid, text="Start Over",
            command=self.start_over_command)
        self.start_over_button.grid(row=0, column=0)

        self.ply_from_ply_button = tk.Button(
            self.lower_grid,
            text="Make a new similar\nplaylist from this one",
            command=self.ply_from_ply_command
        )
        self.ply_from_ply_button.grid(row=0, column=2)

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
