""" TODO: fill in
"""
import tkinter as tk

from .home_page_frame import HomePageFrame


class SearchResultsFrame(HomePageFrame):
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
        self.start_over_button.grid_forget()
        self.get_stats_button.grid_forget()
        self.save_button.grid_forget()

    def init_lower_grid(self):
        super().init_lower_grid()
        self.remove_all_button.grid_forget()
        self.remove_button.grid_forget()

        self.start_over_button = tk.Button(self.lower_grid, command=self.start_over_command)
        self.start_over_button["text"] = "Start Over"
        self.start_over_button.grid(row=0, column=0)

        self.get_stats_button = tk.Button(self.lower_grid, command=self.get_stats_command)
        self.get_stats_button["text"] = "Get Stats"
        self.get_stats_button.grid(row=0, column=1)

        self.similar_songs_button.grid_forget()
        self.save_button = tk.Button(self.lower_grid, text="Save")
        self.save_button.grid(row=0, column=2)

    def get_stats_command(self):
        """command for the get stats button
        """
        self.switch_frame("Song Stats")

    def start_over_command(self):
        """command for start over button
        """
        self.switch_frame("Home Page")

    def display_data(self, songlist):
        """ display the results of the similarity search in the tree view
        """
        artists_string_list = []
        for song in songlist:
            for artist in song.song_artist:
                artists_string_list.append(artist.name)
            artists_string = ", ".join(artists_string_list)

            artists_string_list.clear()

            self.song_treeview.insert("", "end", values=(song.song_name,
                            song.album_details.name, artists_string))