"""The home screen for the app
"""
import time
import tkinter as tk
from tkinter import ttk
from tkinter import StringVar
from tkinter import Grid
from tkinter import messagebox


class HomePage(tk.Frame):
    """ Could possibly be a splash screen but for now this is the home page screen

    Args:
        tk (Frame): parent frame (root in this case)
    """
    max_songs = 6
    # pylint: disable=too-many-instance-attributes
    # theres going to be lots of instance attributes for this class

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.win = None
        self.home_frame = None
        self.progress = None
        self.l_songs_found = None
        self.signed_in = 0
        self.init_member_menu()
        self.init_guest_menu()
        self.init_widgets()

    def init_member_menu(self):
        """ make the menu for when a user links their spotify account
        """
        self.member_menu = tk.Menu(self.master)

        self.my_account_menu = tk.Menu(self.member_menu, tearoff=0)
        self.my_account_menu.add_command(label="Member Home")
        self.my_account_menu.add_separator()

        # make a submenu for groups
        self.group_menu = tk.Menu(self.my_account_menu, tearoff=0)
        self.group_menu.add_command(label="Create Group", command=self.create_group)
        self.group_menu.add_separator()
        self.my_account_menu.add_cascade(label="Groups", menu=self.group_menu)
        self.my_account_menu.add_command(label="Get Shareable ID")
        self.my_account_menu.add_separator()

        self.my_account_menu.add_command(label="Log Out")

        #add menu with submenu to the main menu
        self.member_menu.add_cascade(label="My Account", underline=0, menu=self.my_account_menu)

    def init_guest_menu(self):
        """ make the default menu for guest users
        """
        self.guest_menu = tk.Menu(self.master)
        self.guest_menu.add_command(label="Login", command=self.login)
        self.master.config(menu=self.guest_menu)

    def init_widgets(self):
        """ create the home page widgets
        """
        #make home frame
        self.home_frame = tk.Frame(self.master)
        self.home_frame.grid(row=0, column=0, sticky="nsew")
        self.home_frame.tkraise()

        upper_menu = tk.Frame(self.home_frame)
        upper_menu.grid(row=0, column=0, sticky="ew")
        lower_menu = tk.Frame(self.home_frame)
        lower_menu.grid(row=2, column=0, sticky="ew")

        #set up grid
        Grid.columnconfigure(self.home_frame, 0, weight=1)
        Grid.rowconfigure(self.home_frame, 1, weight=1)
        Grid.columnconfigure(lower_menu, 1, weight=1)

        self.grid(padx="10", pady="10")

        # could put an image logo here if desired, for now just a label
        self.app_title = tk.Label(upper_menu)
        self.app_title["text"] = "N.A.M.E"
        self.app_title.grid(row=0, column=1)

        self.create_playlist = tk.Button(upper_menu)
        self.create_playlist["text"] = "Create Playlist"
        self.create_playlist.grid(row=1, column=0)
        self.create_playlist["state"] = tk.DISABLED

        self.compare_songs_button = tk.Button(upper_menu, command=self.compare_songs)
        self.compare_songs_button["text"] = "Compare Songs"
        self.compare_songs_button.grid(row=1, column=1)

        self.get_song_info = tk.Button(upper_menu)
        self.get_song_info["text"] = "Get Song Info"
        self.get_song_info.grid(row=1, column=2)

        self.song_sim_score_label = tk.Label(upper_menu)

        # TODO: add the proper filters to the dropdown list
        variable = StringVar(upper_menu)
        variable.set("Filters") # default value
        self.filters_dropdown = tk.OptionMenu(upper_menu, variable, "one", "two", "three",
                                                    command=self.filter_function)
        self.filters_dropdown.grid(row=2, column=0)

        self.song_search = tk.Entry(upper_menu)
        self.song_search.insert(0, "Song title")
        self.song_search.grid(row=2, column=1)

        # TODO: connect with backend song search function
        self.song_search_button = tk.Button(upper_menu)
        self.song_search_button["text"] = "Search"
        self.song_search_button.grid(row=2, column=2)

        self.song_listbox = tk.Listbox(self.home_frame)
        self.song_listbox.grid(row=1, column=0, sticky="nsew")

        self.remove_all_button = tk.Button(lower_menu, command=self.rem_all_alert)
        self.remove_all_button["text"] = "Remove all"
        self.remove_all_button.grid(row=0, column=0)

        self.start_over_button = tk.Button(lower_menu, command=self.start_over)
        self.start_over_button["text"] = "Start Over"

        self.get_stats_button = tk.Button(lower_menu, text="Get Stats", command=self.get_stats)
        self.get_stats_button.grid(row=0, column=2)

        self.create_similarity_playlist = tk.Button(lower_menu,
            text="Find Similar Songs", command=self.open_sim_progress)
        self.create_similarity_playlist.grid(row=0, column=2)


    def open_sim_progress(self):
        """open a new window that updates the user on the progress of similarity playlist
           creation
        """
        self.grab_set()

        self.win = tk.Toplevel(self)
        self.win.protocol("WM_DELETE_WINDOW", self.close_window)

        self.win.title("Searching")

        l_1 = tk.Label(self.win, text="Finding Similar Songs!")
        l_1.pack(side=tk.TOP)

        self.l_songs_found = tk.Label(self.win, text="Songs found...   0/" \
                                            + str(self.max_songs))
        self.l_songs_found.pack(side=tk.TOP)

        self.progress = ttk.Progressbar(self.win, orient=tk.HORIZONTAL, length=200,
            mode="determinate")

        self.progress.pack(pady=10)

        cancel_btn = tk.Button(self.win, text="Cancel", command=self.close_window)
        cancel_btn.pack(side=tk.BOTTOM)

        self.search_update()

    def search_update(self):
        """ TODO: link this with the search function in a way that it can be updated likely will
                  require multithreading to avoid the app hanging during search, possibly fork()

                  for now just do a little simulation, notice the hang with time.sleep
        """
        count = 0
        self.progress.update()
        self.progress["maximum"] = 100
        time.sleep(1)

        self.progress['value'] = 20
        count = count + 1
        self.l_songs_found["text"] = "Songs found...   " + str(count) + "/" \
                                        + str(self.max_songs)
        self.progress.update()
        time.sleep(1)

        self.progress['value'] = 40
        count = count + 1
        self.l_songs_found["text"] = "Songs found...   " + str(count) + "/" \
                                        + str(self.max_songs)
        self.progress.update()
        time.sleep(1)

        self.progress['value'] = 50
        count = count + 1
        self.l_songs_found["text"] = "Songs found...   " + str(count) + "/" \
                                        + str(self.max_songs)
        self.progress.update()
        time.sleep(1)

        self.progress['value'] = 60
        count = count + 1
        self.l_songs_found["text"] = "Songs found...   " + str(count) + "/" \
                                        + str(self.max_songs)
        self.progress.update()
        time.sleep(1)

        self.progress['value'] = 80
        count = count + 1
        self.l_songs_found["text"] = "Songs found...   " + str(count) + "/" \
                                        + str(self.max_songs)
        self.progress.update()
        time.sleep(1)

        self.progress['value'] = 100
        count = count + 1
        self.l_songs_found["text"] = "Songs found...   " + str(count) + "/" \
                                        + str(self.max_songs)
        self.progress.update()
        time.sleep(1)

    def switch_frame(self, frame_id):
        """ Change the home frame to the given frame

        Args:
            frame_id (integer): give a frame_id which will correspond to a specific frame to be
                               displayed in place of the home frame
        """
        if frame_id == 0:
            # frame_id[0] = Compare Songs set up the frame for comparing two or more songs
            self.song_search.delete(0, 20)
            self.song_search.insert(0, "two or more songs")
            self.create_similarity_playlist.grid_forget()
            self.get_stats_button.grid(row=0, column=2)
            self.compare_songs_button["state"] = tk.DISABLED
            self.create_playlist["state"] = tk.NORMAL
            self.start_over_button.grid_forget()
            self.remove_all_button.grid(row=0, column=0)
            self.song_sim_score_label.grid_forget()
            self.filters_dropdown.grid(row=2, column=0)
            self.song_search.grid(row=2, column=1)
            self.song_search_button.grid(row=2, column=2)
        elif frame_id == 1:
            # frame_id[1] = get stats frame for displaying similarity comparison of two or more
            #               songs
            self.remove_all_button.grid_forget()
            self.start_over_button.grid(row=0, column=0)
            self.get_stats_button.grid_forget()
            self.filters_dropdown.grid_forget()
            self.song_search_button.grid_forget()
            self.song_search.grid_forget()
            self.song_sim_score_label["text"] = "These songs are X% similar"
            self.song_sim_score_label.grid(row=2, column=0, columnspan=3)
        elif frame_id == 2:
            # frame_id[2] = member frame, this is for when a guest has successfully linked their
            #               spotify account

            # many things change here, first change the dropdown menu
            self.master.config(menu=self.member_menu)
        else:
            print("error")

    def compare_songs(self):
        """ button command to go to song comparison frame
        """
        self.switch_frame(0)

    def get_stats(self):
        """ button command to get the comparison info for the selected songs
            TODO: link this to the song comparison function for now do nothing
        """
        self.switch_frame(1)

    def start_over(self):
        """ button to reset the compare selected songs frame
        """
        self.switch_frame(0)

    def login(self):
        """ Button command to link to a spotify account and if succesfully linked switch to the
            member frame (frame_id = 2).
            TODO: this is where the connection to the backend login function should check
                  if the user successuflly linked their spotify account
        """
        self.signed_in = 1 # TODO: change this with a real check
        if self.signed_in:
            print("successfully logged into spotify")
            self.switch_frame(2)
        else:
            print("error unsuccessfully linked spotify account")

    def create_group(self):
        """ Menu option to create a new group
            TODO: backend connection required here to create a new group, for now just assume
                  the user sucessfully created a new group and add a new menu option as in the
                  storyboards
        """
        self.group_menu.add_command(label="new group name") # TODO: make a real test and connect

    @staticmethod #remove later
    def rem_all_alert():
        """ Remove all songs from the working list if the user agrees
            TODO: add logic to clear the list, for now just return the users boolean response
        """
        msg = "Would you like to remove all songs in the list?"
        return bool(messagebox.askyesno("Remove All", msg))

    @staticmethod #remove later
    def filter_function():
        """ Filters available for the user to search with
            TODO: link the users choice of filter with the search function for now just return
                  anything
        """
        return 1

    def close_window(self):
        """override window closing event
        """
        self.progress.destroy()
        self.win.destroy()
        self.grab_release()
