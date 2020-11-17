""" TODO: fill in
"""
import tkinter as tk
from tkinter import Grid


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
        self.init_menu()

    def init_menu(self):
        """ make the default menu for guest users
        """
        self.guest_menu = tk.Menu(self.parent)
        self.guest_menu.add_command(label="Login", command=self.container.login)
        self.container.config(menu=self.guest_menu)

    def init_upper_grid(self):
        """ TODO: fill in
        """
        self.upper_grid = tk.Frame(self.parent)
        self.upper_grid.grid(row=0, column=0, sticky="nw")

        # could put an image logo here if desired, for now just a label
        self.app_title = tk.Label(self.upper_grid)
        self.app_title["text"] = "N.A.M.E"
        self.app_title.grid(row=0, column=1)

    def init_lower_grid(self):
        """ TODO: fill in
        """
        # self.search_alert_window = SearchProgressFrame(self.container, self)
        self.lower_grid = tk.Frame(self.parent)
        Grid.columnconfigure(self.lower_grid, 1, weight=1)

        self.lower_grid.grid(row=2, column=0, sticky="ew")

    def init_middle_grid(self):
        """ TODO: fill in
        """
        self.middle_grid = tk.Frame(self.parent)
        Grid.columnconfigure(self.middle_grid, 0, weight=1)
        Grid.rowconfigure(self.middle_grid, 0, weight=1)

        self.middle_grid.grid(row=1, column=0, sticky="nsew")
