import tkinter as tk
import sys
import threading
from tkinter import messagebox
from tkinter.ttk import *
from tkinter.scrolledtext import ScrolledText
from scraper import run_all

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("700x500")
        # self.resizable(False, False)

        main_frame = tk.Frame(self, bg="#84CEEB", height=600, width=1024)
        main_frame.pack_propagate(False)
        main_frame.pack(fill="both", expand=1)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        title_styles = {"font": ("Trebuchet MS Bold", 16)}

        text_styles = {"font": ("Verdana", 12)}

        style = Style()
        style.configure('TButton', font=('calibri', 20, 'bold'),
                        borderwidth='4')
        style.map('TButton', foreground=[('active', '!disabled', 'green')],
                  background=[('active', 'green')])

        label_title = tk.Label(main_frame, title_styles, text="Web Listening")
        label_title.pack(pady=(0, 15))

        label_1 = tk.Label(main_frame, text_styles, text="Keyword 1")
        label_1.pack()
        entry_1 = tk.Entry(main_frame, width=35, font=15)
        entry_1.focus_force()
        entry_1.pack(pady=(0, 10), ipadx=30, ipady=6)

        label_2 = tk.Label(main_frame, text_styles, text="Keyword 2")
        label_2.pack()
        entry_2 = tk.Entry(main_frame, width=35, font=15)
        entry_2.pack(pady=(0, 20), ipadx=30, ipady=6)

        self.b1 = Button(main_frame, text="Start", style='TButton',
                         command=lambda: self.run(entry_1.get(), entry_2.get()))
        self.b1.pack(pady=(0, 10))

        self.text = ScrolledText(main_frame, wrap="word")
        self.text.pack(fill="both", expand=True)

        sys.stdout = TextRedirector(self.text, "stdout")

    def run(self, one, two):
        if len(one) != 0 and len(two) != 0:
            if messagebox.askyesnocancel('Confirm', f'Use keywords {one} and {two}?'):
                threading.Thread(target=run_all,
                                 args=([one, two],)
                                 ).start()
                self.b1['state'] = 'disabled'
        else:
            messagebox.showerror('Invalid input', 'Invalid input')


class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, text):
        self.widget.configure(state="normal")
        self.widget.insert("end", text, (self.tag,))
        self.widget.configure(state="disabled")

    def flush(self):
        pass


app = App()
app.mainloop()
