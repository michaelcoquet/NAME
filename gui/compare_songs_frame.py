""" Compare Songs Frame
"""
import tkinter as tk


class CompareSongs(tk.Frame):
    """ Compare songs frame corresponding to storyboard pg. 2
        not a new window will replace the home frame on the home screen (confusing I know)

    Args:
        tk (Frame): parent frame
    """

    def __init__(self, master):
        super().__init__(master)
