""" TODO: fill in
"""
import tkinter as tk
from .home_page import HomePageFrame


class SearchResultsFrame(HomePageFrame):
    """ TODO: fill in

    Args:
        tk ([type]): TODO: fill in
    """
    def __init__(self, parent, container):
        super().__init__(parent, container)
        self.container = container
        self.parent = parent

    def init_lower_grid(self):
        super().init_lower_grid()
        self.remove_all_button.grid_forget()
        self.start_over_button = tk.Button(self.lower_grid)
        self.start_over_button["text"] = "Start Over"
        self.start_over_button.grid(row=0, column=0)

        self.get_stats_button = tk.Button(self.lower_grid)
        self.get_stats_button["text"] = "Get Stats"
        self.get_stats_button.grid(row=0, column=1)

        self.similar_songs_button.grid_forget()
        self.save_button = tk.Button(self.lower_grid, text="Save")
        self.save_button.grid(row=0, column=2)
    # def init_middle_grid(self):
    #     super().init_middle_grid()

    # def init_upper_grid(self):
    #     super().init_upper_grid()
