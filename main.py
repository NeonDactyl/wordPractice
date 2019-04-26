from random import choice
from tkinter import *
from tkinter import ttk
import time
import threading


class gui:

    def loadWords(self):
        """
        Returns a list of valid words. Words are strings of lowercase letters.

        Depending on the size of the word list, this function may
        take a while to finish.
        """
        print("Loading word list from file...")
        # inFile: file
        inFile = open("wordlist.txt", 'r')
        # line: string
        line = inFile.readline()
        # wordlist: list of strings
        wordlist = line.split()
        return wordlist

    def setWord(self):
        """
        Sets the word in the label
        """
        self.word.set(choice(self.wordlist))
        self.t = threading.Timer(self.TIMER_LENGTH, self.setWord)
        self.start_time = time.time()
        self.time_remaining = self.TIMER_LENGTH
        self.t.start()

    def toggleTimer(self):
        if self.t.isAlive():
            self.t.cancel()
            self.time_remaining -= (time.time() - self.start_time)
        else:
            self.t = threading.Timer(self.time_remaining, self.setWord)
            self.start_time = time.time()
            self.t.start()

    def onClose(self):
        self.t.cancel()
        self.root.destroy()

    def __init__(self, timer_length):
        self.TIMER_LENGTH = timer_length
        self.root = Tk()
        self.root.title("Sight Word Practice")
        self.word = StringVar()
        self.word_label = Label(self.root, textvariable=self.word)
        self.word_label.grid(column=0, row=0, sticky=(N, E, S, W), padx=30, pady=30)
        self.word_label.config(font=("Helvetica", 96))
        self.pause = Button(text="Play/Pause", command=self.toggleTimer)
        self.pause.grid(row="1", column="0")
        self.wordlist = self.loadWords()
        self.setWord()
        self.root.geometry("900x250+100+350")
        self.root.protocol("WM_DELETE_WINDOW", self.onClose)
        # self.root.geometry("500x500")
        self.root.mainloop()


if __name__ == "__main__":
    window = gui(2.0)
