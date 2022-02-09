import time
import tkinter as tk
from tkinter import ttk
import random

class Timer(tk.Tk):
    def __init__(self, vocal, countdown_start, output_file):
        super().__init__()

        # configure the window
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.geometry(f'{width}x{height}') 
        self.resizable(False, False)
        self.title("Silent Speech Data Collection") 

        # init list and index
        self.list = []
        self.index = 0

        # init labels
        self.vocal = vocal
        self.vocal_label = ttk.Label(
            self, 
            text=f'{vocal}: word {self.index+1} of {len(self.list)}', 
            font=("Helvetica Neue Thin", 100),
            foreground='#0079BF')
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
        self.next_prompt = ttk.Label(
            self,
            text="Press 'r' to repeat the previous word \n or spacebar to record the next word",
            font=("Helvetica Neue Thin", 100)
        )

        # init file
        self.f = open(output_file, 'x')

    def run(self, word_list):
        """
        Runs through data collection for the given word list.

        Args:
            word_list (str list): list of words to record
        """
        # randomize list
        rand_list = word_list.copy()
        random.shuffle(rand_list)
        self.list = rand_list

        self.start_word(self.list[0])

    def start_word(self, word):
        """
        Initializes the GUI and countdown for a single word.

        Args:
            word (str): the word being recorded
        """

        # init and display labels
        self.next_prompt.pack_forget();
        self.unbind('<KeyPress-space>')
        self.unbind('<KeyPress-r>')
        self.word.configure(text=word)
        self.vocal_label.configure(text=f'{self.vocal}: word {self.index+1} of {len(self.list)}')
        self.vocal_label.pack(expand=True);
        self.word.pack(expand=True); 
        self.countdown.pack(expand=True);
        self.countdown.after(1000, lambda: self.start_countdown(self.countdown_start, word))
    
    def end_word(self, word):
        """
        Clears the screen and sets keybinds for next steps.

        Args:
            word (str): the word being recorded
        """
        self.write_timestamp(word, start=False)
        # self.unbind('<KeyPress-space>')
        self.bind('<KeyPress-space>', self.next)
        self.bind('<KeyPress-r>', self.repeat)
        self.clear()


    def start_countdown(self, cd, word):
        """
        Starts the countdown timer and writes the starting timestamp to file.

        Args:
            cd (int): starting time for the timer (in s)
            word (str): the word being recorded
        """

        if cd-1 == 0:
            self.countdown.configure(text='GO',foreground='green')
            self.write_timestamp(word, start=True)
            self.bind('<Return>', lambda key: self.end_word(word))
        else:
            self.countdown.configure(text=f'{cd-1}')
            self.countdown.after(1000, lambda: self.start_countdown(cd-1, word))

    def clear(self):
        """
        Resets the countdown timer and hides GUI text.
        """
        self.countdown.configure(text=f'{self.countdown_start}',foreground='black')
        self.vocal_label.pack_forget()
        self.word.pack_forget()
        self.countdown.pack_forget()
        self.next_prompt.pack(expand=1)

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

    def repeat(self, key):
        """
        Repeats the collection of the previous word.

        Args:
            key (event): key press event 
        """
        self.start_word(self.list[self.index])

    def next(self, key):
        """.
        Starts the collection of the next word in the list.

        Args:
            key (event): key press event
        """
        self.index=self.index+1
        self.start_word(self.list[self.index])
