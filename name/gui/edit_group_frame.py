"""CMPT 370 Group 5 Project: NAME (Nearly Analogous Music Engine)
    Credits: Michael Coquet
             Elizabeth Reid
             Ben Camplin
             Laurence Craig Garcia
             Sean Warren
"""
import tkinter as tk
from tkinter import ttk

from .group_home_frame import GroupHomeFrame
from name.backend_classes.group import Group


class EditGroupFrame(GroupHomeFrame):
    """ This frame is used for the owner of a group to edit the group members and name of the
        group
    Args:
        tk (Frame): inherited from the main group home page
    """

    def grid_unmap(self):
        super().grid_unmap()
        self.cancel_button.grid_remove()
        self.create_group_button.grid_remove()
        self.delete_button.grid_remove()
        self.delete_all_button.grid_remove()
        self.add_friend_button.grid_remove()
        self.member_listbox.grid_remove()
        self.member_list_label.grid_remove()
        self.group_name_entry.grid_remove()

    def grid_remember(self):
        super().grid_remember()
        self.add_friend_button.grid_remove()
        self.save_playlist_button.grid_remove()
        self.edit_group_button.grid_remove()
        self.l_playlist_select.grid_remove()
        self.playlist_dropdown.grid_remove()
        self.new_playlist_button.grid_remove()

        self.cancel_button.grid()
        self.create_group_button.grid()
        self.delete_button.grid()
        self.delete_all_button.grid()
        self.add_friend_button.grid()
        self.member_listbox.grid()
        self.member_list_label.grid()
        self.group_name_entry.grid()

    def __init__(self, parent, container, user):
        super().__init__(parent, container, user)
        self.invite_id_list = []
        self.max_members = 20

    def init_lower_grid(self):
        super().init_lower_grid()
        self.edit_playlist_button.grid_remove()
        self.save_playlist_button.grid_remove()

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

        self.delete_button = tk.Button(
            self.f_container,
            text="Delete",
            command=self.delete_command
        )
        self.delete_button.grid(row=0, column=0)

        self.delete_all_button = tk.Button(
            self.f_container,
            text="Delete All",
            command=self.delete_all_command
        )
        self.delete_all_button.grid(row=0, column=1)

        self.friend_id_entry = tk.Entry(self.f_container)
        self.friend_id_entry.grid(row=0,column=2)

        self.add_friend_button = tk.Button(
            self.f_container,
            text="Add Friend",
            command=self.add_friend_command
        )
        self.add_friend_button.grid(row=0,column=3)

    def init_middle_grid(self):
        super().init_middle_grid()
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
        self.member_list_label = tk.Label(self.upper_grid, text="Member List")
        self.member_list_label.grid(row=2,column=0)

    def cancel_command(self):
        """command for the cancel button
        """
        # go back to previously active_frame
        self.parent.switch_to_previous_frame()

    def save_group_command(self):
        """command for the create group button
        """
        self.init_member_menu()
        group_name = self.group_name_entry.get()
        self.group_menu.add_command(label=group_name)

        group = Group(group_name, self.user.spotify_id, self.invite_id_list, [])
        # add this new group details to the persisiten storage
        if self.user.create_group(group):
            self.switch_frame("Group Home")
        else:
            tk.messagebox.showerror(title="Error", message="This group already exists")

    def add_friend_command(self):
        """command for the add friend button
        """
        friend_id = self.friend_id_entry.get()
        if friend_id != "":
            if len(self.invite_id_list) == 0:
                self.add_member_to_lists()
            elif len(self.invite_id_list) >= self.max_members:
                tk.messagebox.showerror(title="Error", message="Sorry the group is full")
            else:
                if self.member_exists(friend_id):
                    tk.messagebox.showerror(title="Error", message="Friend already added")
                else:
                    self.add_member_to_lists()
        else:
            tk.messagebox.showerror(title="Error",
                                    message="Please enter your friends spotify id")

    def member_exists(self, friend_id):
        """ check if the member already exists in the list
        """
        for friend in self.invite_id_list:
            if friend == friend_id:
                return True

        return False

    def add_member_to_lists(self):
        """ add the given friend to the listbox and the internal member list
        """
        # add the friends id to the group member id list
        self.invite_id_list.append(self.friend_id_entry.get())
        self.member_listbox.insert("end", self.friend_id_entry.get())

    def delete_all_command(self):
        """command for the delete all button
        """
        self.invite_id_list.clear()
        self.member_listbox.delete(0, "end")

    def delete_command(self):
        """command for the delete all button
        """
        selected = self.member_listbox.selection_get()
        for member in self.invite_id_list:
            for item in selected:
                if item == member:
                    self.invite_id_list.remove(member)
        self.member_listbox.delete(tk.ANCHOR)

    def display_group(self, group):
        """[summary]
        """
        # would like to be able to get these spotify ids back as usernames or something nicer
        for member in group.member_list:
            msg = member + "\t\t"
            if member == self.user.spotify_id:
                msg = msg + "(Me)"
            if member == group.owner_id:
                msg = msg + "(Group Owner)"

            self.member_listbox.insert("end", msg)

        # now load the groups playlists into the dropdown

