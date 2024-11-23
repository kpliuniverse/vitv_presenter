import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Hello World")

# Create a label widget with the text "Hello, World!"
label = tk.Label(root, text="Hello, World!", font=("Helvetica", 16))
label.pack(padx=20, pady=20)

# Start the Tkinter event loop
root.mainloop()
