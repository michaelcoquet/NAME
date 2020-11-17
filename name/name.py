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
        # self.frames[gui.CompareSongsFrame] = gui.CompareSongsFrame(container, self)
        # self.frames[gui.SearchProgressFrame] = gui.SearchProgressFrame(container, self)
        # self.frames[gui.SearchResultsFrame] = gui.SearchResultsFrame(container, self)
        # self.frames[gui.SongInfoSearchFrame] = gui.SongInfoSearchFrame(container, self)
        # self.frames[gui.SongInfoFrame] = gui.SongInfoFrame(container, self)
        # self.frames[gui.SongStatsFrame] = gui.SongStatsFrame(container, self)
        # self.frames[gui.MemberHomeFrame] = gui.MemberHomeFrame(container, self)
        # self.frames[gui.PlaylistInfoFrame] = gui.PlaylistInfoFrame(container, self)
        # self.frames[gui.PlaylistEditFrame] = gui.PlaylistEditFrame(container, self)
        # self.frames[gui.AllPlaylistsFrame] = gui.AllPlaylistsFrame(container, self)
        # self.frames[gui.CreateSimPlaylistFrame] = gui.CreateSimPlaylistFrame(container, self)
        # self.frames[gui.ListeningHabitsFrame] = gui.ListeningHabitsFrame(container, self)
        self.frames[gui.HomePageFrame] = gui.HomePageFrame(container, self)

    def login(self):
        """ Button command to link to a spotify account and if succesfully linked switch to the
            member frame (frame_id = 2).
            TODO: this is where the connection to the backend login function should check
                  if the user successuflly linked their spotify account
        """
        self.logged_in = 1 # TODO: change this with a real check
        if self.logged_in:
            print("successfully logged into spotify, switch to member frame")
        else:
            print("error unsuccessfully linked spotify account")

    @staticmethod #remove later
    def filter_function():
        """ Filters available for the user to search with
            TODO: link the users choice of filter with the search function for now just return
                  anything
        """
        return 1


def main():
    """ main entry point
    """
    app = Name()
    app.mainloop()

if __name__ == "__main__":
    main()
