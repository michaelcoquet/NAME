"""CMPT 370 Group 5 Project: NAME
    Summary: TODO: fill in summary of app
"""
import tkinter as tk
from tkinter import Grid
from gui import HomePage

def main():
    """ main entry point
    """
    #Create & Configure root
    root = tk.Tk()
    root.title("Nearly Analagous Music Engine")
    root.iconbitmap("resources\\ravencon.ico")
    Grid.rowconfigure(root, 0, weight=1)
    Grid.columnconfigure(root, 0, weight=1)

    #Create & Configure frame
    app = HomePage(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()
