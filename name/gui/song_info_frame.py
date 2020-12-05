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

    def grid_remember(self):
        super().grid_remember()
        self.create_playlist_button.grid_remove()
        self.compare_songs_button.grid_remove()
        self.get_song_info_button.grid_remove()
        self.song_treeview.grid_remove()
        self.similar_songs_button.grid_remove()
        self.filters_dropdown.grid_remove()
        self.remove_button.grid_remove()
        self.remove_all_button.grid_remove()

        self.song_info_scrolledtext.grid()
        self.start_over_button.grid()

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

    def display_details(self, songs):
        """gets the details of a song from another frame and displays it in the scrolledText
           widget

        Args:
            song (song):
        """
        self.song_info_scrolledtext.configure(state="normal")
        self.song_lyrics_scrolledtext.configure(state="normal")

        self.song_info_scrolledtext.delete("1.0", "end")
        self.song_lyrics_scrolledtext.delete("1.0", "end")

        check_list = type(songs) is list

        if check_list:
            for song in songs:
                # display new results
                self.song_info_scrolledtext.insert("end", str(song) + "\n\n\n")
                lyrics_obj = Lyrics(song.song_name, song.song_artist[0].name)
                if lyrics_obj.get_lyrics() != None:
                    self.song_lyrics_scrolledtext.insert("end", "Lyrics:\n\n" + song.song_name + " - " +
                                                        ", ".join(dict(song)["song_artist"]) +
                                                        ":\n\n" + lyrics_obj.get_lyrics() + "\n\n\n")
                else:
                    self.song_lyrics_scrolledtext.insert("end", "Couldn't find lyrics for this song \n")
        else:
            # display new results
            self.song_info_scrolledtext.insert("end", str(songs) + "\n\n\n")

            lyrics_obj = Lyrics(songs.song_name, songs.song_artist[0].name)
            if lyrics_obj.get_lyrics() != None:
                self.song_lyrics_scrolledtext.insert("end", "Lyrics:\n\n" + songs.song_name + " - " +
                                                    ", ".join(dict(songs)["song_artist"]) +
                                                    ":\n\n" + lyrics_obj.get_lyrics() + "\n\n\n")
            else:
                self.song_lyrics_scrolledtext.insert("end", "Couldn't find lyrics for this song \n")

        self.song_info_scrolledtext.configure(state="disable")
        self.song_lyrics_scrolledtext.configure(state="disable")

    def display_tuple(self, song):
        """ display data from the tree view instead of song object

        Args:
            song (tuple): representation of a song object
        """
        self.song_info_scrolledtext.delete("1.0", "end")
        self.song_lyrics_scrolledtext.delete("1.0", "end")

        print(song)
        self.song_info_scrolledtext.insert("end", song + "\n\n\n")

    def start_over_command(self):
        """command for the start over button
        """
        self.parent.switch_to_previous_frame()

    def song_select_dropdown_command(self, item):
        """ overrides parent song select dropdown command, dont super it though
        """
        super()
        # make sure the user has actually made a selection
        if self.song_selection.get() != self.song_selection_default:
            # get the item that is currently selected in the OptionMenu dropdown
            item = self.song_selection.get()
        artists_string_list = []

        # search the original list of song objects returned from the API for the item
        for song_search in self.api_search_results:
            # build string for comparison to find object probably a better way to do this
            for artist in song_search.song_artist:
                artists_string_list.append(artist.name)
            artists_string = ", ".join(artists_string_list)

            artists_string_list.clear()

            comp_str = song_search.song_name + "  -  " + artists_string

            if item == comp_str:
                # close the popup window after the user makes a selection
                self.close_single_search_window()

                # add this song to the list of songs
                self.song_info_scrolledtext.delete("1.0", "end")
                self.song_lyrics_scrolledtext.delete("1.0", "end")
                # print("song_object_list:    " + str(self.parent.song_object_list) + "\n\n\n\n")
                # for song_from_list in self.parent.song_object_list:
                #     print("song_search" + str(song_search))
                #     print("song_from_list" + str(song_from_list))

                #     if (
                #         song_from_list.song_name == song_search.song_name and
                #         song_from_list.song_artist == song_search.song_artist
                #     ):

                self.display_details(song_search)

                break

