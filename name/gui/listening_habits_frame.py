""" TODO: fill in
"""
import tkinter as tk
import tkinter.scrolledtext as st
import operator

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
        self.song_treeview.grid_forget()

        self.top_songs_scrolledtext = st.ScrolledText(self.middle_grid, width=40)
        self.top_songs_scrolledtext.grid(row=0, column=0, sticky="nsew")
        self.top_artists_scrolledtext = st.ScrolledText(self.middle_grid, width=40)
        self.top_artists_scrolledtext.grid(row=0, column=1, sticky="nsew")
        self.recent_songs_scrolledtext = st.ScrolledText(self.middle_grid, width=40)
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
        """ Displays each of the top songs in the top song scrolldown section.
        Also displays a list of top genres.
        songs: a list of song objects
        """
        # delete any details that might have already been in the display
        self.top_songs_scrolledtext.configure(state="normal")
        self.top_songs_scrolledtext.delete("1.0", "end")
        # add top songs and collect genre info
        genres = {}
        self.top_songs_scrolledtext.insert("end", "These are your top songs: \n\n")
        for song in songs:
            self.top_songs_scrolledtext.insert("end", song.song_name + "\n")
            genre_lst = self.parent.spotify_manager.get_song_genres(song)
            for genre in genre_lst:
                if genre not in genres:
                    genres[genre] = 1
                else:
                    genres[genre] += 1
        # get top 5 genres
        top_genres = dict(sorted(genres.items(), key=operator.itemgetter(1), reverse=True)[:5])
        # first add some newlines so it looks nicer
        self.top_songs_scrolledtext.insert("end", "\n\n\n")
        self.top_songs_scrolledtext.insert("end", "Your top 5 genres are: \n\n")
        for genre in top_genres:
            self.top_songs_scrolledtext.insert("end", genre + "\n")
        # prevent users from typing in the text area
        self.top_songs_scrolledtext.configure(state="disabled")

    def display_recent_songs(self, songs):
        """ Displays the the member's recent songs
        that they have played on spotify.
        songs: a list of song objects (the recent songs)
        """
        # delete any details that might have already been in the display
        self.recent_songs_scrolledtext.configure(state="normal")
        self.recent_songs_scrolledtext.delete("1.0", "end")
        # add recent songs
        self.recent_songs_scrolledtext.insert("end", "Your recently played songs are: \n\n")
        for song in songs:
            self.recent_songs_scrolledtext.insert("end", song.song_name + "\n")
        # prevent users from typing in the text area
        self.recent_songs_scrolledtext.configure(state="disabled")
