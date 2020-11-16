"""CMPT 370 Group 5 Project: NAME
    Summary: TODO: fill in summary of app
"""
import tkinter as tk
from tkinter import Grid
from gui import HomePage

class Name(tk.Tk):
    """TODO: fill out docstring -- basically the gui wrapper
       TODO: set up a finite state machine to flip between frames in a more controlled fashion

    Args:
        tk ([type]): [description]
    """
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Nearly Analagous Music Engine")
        self.iconbitmap("resources\\ravencon.ico")
        Grid.rowconfigure(self, 0, weight=1)
        Grid.columnconfigure(self, 0, weight=1)

        # container frame
        container = tk.Frame(self)
        container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # instantiate frame array
        self.frames = {}

        # instantiate the home frame
        self.frames[HomePage] = HomePage(container, self)

def main():
    """ main entry point
    """
    app = Name()
    app.mainloop()

if __name__ == "__main__":
    main()
