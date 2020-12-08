"""CMPT 370 Group 5 Project: NAME (Nearly Analogous Music Engine)
    Credits: Michael Coquet
             Elizabeth Reid
             Ben Camplin
             Laurence Craig Garcia
             Sean Warren
"""
import tkinter as tk
from tkinter import ttk

from .home_page_frame import HomePageFrame
from name.backend_classes.checking_song_similarity import CheckingSongSimilarity

class CompareSongsFrame(HomePageFrame):
    """ This the frame a user goes to compare lists of 2 or more songs
        for similairty score

    Args:
        tk (Frame): inheritied from main home page
    """

    def grid_unmap(self):
        super().grid_unmap()
        self.get_stats_button.grid_remove()

    def grid_remember(self):
        super().grid_remember()
        self.similar_songs_button.grid_remove()

        self.get_stats_button.grid()
        self.display_data(self.parent.song_object_list)

    def init_upper_grid(self):
        super().init_upper_grid()
        self.compare_songs_button["state"] = tk.DISABLED
        self.create_playlist_button["state"] = tk.NORMAL

    def init_lower_grid(self):
        super().init_lower_grid()
        self.similar_songs_button.grid_remove()

        self.get_stats_button = tk.Button(self.lower_grid, command=self.song_stats_cmd)
        self.get_stats_button["text"] = "Get Stats"
        self.get_stats_button.grid(row=0, column=2)

    def song_stats_cmd(self):
        """ command for song stats btn
        """
        # check to make sure two or more songs have been entered
        if len(self.parent.song_object_list) < 2:
            message = "Enter at least two songs to compare their stats!"
            self.enter_more_songs_popup(message)
        else:
            self.switch_frame("Song Stats")

            # Return similarities of the two or more selected songs
            self.formatted_filters = self.convert_filters_list(self.parent.song_object_list)
            sim_scores_obj = CheckingSongSimilarity(self.formatted_filters)
            sim_score = sim_scores_obj.get_songs_similarity_score(self.parent.song_object_list)

            # Update the srcolledText widget in the song stats frame with the
            # returned data
            d = [int(sim_score), self.parent.song_object_list]
            self.parent.frames[self.parent.get_frame_id("Song Stats")].display(d)
