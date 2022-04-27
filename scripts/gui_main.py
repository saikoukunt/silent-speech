from multiprocessing import Process, Queue
from turtle import bgcolor
from acquisition_realtime import EMGStream
from filter_realtime import Filter
from SAD_final import SAD
from decoder_realtime import Decoder
from gui_2048 import Board
from gui_text import GUI
import tkinter as tk
from tkinter import ttk
from gtts import gTTS
from playsound import playsound
import time

class GUI(tk.Tk):
	def __init__(self, master, input):
		self.input = input
		self.master = master

		width = 1280; height=800
		master.geometry(f'{width}x{height}') 

		self.word = "test"
		self.prev_word = "test"
		self.prev_2 = "test"

		self.word_l = ttk.Label(
            master, 
            text=f'{self.word}', 
            font=("Helvetica Neue Thin", 150),
            foreground='black',
        )
        
		self.prev_word_l = ttk.Label(
            master,
            text=f'{self.prev_word}',
            font=("Helvetica Neue Thin", 100),
            foreground='#888888'
        )
		self.prev_2_l = ttk.Label(
            master,
            text=f'{self.prev_2}',
            font=("Helvetica Neue Thin", 66),
            foreground='#dddddd'
        )

		self.word_l.pack(expand=True)
		self.prev_word_l.pack(expand=True)
		self.prev_2_l.pack(expand=True)

		self.update()

	def update(self):
		if not self.input.empty():
			self.prev_2 = self.prev_word
			self.prev_word = self.word
			self.word = self.input.get()

			self.word_l.configure(text=f"{self.word}")
			self.prev_word_l.configure(text=f"{self.prev_word}")
			self.prev_2_l.configure(text=f"{self.prev_2}")

			self.word_l.pack(expand=True)
			self.prev_word_l.pack(expand=True)
			self.prev_2_l.pack(expand=True)

			speech = gTTS(text=self.word, lang='en', slow=False)
			speech.save("audio.mp3")
			playsound("audio.mp3")
		self.master.after(200, self.update)

def run(input):
	root = tk.Tk()
	gui = GUI(root, input)
	root.mainloop()
