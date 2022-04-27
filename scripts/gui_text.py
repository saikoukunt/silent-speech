import tkinter as tk
from tkinter import ttk
from gtts import gTTS
from playsound import playsound
import os

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.geometry(f'{width}x{height}') 
        self.resizable(False, False)

        self.word = ""
        self.prev_word = ""
        self.prev_2 = ""

        self.word_l = ttk.Label(
            self, 
            text=f'{self.word}', 
            font=("Helvetica Neue Thin", 150),
            foreground='black'
        )
        
        self.prev_word_l = ttk.Label(
            self,
            text=f'{self.prev_word}',
            font=("Helvetica Neue Thin", 100),
            foreground='#888888'
        )
        self.prev_2_l = ttk.Label(
            self,
            text=f'{self.prev_2}',
            font=("Helvetica Neue Thin", 66),
            foreground='#dddddd'
        )

    def run(self, input):
        while True:
            if not input.empty():
                self.prev_2 = self.prev_word
                self.prev_word = self.word
                self.word = input.get()

                self.word_l.configure(text="{self.word}")
                self.prev_word_l.configure(text="{self.prev_word}")
                self.prev_2_l.configure(text="{self.prev_2}")

                speech = gTTS(text=self.word, lang='en', slow=False)
                speech.save("audio.mp3")
                playsound("audio.mp3")



