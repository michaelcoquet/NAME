"""CMPT 370 Group 5 Project: NAME
    Summary: TODO: fill in summary of app
"""
import tkinter as tk
import gui
from tkinter import Grid


class Name(tk.Tk):
    """TODO: fill out docstring -- basically the gui wrapper
       TODO: set up a finite state machine to flip between frames in a more controlled fashion

    Args:
        tk ([type]): [description]
    """
    max_songs = 6 # need to set a maximum number of songs that can show up in the search
    active_frame = 11 # the frame that is currently shown to the user

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.logged_in = 0

        self.title("Nearly Analagous Music Engine")
        self.iconbitmap("resources\\ravencon.ico") # TODO: make suren to change this to be
                                                   # accessable from anywhere
        Grid.rowconfigure(self, 0, weight=1)
        Grid.columnconfigure(self, 0, weight=1)

        # container frame
        container = tk.Frame(self)
        container.grid(row=0, column=0, sticky="nsew")
        container.grid_rowconfigure(1, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.grid(padx="10", pady="10")

        # instantiate frame array
        self.frames = {}

        # instantiate the frames
        self.frames[0] = gui.CompareSongsFrame(self, container)
        self.frames[1] = gui.SearchResultsFrame(self, container)
        self.frames[2] = gui.SongInfoSearchFrame(self, container)
        self.frames[3] = gui.SongInfoFrame(self, container)
        self.frames[4] = gui.SongStatsFrame(self, container)
        self.frames[5] = gui.MemberHomeFrame(self, container)
        self.frames[6] = gui.PlaylistInfoFrame(self, container)
        self.frames[7] = gui.PlaylistEditFrame(self, container)
        self.frames[8] = gui.AllPlaylistsFrame(self, container)
        self.frames[9] = gui.CreateSimPlaylistFrame(self, container)
        self.frames[10] = gui.ListeningHabitsFrame(self, container)
        for i in self.frames:
            self.frames[i].grid_forget()
        self.frames[11] = gui.HomePageFrame(self, container)

    def switch_frame(self, old_id, new_id):
        """ TODO: Fill In

        Args:
            old_id ([type]): TODO: Fill In
            new_id ([type]): TODO: Fill In
        """
        self.frames[old_id].grid_forget()
        self.frames[new_id].grid_remember()
        self.active_frame = new_id

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
        else:
            print("ERROR NO SUCH FRAME")
            exit()

def main():
    """ main entry point
    """
    app = Name()
    app.mainloop()

if __name__ == "__main__":
    main()
