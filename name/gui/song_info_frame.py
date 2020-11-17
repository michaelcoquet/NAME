""" TODO: fill in
"""
import tkinter as tk
import tkinter.scrolledtext as st
from .home_page import HomePageFrame


class SongInfoFrame(HomePageFrame):
    """ TODO: fill in

    Args:
        tk ([type]): TODO: fill in
    """
    def __init__(self, parent, container):
        super().__init__(parent, container)
        self.container = container
        self.parent = parent

    def init_middle_grid(self):
        """TODO: fill in
        """
        super().init_middle_grid()
        self.filters_dropdown.grid_forget()
        self.song_search_entry.grid_forget()
        self.song_search_button.grid_forget()
        self.song_listbox.grid_forget()
        self.song_info_scrolledtext = st.ScrolledText(self.middle_grid)
        self.song_info_scrolledtext.grid(row=0, column=0, sticky="nsew")
        self.song_info_scrolledtext.insert(tk.INSERT,
        """\
Lots of song details
    - sdf
    - as
    - ff
    - n
        """)

    def init_lower_grid(self):
        """TODO: fill in
        """
        super().init_lower_grid()
        self.remove_all_button.grid_forget()
        self.similar_songs_button.grid_forget()
        self.start_over_button = tk.Button(self.lower_grid, text="Start Over")
        self.start_over_button.grid(row=0, column=0)
