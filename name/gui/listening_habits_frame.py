""" TODO: fill in
"""
import tkinter as tk
import tkinter.scrolledtext as st

from .member_home_frame import MemberHomeFrame


class ListeningHabitsFrame(MemberHomeFrame):
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
        self.latest_playlist_button.grid_forget()
        self.all_playlists_button.grid_forget()
        self.listening_habits_button.grid_forget()

    def init_lower_grid(self):
        super().init_lower_grid()
        self.edit_button.grid_forget()
        self.save_spotify_button.grid_forget()
        self.playlist_info_button.grid_forget()


    def init_middle_grid(self):
        super().init_middle_grid()

        self.top_songs_scrolledtext = st.ScrolledText(self.middle_grid)
        self.top_songs_scrolledtext.grid(row=0, column=0, sticky="nsew")
        self.top_artists_scrolledtext = st.ScrolledText(self.middle_grid)
        self.top_artists_scrolledtext.grid(row=0, column=1, sticky="nsew")
        self.recent_songs_scrolledtext = st.ScrolledText(self.middle_grid)
        self.recent_songs_scrolledtext.grid(row=0, column=2, sticky="nsew")

    def init_upper_grid(self):
        super().init_upper_grid()
        self.create_playlist_button.grid_forget()
        self.compare_songs_button.grid_forget()
        self.get_song_info_button.grid_forget()
        self.song_search_entry.grid_forget()
        self.filters_dropdown.grid_forget()
        self.song_search_button.grid_forget()

        self.latest_playlist_button = tk.Button(
            self.upper_grid,
            text="Latest Playlist",
            command=self.latest_playlist_command)
        self.latest_playlist_button.grid(row=1, column=0)

        self.all_playlists_button = tk.Button(
            self.upper_grid,
            text="All Playlists",
            command=self.all_playlists_command)
        self.all_playlists_button.grid(row=1, column=1)

        self.listening_habits_button = tk.Button(
            self.upper_grid,
            text="Your Listening Habits",
            state=tk.DISABLED)
        self.listening_habits_button.grid(row=1, column=2)

    def all_playlists_command(self):
        """command for the all playlists button
        """
        self.switch_frame("All Playlists")

    def latest_playlist_command(self):
        """command for the latest playlist button
        """
        self.switch_frame("Member Home")

    def display_top_songs(self, songs):
        """ Displays each of the top songs in the
        top song scrolldown section.
        songs: a list of song objects
        """
        # delete any details that might have already been in the display
        self.top_songs_scrolledtext.delete("1.0", "end")
        # display new results
        self.top_songs_scrolledtext.insert("end", song[0].__str__())