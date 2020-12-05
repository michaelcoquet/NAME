"""CMPT 370 Group 5 Project: NAME (Nearly Analogous Music Engine)
    Summary:  is a piece of software to compare songs using the Spotify API. NAME will help the
              user find other similar songs to the ones they are interested in, as well as
              detailed info about their favorite songs.
"""
import os
import name.gui as gui
import tkinter as tk
from tkinter import Grid

from name.backend_classes.user import User


class Name(tk.Tk):
    """TODO: fill out docstring -- basically the gui wrapper
       TODO: set up a finite state machine to flip between frames in a more controlled fashion
       TODO: move all the code in this class to a seperate gui wrapper class just to keep the
             main entry point of the app clean
    Args:
        tk ([type]): [description]
    """
    max_songs = 6 # need to set a maximum number of songs that can show up in the search
    active_frame = 11 # the frame that is currently shown to the user
    previous_frame = 11

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Nearly Analagous Music Engine")
        self.iconbitmap("name\\resources\\ravencon.ico") # TODO: make suren to change this to be
                                                   # accessable from anywhere
        Grid.rowconfigure(self, 0, weight=1)
        Grid.columnconfigure(self, 0, weight=1)

        # container frame
        container = tk.Frame(self)
        container.grid(row=0, column=0, sticky="nsew")
        container.grid_rowconfigure(1, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.grid(padx="10", pady="10")

        # working list of songs (displayed in the song_treeview widgets)
        self.song_object_list = []

        # instantiate frame array
        self.frames = {}

        # instantiate the user
        self.user = User()

        # instantiate the frames
        self.frames[0] = gui.CompareSongsFrame(self, container, self.user)
        self.frames[1] = gui.SearchResultsFrame(self, container, self.user)
        self.frames[2] = gui.SongInfoSearchFrame(self, container, self.user)
        self.frames[3] = gui.SongInfoFrame(self, container, self.user)
        self.frames[4] = gui.SongStatsFrame(self, container, self.user)
        self.frames[5] = gui.MemberHomeFrame(self, container, self.user)
        self.frames[6] = gui.PlaylistInfoFrame(self, container, self.user)
        self.frames[7] = gui.PlaylistEditFrame(self, container, self.user)
        self.frames[8] = gui.AllPlaylistsFrame(self, container, self.user)
        self.frames[9] = gui.CreateSimPlaylistFrame(self, container, self.user)
        self.frames[10] = gui.ListeningHabitsFrame(self, container, self.user)
        self.frames[11] = gui.HomePageFrame(self, container, self.user)

        #instantiate group frames
        self.frames[12] = gui.EditGroupFrame(self, container, self.user)
        self.frames[13] = gui.GroupStatsFrame(self, container, self.user)
        self.frames[14] = gui.EditGroupPlaylistFrame(self, container, self.user)
        self.frames[15] = gui.GroupHomeFrame(self, container, self.user)

        for i in self.frames:
            self.frames[i].grid_forget()

        self.frames[11].grid_remember()

    def update_search_results(self, list):
        """ used to update the listbox in the search results frame

        Args:
            list (song[]): list of songs returned from the API in the search function to update
                           the listbox in the search results frame
        """
        # this is just temporary will likely change when we have a proper list of song objects
        for item in range(len(list)):
            self.frames[1].song_listbox.insert(item, list[item])

    def switch_frame(self, old_id, new_id):
        """ TODO: Fill In

        Args:
            old_id ([type]): TODO: Fill In
            new_id ([type]): TODO: Fill In
        """
        self.frames[old_id].grid_forget()
        self.frames[new_id].grid_remember()
        self.previous_frame = old_id
        self.active_frame = new_id

    def switch_to_previous_frame(self):
        """ TODO: Fill In
        """
        self.switch_frame(self.active_frame, self.previous_frame)

    def get_frame_id(self, name):
        """ get the frame id based on the given name see GUI FSM diagram in wiki
            maybe not the best way to do this but its fine for now

        Args:
            name (string): the name of desired frame id

        Returns:
            integer: the corresponding frame_id of given name
        """
        if name == "Compare Songs":
            return 0
        elif name == "Search Results":
            return 1
        elif name == "Song Info Search":
            return 2
        elif name == "Song Info":
            return 3
        elif name == "Song Stats":
            return 4
        elif name == "Member Home":
            return 5
        elif name == "Playlist Info":
            return 6
        elif name == "Playlist Edit":
            return 7
        elif name == "All Playlists":
            return 8
        elif name == "Create Sim Playlist":
            return 9
        elif name == "Listening Habits":
            return 10
        elif name == "Home Page":
            return 11
        elif name == "Edit Group":
            return 12
        elif name == "Group Stats":
            return 13
        elif name == "Edit Group Playlist":
            return 14
        elif name == "Group Home":
            return 15
        else:
            print("ERROR NO SUCH FRAME")
            exit()

def main():
    """ main entry point
    """
    app = Name()
    app.mainloop()
    if os.path.exists(".cache"):
        os.remove(".cache")

if __name__ == "__main__":
    main()
