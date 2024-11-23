import os
import tkinter as tk
from tkinter import filedialog, Listbox, SINGLE
import pygame
from pygame import mixer

class SimpleMusicPlayer:
    def __init__(self, master):
        self.master = master
        self.master.title("Simple Music Player")
        self.master.geometry("600x600")

        # Initialize Pygame mixer
        pygame.init()
        mixer.init()
        pygame.mixer.music.set_endevent(pygame.USEREVENT)

        self.current_index = 0
        self.is_paused = False
        self.song_list = []

        # GUI Components
        self.select_folder_button = tk.Button(master, text="Select Folder", command=self.load_folder)
        self.select_folder_button.pack(pady=10)

        self.song_listbox = Listbox(master, selectmode=SINGLE, width=50)
        self.song_listbox.pack(pady=10)
        self.song_listbox.bind("<Double-Button-1>", self.play_selected_song)

        self.play_button = tk.Button(master, text="Play", command=self.play_song)
        self.play_button.pack(pady=5)

        self.pause_button = tk.Button(master, text="Pause", command=self.pause_song)
        self.pause_button.pack(pady=5)

        self.stop_button = tk.Button(master, text="Stop", command=self.stop_song)
        self.stop_button.pack(pady=5)

        self.next_button = tk.Button(master, text="Next", command=self.next_song)
        self.next_button.pack(pady=5)

        self.prev_button = tk.Button(master, text="Previous", command=self.previous_song)
        self.prev_button.pack(pady=5)

        self.master.bind("<space>", self.pause_song)
        self.master.bind("<Escape>", self.stop_song)

        self.check_song_end()

    def load_folder(self):
        selected_folder = filedialog.askdirectory()
        if selected_folder:
            self.song_list = [os.path.join(selected_folder, f) for f in os.listdir(selected_folder) if f.endswith('.mp3')]
            self.song_list.sort()
            self.current_index = 0
            self.update_playlist_display()

    def update_playlist_display(self):
        self.song_listbox.delete(0, tk.END)
        for song in self.song_list:
            self.song_listbox.insert(tk.END, os.path.basename(song))
        if self.song_list:
            self.song_listbox.select_set(self.current_index)

    def play_selected_song(self, event):
        selected_index = self.song_listbox.curselection()
        if selected_index:
            self.current_index = selected_index[0]
            self.play_song()

    def play_song(self):
        if not self.song_list:
            return
        mixer.music.load(self.song_list[self.current_index])
        mixer.music.play()
        self.is_paused = False
        self.update_playlist_display()

    def pause_song(self, event=None):
        if not self.song_list:
            return
        if not self.is_paused:
            mixer.music.pause()
            self.is_paused = True
        else:
            mixer.music.unpause()
            self.is_paused = False

    def stop_song(self, event=None):
        if not self.song_list:
            return
        mixer.music.stop()
        self.is_paused = False
        print("Music stopped")
        self.master.destroy()

    def next_song(self):
        if not self.song_list:
            return
        self.current_index = (self.current_index + 1) % len(self.song_list)
        self.play_song()

    def previous_song(self):
        if not self.song_list:
            return
        self.current_index = (self.current_index - 1) % len(self.song_list)
        self.play_song()

    def check_song_end(self):
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                self.next_song()
        self.master.after(1000, self.check_song_end)  # Check every second

    def run(self):
        self.master.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleMusicPlayer(root)
    app.run()
