import tkinter as tk
from tkinter import filedialog
import glob
from moviepy.editor import VideoFileClip
import pyglet
import multiprocessing

class VideoPlayer:
    def __init__(self, master):
        self.master = master
        self.video_list = []
        self.current_video = 0
        self.is_playing = False

        self.select_button = tk.Button(self.master, text="Select Root Folder", command=self.select_folder)
        self.play_button = tk.Button(self.master, text="Play", command=self.play_pause_video)
        self.next_button = tk.Button(self.master, text="Next", command=self.next_video)
        self.prev_button = tk.Button(self.master, text="Previous", command=self.previous_video)
        
        self.select_button.grid(row=0, column=0, padx=5, pady=5)
        self.play_button.grid(row=0, column=1, padx=5, pady=5)
        self.next_button.grid(row=0, column=2, padx=5, pady=5)
        self.prev_button.grid(row=0, column=3, padx=5, pady=5)

        self.video_player = tk.Label(self.master)
        self.video_player.grid(row=1, column=0, columnspan=5, padx=5, pady=5)

    def select_folder(self):
        folder_path = filedialog.askdirectory(title="Select Root Folder")
        if folder_path:
            self.video_list = glob.glob(folder_path + '/**/*.mp4', recursive=True)
            self.current_video = 0
            self.load_video()

    def next_video(self):
        if self.current_video < len(self.video_list) - 1:
            self.current_video += 1
            self.load_video()

    def previous_video(self):
        if self.current_video > 0:
            self.current_video -= 1
            self.load_video()

    def play_pause_video(self):
        if self.is_playing:
            self.pause_video()
        else:
            self.play_video()

    def play_video(self):
        if self.video_clip is not None and not self.is_playing:
            self.is_playing = True
            self.process = multiprocessing.Process(target=self.play_audio, args=(self.video_clip.reader.filename,))
            self.process.start()
            self.update_video_frames()

    def pause_video(self):
        if self.video_clip is not None and self.is_playing:
            self.is_playing = False
            self.process.terminate()

    def load_video(self):
        if self.current_video < len(self.video_list):
            video_path = self.video_list[self.current_video]
            self.video_clip = VideoFileClip(video_path)
            self.is_playing = False
            self.video_player.configure(text=f"Playing: {video_path}")
            self.video_player.update()

    def play_audio(self, audio_path):
        audio_player = pyglet.media.Player()
        audio_player.queue(pyglet.media.load(audio_path))
        audio_player.play()
        pyglet.app.run()

    def update_video_frames(self):
        if self.is_playing and self.current_video < len(self.video_list):
            frame = self.video_clip.get_frame(self.video_clip.duration * self.video_player.winfo_width() / self.video_clip.w)
            frame_image = tk.PhotoImage(format="RGBA", data=frame.tobytes())
            self.video_player.configure(image=frame_image)
            self.video_player.image = frame_image
            self.master.after(30, self.update_video_frames)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Video Player")
    player = VideoPlayer(root)
    root.mainloop()
