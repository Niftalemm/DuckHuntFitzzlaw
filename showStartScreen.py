import tkinter as tk
from tkinter import scrolledtext, messagebox
import sys
import pygame

# Put your full agreement here (or load from disk)
AGREEMENT_TEXT = open("assets/agreement.txt", "r").read()

def show_user_agreement():
    """
    Displays a user agreement window with a scrollable text widget and two buttons: "I Agree" and "Decline".
    The function creates a GUI window using Tkinter. The agreement text is displayed in a read-only 
    scrolled text widget. Users can either agree to proceed or decline, which exits the application 
    with a warning message.
    """
    root = tk.Tk()
    root.title("User Agreement")
    root.geometry("700x500")

    # Scrolled text widget
    txt = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Consolas", 10))
    txt.insert(tk.END, AGREEMENT_TEXT)
    txt.configure(state='disabled')  # read‑only
    txt.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Buttons
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=5)
    def on_agree():
        root.destroy()
        root.result = "agree"

    def on_decline():
        messagebox.showwarning("Declined", "You must agree to play.")
        root.result = "decline"
        root.destroy()

    tk.Button(btn_frame, text="I Agree", width=12, command=on_agree).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Decline", width=12, command=on_decline).pack(side=tk.LEFT, padx=5)

    root.result = None

    root.mainloop()
