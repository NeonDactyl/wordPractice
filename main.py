from random import choice
from tkinter import *
from tkinter import ttk
import time
import threading


class gui:

    def load_words(self):
        """
        Loads internal list of practice words from file, "wordlist.txt"
        """
        in_file = open("wordlist.txt", 'r')
        # line: string
        line = in_file.readline()
        # wordlist: list of strings
        self.word_list = line.split()

    def set_word(self):
        """
        Sets the word in the label
        """
        self.word.set(choice(self.word_list))
        self.word_label.update()
        self.geometry_update()
        self.t = threading.Timer(self.TIMER_LENGTH, self.set_word)
        self.start_time = time.time()
        self.time_remaining = self.TIMER_LENGTH
        self.t.start()

    def geometry_update(self):
        """
        Adjusts window size and position to keep it centered on screen, and
        maintains extra width around the word.
        """
        self.window_width = self.word_label.winfo_width() + 60
        self.window_x_pos = int((self.screen_width - self.window_width) // 2)
        self.root.geometry("{}x{}+{}+{}".format(self.window_width,
                                                self.window_height,
                                                self.window_x_pos,
                                                self.window_y_pos))

    def toggle_timer(self, event=None):
        """
        Used to pause and restart the timer, based upon time remaining.
        """
        if self.t.isAlive():
            self.t.cancel()
            self.time_remaining -= (time.time() - self.start_time)
        else:
            self.t = threading.Timer(self.time_remaining, self.set_word)
            self.start_time = time.time()
            self.t.start()

    def on_close(self):
        """
        When closing window, cancel timer, and destroy root.
        """
        self.t.cancel()
        self.root.destroy()

    def __init__(self, timer_length):
        self.TIMER_LENGTH = timer_length
        self.root = Tk()
        self.root.title("Sight Word Practice")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.window_height = 320
        self.window_y_pos = int((self.screen_height - self.window_height) // 2)

        self.word = StringVar()
        self.word_label = Label(self.root, textvariable=self.word)
        self.word_label.grid(column=0, row=0, sticky=(E, W), padx=30, pady=30)
        self.word_label.config(font=("Helvetica", 96))

        self.pause = Button(self.root, text="Pause", command=self.toggle_timer)
        self.pause.grid(row="1", column="0", sticky=(N))
        self.pause.config(font=("Helvetica", 32))
        self.pause.focus_force()

        self.load_words()
        self.set_word()

        self.root.bind('<Return>', self.toggle_timer)
        self.root.mainloop()


if __name__ == "__main__":
    window = gui(3.0)
