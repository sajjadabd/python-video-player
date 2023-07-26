from tkinter import *
from tkinter.filedialog import askopenfile
from tkVideoPlayer import TkinterVideo
import pyglet
import multiprocessing

# create box
window = Tk()
# title of the box, not the text in the box
window.title("Tkinter Play Videos in Video Player")
window.geometry("700x450")
window.configure(bg="white")

filename = None

def open_file():
    file = askopenfile(mode='r', filetypes=[('Video Files', ["*.mp4"])])
    if file is not None:
        global filename
        filename = file.name
        videoplayer.load(r"{}".format(filename))
        play_video_with_audio()
        videoplayer.play()

def play_audio(audio_path):
    audio_player = pyglet.media.Player()
    audio_player.queue(pyglet.media.load(audio_path))
    audio_player.play()
    pyglet.app.run()

def playAgain():
    if filename:
        videoplayer.play()

def StopVideo():
    if filename:
        videoplayer.stop()

def PauseVideo():
    if filename:
        videoplayer.pause()

def play_video_with_audio():
    if filename:
        # Create a separate process for audio playback
        print(filename)
        audio_process = multiprocessing.Process(target=play_audio, args=(filename.replace("mp4" , "mp3"),))
        audio_process.start()
        

openbtn = Button(window, text='Open', command=lambda: open_file())
openbtn.grid(row=0, column=0, padx=5, pady=5)

playbtn = Button(window, text='Play Video', command=play_video_with_audio)
playbtn.grid(row=0, column=1, padx=5, pady=5)

stopbtn = Button(window, text='Stop Video', command=StopVideo)
stopbtn.grid(row=0, column=2, padx=5, pady=5)

pausebtn = Button(window, text='Pause Video', command=PauseVideo)
pausebtn.grid(row=0, column=3, padx=5, pady=5)

videoplayer = TkinterVideo(master=window, scaled=True)
videoplayer.grid(row=1, column=0, columnspan=5, padx=5, pady=5)

window.mainloop()
