"""CMPT 370 Group 5 Project: NAME (Nearly Analogous Music Engine)
    Credits: Michael Coquet
             Elizabeth Reid
             Ben Camplin
             Laurence Craig Garcia
             Sean Warren
"""
import tkinter as tk
from tkinter import StringVar

from .member_home_frame import MemberHomeFrame
from name.backend_classes.persistent_storage import PersistentStorage


class SavePlaylistFrame(MemberHomeFrame):
    """ Help a user save a playlist to eithe rtheir group or their spotify account

    Args:
        tk (Frame): inherits Member home page
    """

    def grid_unmap(self):
        super().grid_unmap()
        self.new_list_entry.grid_remove()
        self.cancel_button.grid_remove()
        self.save_playlist_button.grid_remove()

    def grid_remember(self):
        super().grid_remember()
        self.get_song_info_button.grid_remove()
        self.latest_playlist_button.grid_remove()
        self.all_playlists_button.grid_remove()
        self.listening_habits_button.grid_remove()

        self.new_list_entry.grid()
        self.cancel_button.grid()
        self.save_playlist_button.grid()
        self.song_treeview.grid()

    def init_lower_grid(self):
        super().init_lower_grid()

        self.cancel_button = tk.Button(
            self.lower_grid,
            text="Cancel",
            command=self.cancel_command)
        self.cancel_button.grid(row=0, column=0)

        container = tk.Frame(self.lower_grid)
        container.grid(row=0, column=2)

        self.new_list_entry = tk.Entry(container)
        self.new_list_entry.insert(0, "New Playlist Name")
        self.new_list_entry.grid(row=0, column=0)

        self.save_playlist_button = tk.Button(
            container,
            text="Save",
            command=self.save_playlist_command)
        self.save_playlist_button.grid(row=0, column=1)

    def cancel_command(self):
        """command for the cancel button
        """
        self.parent.switch_to_previous_frame()

    def save_playlist_command(self):
        """command for the save playlist button
        """
        if self.new_list_entry.get() != "New Playlist Name":
            if self.parent.previous_frame == self.parent.get_frame_id("Member Home"):
                # assemble a playlist object
                json_plylst = {
                    "name": self.new_list_entry.get(),
                    "owner": { "id": self.user.spotify_id },
                    "id": self.user.spotify_id,
                    "tracks": { "total": len(self.parent.song_object_list)}
                }
                if self.user.save_playlist_to_spotify(json_plylst, self.parent.song_object_list) is not None:
                    tk.messagebox.showinfo(title="Success", message="The playlist was saved to " +
                        "your spotify account")
                    self.parent.switch_to_previous_frame
                else:
                    print("error")
            else:
                storage = PersistentStorage(self.user.spotify_id)
                storage.save_group_playlist(
                    group_id=self.user.active_group.group_id,
                    group_name=self.user.active_group.group_name,
                    playlist_tracks=self.parent.song_object_list,
                    playlist_name=self.new_list_entry.get()
                )
                tk.messagebox.showinfo(title="Success", message="The playlist was saved to " +
                        "your group account")
                self.parent.switch_frame(self.parent.active_frame, self.parent.active_frame)
