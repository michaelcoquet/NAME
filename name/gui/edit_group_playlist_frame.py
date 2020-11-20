""" TODO: fill in
"""
import tkinter as tk

from .member_home_frame import MemberHomeFrame


class EditGroupPlaylistFrame(MemberHomeFrame):
    """ TODO: fill in

    Args:
        tk ([type]): TODO: fill in
    """
    def __init__(self, parent, container):
        super().__init__(parent, container)
        self.container = container
        self.parent = parent
