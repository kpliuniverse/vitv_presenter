from copy import deepcopy
import tkinter as tk

import PIL
import PIL.Image
import PIL.ImageTk

import layoutconsts


path: str = "assets/sampprev.png"

    
class App:
    root: tk.Tk = tk.Tk()

    thumb_list: list[tk.Frame] = []
    def on_frame_click(self, event: tk.Event):
        print(f"Frame was clicked from {event.widget}, labeled!")
    def __init__(self):
        with PIL.Image.open(path) as img:
            img = img.resize((layoutconsts.SMALL_THUMB_SIZE, layoutconsts.SMALL_THUMB_SIZE), PIL.Image.Resampling.LANCZOS)
            #img.show()
            self.s_img = PIL.ImageTk.PhotoImage(img)
        for i in range(7):
            x = tk.Frame(self.root, width=layoutconsts.SMALL_THUMB_SIZE, height=layoutconsts.SMALL_THUMB_SIZE)
            
            s = tk.Label(x, image=self.s_img, width=layoutconsts.SMALL_THUMB_SIZE, height=layoutconsts.SMALL_THUMB_SIZE)
            s.grid(row=0,column=0)
            x.pack_propagate(False)
            self.thumb_list.append(x)
            x.bind("<Button-1>", self.on_frame_click)
            s.bind("<Button-1>", self.on_frame_click)
        
        for i, x in enumerate(self.thumb_list):
            x.grid(row=i // 4, column= i % 4)
        self.root.geometry("400x300")

    def run(self):

        #self.root.title("VitVDocs")
        self.root.mainloop()
        


if __name__ == "__main__": 
    app = App()
    print("a")
    app.run()