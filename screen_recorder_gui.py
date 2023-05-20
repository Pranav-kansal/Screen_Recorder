from tkinter import *
from tkinter import ttk
from PIL import ImageGrab
import numpy as np
import cv2
from win32api import GetSystemMetrics
from datetime import datetime
import threading
import dropbox

class Screen:
    def __init__(self):
        self.width = GetSystemMetrics(0)
        self.height = GetSystemMetrics(1)
        self.time_stamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.file_name = f'{self.time_stamp}.mp4'
        self.access_token = 'sl.Bezw7sb8H-IIlEMor35-RYwEdR7fdkYihWzY_BQ-zOoWDxZcTpoPxJHYCNN7B6M6fKoKkRZWjS7wcDFhj7G5Z9HkbIm9U7XTAEli3B-UHyaeKd4QjDlSDW5koqKIc-5Da7SYFv1d'  # Replace with your Dropbox access token

        self.fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        self.captured_video = cv2.VideoWriter(self.file_name, self.fourcc, 20.0, (self.width, self.height))
        self.status = True

    def stop(self):
        self.status = False
        self.upload_video()

    def start(self):
        while self.status:
            img = ImageGrab.grab(bbox=(0, 0, self.width, self.height))
            img_np = np.array(img)
            img_final = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
            self.captured_video.write(img_final)
            if cv2.waitKey(10) == ord('.'):
                break

    def upload_video(self):
        dbx = dropbox.Dropbox(self.access_token)
        with open(self.file_name, 'rb') as file:
            dbx.files_upload(file.read(), '/' + self.file_name)
            print(f'Video uploaded to Dropbox: {self.file_name}')

class ScreenRecorder:
    def __init__(self, root):
        self.screen = Screen()

        self.root = root
        self.root.geometry("605x160")
        self.root.title("Screen Recorder")
        self.root.config(bg="sky blue")
        self.root.iconbitmap(r'C:\Users\PRANAV KANSAL\Desktop\face recognition\logo_Xum_icon.ico')

        self.heading = Label(self.root, text="Screen Recorder", font=("new time romans", 14, "bold"), bg="sky blue", fg="purple")
        self.heading.config(width=58, height=5)
        self.heading.place(x=0, y=0)

        self.start_button = Button(self.root, text="START", bg="sky blue", fg="purple", command=self.start_recording)
        self.start_button.place(x=0, y=100, width=300, height=50)

        self.stop_button = Button(self.root, text="STOP", bg="sky blue", fg="purple", command=self.stop_recording)
        self.stop_button.place(x=305, y=100, width=300, height=50)

    def start_recording(self):
        self.screen.status = True
        threading.Thread(target=self.screen.start).start()

    def stop_recording(self):
        self.screen.stop()

if __name__ == '__main__':
    root = Tk()
    obj = ScreenRecorder(root)
    root.mainloop()

