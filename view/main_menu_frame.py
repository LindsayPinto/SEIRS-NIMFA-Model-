import os
import tkinter as tk
from tkinter import filedialog

class MainMenuFrame(tk.Frame):
    def __init__(self, master, show_params, quit):
        super().__init__(master)

        self.grid_columnconfigure(1, minsize=200)
        self.grid_columnconfigure([0,2], weight=1)
        self.grid_rowconfigure(2, minsize=20)
        tk.Button(self, text="Load network from file...", command=lambda: self.open_file(show_params)).grid(row=1, column=1, sticky="ew")
        tk.Button(self, text="Exit", command=quit).grid(row=3, column=1, sticky="ew")

    def open_file(self, show_params):
        file = filedialog.askopenfilename(title="Select file", initialdir=os.getcwd())
        if(file):
            show_params(file)