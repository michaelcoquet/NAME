""" TODO: fill in
"""
from .home_page import HomePageFrame


class SongInfoSearchFrame(HomePageFrame):
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
        self.song_listbox.grid_forget()

    def init_lower_grid(self):
        """TODO: fill in
        """
        super().init_lower_grid()
        self.remove_all_button.grid_forget()
        self.similar_songs_button.grid_forget()
