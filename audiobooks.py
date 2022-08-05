import os
import time
from datetime import datetime
import shutil
from tkinter import ttk
import PyPDF2
from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog
import threading
from threading import Thread
from threading import *
import tkinter as tk
from tkinter import *
import pyttsx3
from logger_class import get_module_logger


bg='#808080'
# Creating TK Container
app = Tk()  # intialise tk

# Window Geometry
app.geometry('700x750')

# Title of the window
app.title('Personal Audiobook')

app.config(padx=50, pady=30, bg=bg)
path = None

logger = get_module_logger(__name__)

# Defining AudiobookClass
class Audiobook(tk.Frame,Thread):
    def __init__(self, master=None):
        # Defining Constructor
        super().__init__(master=master)

        self.master = master
        self.grid()


        frame = tk.Frame(app)
        frame.grid()
        self.progressbar = ttk.Progressbar(frame, orient=tk.HORIZONTAL,mode='indeterminate')
        self.progressbar.grid(row=1,column=3)


        self.image_canvas = tk.Canvas(width=300, height=320, bg=bg, highlightthickness=0)

        self.img = tk.PhotoImage(file='image/audioboooks2.png')

        self.image_canvas.create_image(140, 150, image=self.img)

        self.image_canvas.grid(row=3, column=2, pady=10)


        self.title = tk.Label(app, text="Let's listen to the book", font=('Courier', 20, 'bold'), bg=bg)
        self.title.grid(row=2, column=2, pady=10)

        self.open_PDF = tk.Button(app, text="Open", font=('Courier', 10, 'bold'), command=self.click, width=20, bg=bg)
        self.open_PDF.grid(row=4, column=2, pady=10)

        self.say_PDF = tk.Button(app, text="Talk", font=('Courier', 10, 'bold'), command=lambda:self.start_talk_thread(None),
                                 width=20, bg=bg)
        self.say_PDF.grid(row=5, column=2, pady=10)



        self.stop_PDF = tk.Button(app, text="Stop", font=('Courier', 10, 'bold'),command=lambda: self.start_stop_thread(None),
                                  width=20, bg=bg)
        self.stop_PDF.grid(row=7, column=2, pady=15)

        self.message_label = tk.Label(text="Click on talk button and wait for few seconds :)",font=('Courier', 10, 'bold'),
                                      wraplength=300, bg=bg)
        self.message_label.grid(row=8, column=2)

    # Defining Click Function
    def click(self):

        # To extract text from chosen PDF file

        try:
            global path
            # we can choose any file we want
            path = filedialog.askopenfilename()
            print(path)
            logger.info('Processing done for pdf file ')
        except Exception as e:
            raise Exception("(feedback) - Something went wrong while opening a pdf file.\n" + str(e))

    # Defining Talk Function
    def talk(self):
          # function  to speak the pdf text
          try:
              if path:
                  # init the speaker

                  speaker = pyttsx3.init()

                  # open the pdf

                  book = open(path, 'rb')

                  # read the pdf

                  read_file = PyPDF2.PdfFileReader(book)

                  num_pages = read_file.numPages

                 # extract the text from the page

              for num in range(num_pages):
                     page = read_file.getPage(num)
                     text = page.extractText()

                      # speaker.say(text)
                     speaker.save_to_file(text, 'speech.mp3')  ## Saving Text In a audio file 'speech.mp3'

                     speaker.say(text)
                     speaker.runAndWait()
              logger.info('Processing done for pdf file and it is coverted into audio file')
              time.sleep(5)

          except Exception as e:
                    raise Exception("(feedback) - Something went wrong on while reading.\n" + str(e))


    def start_talk_thread(self,event):

            global talk_thread

            talk_thread = threading.Thread(target=self.talk)
            talk_thread.daemon = True
            self.progressbar.start()
            talk_thread.start()
            app.after(20, self.check_talk_thread)
            logger.info("Thread run completed")

    def check_talk_thread(self):
        if talk_thread.is_alive():
            app.after(20, self.check_talk_thread)
        else:
            self.progressbar.stop()


    def stop(self):

        app.destroy()
        time.sleep(5)
        logger.info('audio file is stop ')


    def start_stop_thread(self,event):
        global stop_thread

        stop_thread = threading.Thread(target=self.stop)
        stop_thread.daemon = True
        self.progressbar.start()
        stop_thread.start()
        app.after(20, self.check_stop_thread)
        logger.info("Thread run completed")

    def check_stop_thread(self):
        if stop_thread.is_alive():
            app.after(20, self.check_stop_thread)
        else:
            self.progressbar.stop()



if __name__ == '__main__':

    root = Audiobook(master=app)

    root.mainloop()

