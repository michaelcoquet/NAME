""" TODO: fill in
"""
import time
import tkinter as tk
from tkinter import StringVar
from tkinter import Grid
from tkinter import Menu
from tkinter import ttk
from tkinter import messagebox

from name.backend_classes import Query
from name.backend_classes import SpotifyAPIManager


class NameFrame(tk.Frame):
    """ TODO: fill in

    Args:
        tk ([type]): TODO: fill in
    """
    def __init__(self, parent, container):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.container = container
        self.init_upper_grid()
        self.init_middle_grid()
        self.init_lower_grid()
        self.init_guest_menu()

        # needed for the progress bar in search progress pop up window
        self.win = None
        self.progress = None
        self.l_songs_found = None

        l = []
        self.query_object = Query(l)

        self.api_search_results = []

        self.final_song_selection = []

        #instantiate the spotify api manager
        self.spotify_manager = SpotifyAPIManager()

    def grid_forget(self):
        self.upper_grid.grid_forget()
        self.middle_grid.grid_forget()
        self.lower_grid.grid_forget()

    def grid_remember(self):
        self.init_lower_grid()
        self.init_middle_grid()
        self.init_upper_grid()

    def init_guest_menu(self):
        """ make the default menu for guest users
        """
        self.guest_menu = tk.Menu(self.container)
        self.guest_menu.add_command(label="Login", command=self.login)
        self.parent.config(menu=self.guest_menu)

    def init_member_menu(self):
        """ make the menu for when a user links their spotify account
        """
        self.member_menu = tk.Menu(self.container)

        self.my_account_menu = tk.Menu(self.member_menu, tearoff=0)
        self.my_account_menu.add_command(label="Member Home", command=self.member_home_command)
        self.my_account_menu.add_separator()

        # make a submenu for groups
        self.group_menu = tk.Menu(self.my_account_menu, tearoff=0)
        self.group_menu.add_command(label="Create Group", command=self.create_group)
        self.group_menu.add_separator()
        self.my_account_menu.add_cascade(label="Groups", menu=self.group_menu)
        self.my_account_menu.add_command(label="Get Shareable ID", command=self.get_id_command)
        self.my_account_menu.add_separator()

        self.my_account_menu.add_command(label="Log Out", command=self.log_out)

        self.member_menu.add_cascade(label="My Account", underline=0, menu=self.my_account_menu)
        self.parent.config(menu=self.member_menu)

    def create_group(self):
        """ Menu option to create a new group
            TODO: backend connection required here to create a new group, for now just assume
                  the user sucessfully created a new group and add a new menu option as in the
                  storyboards
        """
        self.switch_frame("Edit Group")

    def init_upper_grid(self):
        """ TODO: fill in
        """
        self.upper_grid = tk.Frame(self.container)
        self.upper_grid.grid(row=0, column=0, sticky="nw")

        # could put an image logo here if desired, for now just a label
        self.app_title_button = tk.Button(self.upper_grid)
        self.app_title_button["text"] = "N.A.M.E"
        self.app_title_button["command"] = self.app_title_command
        self.app_title_button.grid(row=0, column=1)

    def init_lower_grid(self):
        """ TODO: fill in
        """
        self.lower_grid = tk.Frame(self.container)
        Grid.columnconfigure(self.lower_grid, 1, weight=1)

        self.lower_grid.grid(row=2, column=0, sticky="ew")

    def init_middle_grid(self):
        """ TODO: fill in
        """
        self.middle_grid = tk.Frame(self.container)
        Grid.columnconfigure(self.middle_grid, 0, weight=1)
        Grid.rowconfigure(self.middle_grid, 0, weight=1)

        self.middle_grid.grid(row=1, column=0, sticky="nsew")

    def switch_frame(self, name):
        """ switch to the given frame

        Args:
            name (string): pass the name of the desired frame to switch to
        """
        self.parent.switch_frame(self.parent.active_frame, self.parent.get_frame_id(name))

    def app_title_command(self):
        self.switch_frame("Home Page")

    def login(self):
        """ Button command to link to a spotify account and if succesfully linked switch to the
            member frame (frame_id = 2).
        """
        if self.spotify_manager.link_spotify_account() == True:
            self.init_member_menu()
        else:
            print("error unsuccessfully linked spotify account")

    def log_out(self):
        """ Command for the logout button, should be able to just reinstantiate Spotify API
            Manager
        """
        self.spotify_manager = SpotifyAPIManager()
        self.init_guest_menu()

    def member_home_command(self):
        """ command for the member home member menu item
        """
        self.switch_frame("Member Home")

    def get_id_command(self):
        """ Command for the get shareable ID menu item
        """
        # TODO: BACKEND - Return the users spotify ID that they can share with other users to
        #                 form groups
        # TODO: GUI     - Display the returned ID in the following messagebox popup
        messagebox.showinfo("My Shareable ID", "this is the id")

    def start_single_search(self, title, filters):
        """ Search the spotify API for the given song

        Args:
            title (str): the desired song title
            filters (dict): the selected filters
        """
        # TODO: BACKEND - single song search connection return a list of songs
        self.api_search_results = self.query_object.search_single_song(title)
        self.open_song_search_popup(self.api_search_results)

    def search_similar(self, titles, filters):
        """ Search the spotify API for songs that are similar to the list of titles

        Args:
            titles  (str[]): list of song titles that the user would like to find similar songs
                             to
            filters (str[]): list of all the filters selected by the user

        Returns:
            song[]: return a list of songs that match (or partial match) the title
        """
        return 1

    def open_song_search_popup(self, api_results):
        """ open a popup for the user to select the song they actually wanted to add to the list
        """
        self.grab_set()
        self.popup = tk.Toplevel(self)
        self.popup.protocol("WM_DELETE_WINDOW", self.close_single_search_window)
        self.popup.title("Pick a Song")

        variable = StringVar(self.popup)
        variable.set("Which song were you looking for?") # default value

        names = [song_result for song_result in api_results]

        self.song_select_dropdown = tk.OptionMenu(
            self.popup,
            variable,
            *names,
            command=self.song_select_dropdown_function)
        self.song_select_dropdown.pack()


    def open_search_progress(self):
        """open a new window that updates the user on the progress of similarity playlist
           creation
        """
        self.grab_set()
        # Toplevel object which will
        # be treated as a new window
        self.win = tk.Toplevel(self)
        self.win.protocol("WM_DELETE_WINDOW", self.close_progress_window)
        # sets the title of the
        # Toplevel widget
        self.win.title("Searching")

        l_1 = tk.Label(self.win, text="Finding Similar Songs!")
        l_1.pack(side=tk.TOP)

        self.l_songs_found = tk.Label(self.win,
            text="Songs found...   0/" + str(self.parent.max_songs))
        self.l_songs_found.pack(side=tk.TOP)

        self.progress = tk.ttk.Progressbar(self.win, orient=tk.HORIZONTAL, length=200,
            mode="determinate")

        self.progress.pack(pady=10)

        cancel_btn = tk.Button(self.win, text="Cancel", command=self.close_progress_window)
        cancel_btn.pack(side=tk.BOTTOM)

        self.progress_update()

    def progress_update(self):
        """ This is used to update the search progress bar
                  for now just do a little simulation, notice the hang with time.sleep
        """
        # TODO: BACKEND - This will have to be updated by the search function(s) in the backend
        #                 to update the progress bar, could be indeterminate also, but if not
        #                 will need some multithreadin to avoid the app hanging during search,
        #                 possibly fork() would work
        count = 0
        self.progress.update()
        self.progress["maximum"] = 100
        time.sleep(1)

        self.progress['value'] = 20
        count = count + 1
        self.l_songs_found["text"] = "Songs found...   " + str(count) + "/" \
                                        + str(self.parent.max_songs)
        self.progress.update()
        time.sleep(1)

        self.progress['value'] = 40
        count = count + 1
        self.l_songs_found["text"] = "Songs found...   " + str(count) + "/" \
                                        + str(self.parent.max_songs)
        self.progress.update()
        time.sleep(1)

        self.progress['value'] = 50
        count = count + 1
        self.l_songs_found["text"] = "Songs found...   " + str(count) + "/" \
                                        + str(self.parent.max_songs)
        self.progress.update()
        time.sleep(1)

        self.progress['value'] = 60
        count = count + 1
        self.l_songs_found["text"] = "Songs found...   " + str(count) + "/" \
                                        + str(self.parent.max_songs)
        self.progress.update()
        time.sleep(1)

        self.progress['value'] = 80
        count = count + 1
        self.l_songs_found["text"] = "Songs found...   " + str(count) + "/" \
                                        + str(self.parent.max_songs)
        self.progress.update()
        time.sleep(1)

        self.progress['value'] = 100
        count = count + 1
        self.l_songs_found["text"] = "Songs found...   " + str(count) + "/" \
                                        + str(self.parent.max_songs)
        self.progress.update()
        time.sleep(1)

        self.switch_frame("Search Results")

        # TODO : GUI - need to update the search results screen with the results
        # for testing purposes
        song_list = ["hfhsjkhfs", "uiosfios", "sywyquq", "asdfsd", "ddddd", "ccccc"]

        self.parent.update_search_results(song_list)

        self.close_progress_window()

    def close_progress_window(self):
        """override window closing event
        """
        self.progress.destroy()
        self.win.destroy()
        self.grab_release()

    def close_single_search_window(self):
        """ closing window event for the single song search box
        """
        self.popup.destroy()
        self.grab_release()

    def song_select_dropdown_function(self, item):
        """ function to get the users selection of the song select dropdown box
        """
        # for i in self.api_search_results:
        self.parent.frames[11].song_treeview.insert("end", item)
        self.close_single_search_window()
