import time
import tkinter as tk
from tkinter import ttk

class Timer(tk.Tk):
    def __init__(self, vocal, countdown_start, output_file):
        super().__init__()

        # configure the window
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.geometry(f'{width}x{height}') 
        self.resizable(False, False)
        self.title("Silent Speech Data Collection")
        self.running = False

        # init labels
        self.vocal = ttk.Label(
            self, 
            text=vocal, 
            font=("Helvetica Neue Thin", 100))
        self.word = ttk.Label(
            self, 
            text='word', 
            font=("Helvetica Neue Thin", 300))
        self.countdown_start = countdown_start
        self.countdown = ttk.Label(
            self,
            text=f'{self.countdown_start}',
            font=("Helvetica Neue Thin", 150)
        )

        # init file
        self.f = open(output_file, 'x')

    def start_word(self, word):
        # init and display labels
        self.word.configure(text=word)
        self.vocal.pack(expand=True);
        self.word.pack(expand=True); 
        self.countdown.pack(expand=True);
        self.countdown.after(1000, lambda: self.start_countdown(self.countdown_start, word))

        # wait for stop key

        # record ending timestamp

        # clear
    
    def end_word(self, word):
        self.write_timestamp(word, start=False)
        # self.bind('<KeyPress-SpaceBar>', self.next)
        # self.bind('<KeyPress-R>', self.repeat)
        self.clear()


    def start_countdown(self, cd, word):
        """
        Starts the countdown timer and writes the starting timestamp to file.

        Args:
            cd (int): starting time for the timer (in s)
            word (str) the current word
        """

        if cd-1 == 0:
            self.countdown.configure(text='GO',foreground='green')
            self.write_timestamp(word, start=True)
            self.bind('<Return>', lambda x: self.end_word(word))
        else:
            self.countdown.configure(text=f'{cd-1}')
            self.countdown.after(1000, lambda: self.start_countdown(cd-1, word))

    def clear(self):
        """
        Resets the countdown timer and hides GUI text.
        """

        self.countdown.configure(text=f'{self.countdown_start}',foreground='black')
        self.vocal.pack_forget()
        self.word.pack_forget()
        self.countdown.pack_forget()

    def write_timestamp(self, word, start):
        """
        Writes the current word, timestamp type, and timestamp value (in ns) to the
        output file.

        Args:
            word (str): the current word
            start (bool): whether this is the start time (=True) or stop time 
                (=False)
        """

        print(f'{word} {"start" if start else "stop"}: {time.time_ns()}')
        self.f.write(f'{word} {"start" if start else "stop"}: {time.time_ns()}\n')
        self.f.flush()

    def repeat():
        self.repeat = 1
        print("repeat")

    def next():
        print("next")
