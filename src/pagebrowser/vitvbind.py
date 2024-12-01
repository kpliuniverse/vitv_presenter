import tkinter as tk

def propagate_parent (e: tk.Event, event: str):
    e.widget.master.event_generate(event)