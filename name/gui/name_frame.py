"""CMPT 370 Group 5 Project: NAME (Nearly Analogous Music Engine)
    Credits: Michael Coquet
             Elizabeth Reid
             Ben Camplin
             Laurence Craig Garcia
             Sean Warren
"""
import os
import time
import threading
import tkinter as tk
from tkinter import simpledialog
from tkinter import StringVar
from tkinter import Grid
from tkinter import Menu
from tkinter import ttk

from name.backend_classes import Query


class NameFrame(tk.Frame):
    """ This is the main template for all of the frames in the app

    Args:
        tk (Frame): inherits from tk.Frame
    """
    def __init__(self, parent, container, user):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.container = container
        self.user = user

        self.init_upper_grid()
        self.init_middle_grid()
        self.init_lower_grid()
        self.init_guest_menu()

        # needed for the progress bar in search progress pop up window

        l = []
        self.query_object = Query(l)

        self.api_search_results = []

        self.final_song_selection = []

    def grid_unmap(self):
        self.upper_grid.grid_remove()
        self.middle_grid.grid_remove()
        self.lower_grid.grid_remove()

    def grid_init(self):
        self.init_lower_grid()
        self.init_middle_grid()
        self.init_upper_grid()

    def grid_remember(self):
        self.upper_grid.grid()
        self.lower_grid.grid()
        self.middle_grid.grid()

    def init_guest_menu(self):
        """ make the default menu for guest users """
        
        self.guest_menu = tk.Menu(self.container)
        self.guest_menu.add_command(label="Login", command=self.login)
        self.parent.config(menu=self.guest_menu)

    def init_member_menu(self):
        """ make the menu for when a user links their spotify account
        """
        self.member_menu = tk.Menu(self.container)

        self.my_account_menu = tk.Menu(self.member_menu, tearoff=0)
        self.my_account_menu.add_command(
            label="Member Home",
            command=self.member_home_command
        )
        self.my_account_menu.add_separator()

        # make a submenu for groups
        self.group_menu = tk.Menu(self.my_account_menu, tearoff=0)
        self.group_menu.add_command(
            label="Create Group",
            command=self.create_group
        )
        self.group_menu.add_separator()
        self.my_account_menu.add_cascade(label="Groups", menu=self.group_menu)

        for group in self.user.groups:
            self.group_menu.add_command(
                    label=group.group_name,
                    command=lambda group=group: self.group_menu_command(group)
                )

        self.my_account_menu.add_command(
            label="Get Shareable ID",
            command=self.get_id_command
        )
        self.my_account_menu.add_separator()

        self.my_account_menu.add_command(label="Log Out", command=self.log_out)

        self.member_menu.add_cascade(
            label="My Account",
            underline=0,
            menu=self.my_account_menu
        )
        self.parent.config(menu=self.member_menu)

    def create_group(self):
        """ Menu option to create a new group """
        self.switch_frame("Edit Group")

    def init_upper_grid(self):
        """ Initialize the top grid """
        
        self.upper_grid = tk.Frame(self.container)
        self.upper_grid.grid(row=0, column=0, sticky="nw")

        # could put an image logo here if desired, for now just a label
        self.app_title_button = tk.Button(self.upper_grid)
        self.app_title_button["text"] = "N.A.M.E"
        self.app_title_button["command"] = self.app_title_command
        self.app_title_button.grid(row=0, column=1)

    def init_lower_grid(self):
        """ Initialize the lower grid """
        
        self.lower_grid = tk.Frame(self.container)
        Grid.columnconfigure(self.lower_grid, 1, weight=1)

        self.lower_grid.grid(row=2, column=0, sticky="ew")

    def init_middle_grid(self):
        """ Initialize the middle grid """
        self.middle_grid = tk.Frame(self.container)
        Grid.columnconfigure(self.middle_grid, 0, weight=1)
        Grid.rowconfigure(self.middle_grid, 0, weight=1)

        self.middle_grid.grid(row=1, column=0, sticky="nsew")

    def switch_frame(self, name):
        """ switch to the given frame

        Args:
            name (string): pass the name of the desired frame to switch to
        """
        self.parent.switch_frame(
            self.parent.active_frame,
            self.parent.get_frame_id(name)
        )

    def app_title_command(self):
        self.switch_frame("Home Page")

    def login(self):
        """ Button command to link to a spotify account and if
            succesfull linked switch to the member frame 
            (frame_id = 2). Puts it in a thread so if they cancel the
            process online, our whole app doesn't freeze.
        """
        login = threading.Thread(target=self.login_thread, daemon=True)
        login.start()

    def login_thread(self):
        if self.user.link_spotify_account() is True:
            self.init_member_menu()
        else:
            print("error unsuccessfully linked spotify account")

    def log_out(self):
        """ Command for the logout button
        """
        # delete the cache file
        self.user.logout()
        self.init_guest_menu()
        # go back to the home frame
        self.switch_frame("Home Page")

    def group_menu_command(self, group):
        """ Command for clicking a group menu button
        """
        self.user.active_group = group
        self.switch_frame("Group Home")
        self.parent.frames[
            self.parent.get_frame_id("Group Home")
        ].display_group(group)

    def member_home_command(self):
        """ command for the member home member menu item
        """
        self.switch_frame("Member Home")

    def get_id_command(self):
        """ Command for the get shareable ID menu item
        """
        # Return the users spotify ID that they can share with other users to
        # form groups
        if self.user.is_member():
            message = self.user.get_account_id()
            # Display the returned ID in the following messagebox popup
            ShareableIdDialog(self.container, title="NAME", text=message)

    def start_single_search(self, title):
        """ Search the spotify API for the given song

        Args:
            title (str): the desired song title
            filters (dict): the selected filters
        """
        # BACKEND - single song search connection return a list of songs
        # do this in another thread
        self.api_search_results = self.query_object.search_single_song(title)
        if self.api_search_results != []:
            self.open_song_search_popup(self.api_search_results)
        else:
            self.no_songs_found_popup()

    def no_songs_found_popup(self):
        """ In the case that spotify can't find any songs for the
        title the user entered, display this popup window so that
        the gui doesn't break.
        """
        self.grab_set()
        popup = tk.Toplevel(self)
        popup.title("No results")

        label = tk.Label(
            popup,
            text="Sorry, Spotify couldn't find any songs with that title."
        )
        label.grid(row=0, column=0)

        button = ttk.Button(popup, text="Okay", command=popup.destroy)
        button.grid(row=1, column=0)
        self.grab_release()

    def open_song_search_popup(self, api_results):
        """ open a popup for the user to select the song they actually
            wanted to add to the list
        """
        self.grab_set()
        self.popup = tk.Toplevel(self)
        # remove windows borders and stuff with splash screen option
        self.popup.overrideredirect(1)
        self.popup.attributes("-topmost", 1)
        self.popup.protocol(
            "WM_DELETE_WINDOW",
            self.close_single_search_window
        )
        self.popup.title("Pick a Song")

        self.song_selection = StringVar(self.popup)
        self.song_selection_default = "Which song were you looking for?"
        self.song_selection.set(self.song_selection_default)  # default value

        songs = [song_result for song_result in api_results]
        formated_songs = []
        artists_string_list = []

        for song in songs:
            artists = [arts for arts in song.song_artist]
            for artist in artists:
                artists_string_list.append(artist.name)
            artists_string = ", ".join(artists_string_list)
            formated_songs.append(song.song_name + "  -  " + artists_string)
            artists_string_list.clear()

        self.song_select_dropdown = tk.OptionMenu(
            self.popup,
            self.song_selection,
            *formated_songs,
            command=self.song_select_dropdown_command)
        self.song_select_dropdown.pack()

        # update stuff first before getting widths
        self.update_idletasks()

        # find the location of the cursor
        x = self.winfo_pointerx() - (self.popup.winfo_width()/2)
        y = self.winfo_pointery() - (self.popup.winfo_height()/2)
        # open the popup window on the cursor
        self.popup.geometry('+%d+%d' % (x, y))

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


class ShareableIdDialog(simpledialog.Dialog):

    def __init__(self, parent, title=None, text=None):
        self.data = text
        simpledialog.Dialog.__init__(self, parent, title=title)

    def body(self, parent):
        self.lbl = tk.Label(
            self,
            text="Your Spotify ID (share with your friends): "
        )
        self.lbl.pack(side=tk.TOP)

        self.text = tk.Text(self, width=25, height=2)
        self.text.configure(state="normal")
        self.text.pack(fill="both", expand=False)

        self.text.insert("1.0", self.data)
        # make sure the user can't edit the textbox
        self.text.configure(state="disable")
        return self.text

    def buttonbox(self):
        self.copy = tk.Button(
            self,
            text="Copy to Clipboard",
            command=self.copy_command
        )
        self.copy.pack(side=tk.LEFT)

        self.close_button = tk.Button(self, text="Close", command=self.destroy)
        self.close_button.pack(side=tk.BOTTOM)

    def copy_command(self):
        self.clipboard_clear()
        self.clipboard_append(self.text.get("1.0", tk.END))

        self.update()
        self.destroy()
