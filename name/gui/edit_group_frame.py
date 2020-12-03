""" TODO: fill in
"""
import tkinter as tk
from tkinter import ttk

from .group_home_frame import GroupHomeFrame
from name.backend_classes.group import Group


class EditGroupFrame(GroupHomeFrame):
    """ TODO: fill in

    Args:
        tk ([type]): TODO: fill in
    """

    def init_lower_grid(self):
        super().init_lower_grid()
        self.edit_playlist_button.grid_forget()
        self.save_playlist_button.grid_forget()

        self.cancel_button = tk.Button(
            self.lower_grid,
            text="Cancel",
            command=self.cancel_command
        )
        self.cancel_button.grid(row=1, column=0, sticky="w")

        self.create_group_button = tk.Button(
            self.lower_grid,
            text="Save Group",
            command=self.save_group_command
        )
        self.create_group_button.grid(row=1, column=2)

        self.f_container = tk.Frame(self.lower_grid)
        self.f_container.grid(row=0, column=0)

        self.delete_all_button = tk.Button(
            self.f_container,
            text="Delete All",
            command=self.delete_all_command
        )
        self.delete_all_button.grid(row=0, column=0)

        self.friend_id_entry = tk.Entry(self.f_container)
        self.friend_id_entry.grid(row=0,column=1)

        self.add_friend_button = tk.Button(
            self.f_container,
            text="Add Friend",
            command=self.add_friend_command
        )
        self.add_friend_button.grid(row=0,column=2)

    def init_middle_grid(self):
        super().init_middle_grid()
        self.song_listbox.grid_forget()
        self.playlist_dropdown.grid_forget()
        self.new_playlist_button.grid_forget()
        self.group_song_stats_button.grid_forget()
        self.edit_group_button.grid_forget()
        self.list_1_label.grid_forget()

        f_container = tk.Frame(self.middle_grid)
        f_container.grid(row=0, column=1, sticky="n")

        self.member_listbox = tk.Listbox(self.middle_grid)
        self.member_listbox.grid(row=0, column=0, sticky="nsew")

        l1 = tk.Label(f_container, text="Group:")
        l1.grid(row=0, column=1, sticky="nw")
        self.group_name_entry = tk.Entry(f_container)
        self.group_name_entry.insert(0, "Group Name")
        self.group_name_entry.grid(row=0,column=2, sticky="nw")

    def init_upper_grid(self):
        super().init_upper_grid()
        self.list_1_label.grid_forget()
        self.member_list_label = tk.Label(self.upper_grid, text="Member List")
        self.member_list_label.grid(row=2,column=0)

    def cancel_command(self):
        """command for the cancel button
        """
        return 1

    def save_group_command(self):
        """command for the create group button
        """
        self.init_member_menu()
        group_name = self.group_name_entry.get()
        self.group_menu.add_command(label=group_name)
        member_list = [ "asdfasdfasdfasdff", "testing", "TODO", "change", "This"]

        group = Group(group_name, self.user.spotify_id, member_list)
        # add this new group details to the persisiten storage
        if self.user.create_group(group):
            self.switch_frame("Group Home")
        else:
            tk.messagebox.showerror(title="Error", message="This group already exists")

    def add_friend_command(self):
        """command for the add friend button
        """
        return 1

    def delete_all_command(self):
        """command for the delete all button
        """
        return 1
