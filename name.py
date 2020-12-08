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
    """Main entry point for the app basically wraps the GUI
       set up a finite state machine to flip between frames in a more controlled fashion
    Args:
        tk (Tk): a tk application object
    """
    max_songs = 6 # need to set a maximum number of songs that can show up in the search
    active_frame =  9 # the frame that is currently shown to the user
    previous_frame = 9

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Nearly Analagous Music Engine")
        self.iconbitmap("name\\resources\\ravencon.ico")

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
        self.frames[1] = gui.SongInfoSearchFrame(self, container, self.user)
        self.frames[2] = gui.SongInfoFrame(self, container, self.user)
        self.frames[3] = gui.SongStatsFrame(self, container, self.user)
        self.frames[4] = gui.MemberHomeFrame(self, container, self.user)
        self.frames[5] = gui.PlaylistEditFrame(self, container, self.user)
        self.frames[6] = gui.AllPlaylistsFrame(self, container, self.user)
        self.frames[7] = gui.SavePlaylistFrame(self, container, self.user)
        self.frames[8] = gui.ListeningHabitsFrame(self, container, self.user)
        self.frames[9] = gui.HomePageFrame(self, container, self.user)

        #instantiate group frames
        self.frames[10] = gui.EditGroupFrame(self, container, self.user)
        self.frames[11] = gui.EditGroupPlaylistFrame(self, container, self.user)
        self.frames[12] = gui.GroupHomeFrame(self, container, self.user)
        self.frames[13] = gui.SongInfoMemberFrame(self, container, self.user)

        for i in self.frames:
            self.frames[i].grid_unmap()

        self.frames[self.get_frame_id("Home Page")].grid_init()

    def switch_frame(self, old_id, new_id):
        """ This will switch the state in the finite state machine to the next state based on
            some event

        Args:
            old_id (int): The previously active frame
            new_id (int): THe frame being switched too
        """
        self.frames[old_id].grid_unmap()
        self.frames[new_id].grid_remember()
        self.previous_frame = old_id
        self.active_frame = new_id

    def switch_to_previous_frame(self):
        """ switch to the previously active frame
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
        elif name == "Song Info Search":
            return 1
        elif name == "Song Info":
            return 2
        elif name == "Song Stats":
            return 3
        elif name == "Member Home":
            return 4
        elif name == "Playlist Edit":
            return 5
        elif name == "All Playlists":
            return 6
        elif name == "Save Playlist":
            return 7
        elif name == "Listening Habits":
            return 8
        elif name == "Home Page":
            return 9
        elif name == "Edit Group":
            return 10
        elif name == "Edit Group Playlist":
            return 11
        elif name == "Group Home":
            return 12
        elif name == "Song Info Member":
            return 13
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
