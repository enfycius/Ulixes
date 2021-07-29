from tkinter import *
from tkinter import ttk

class RotationWindow(Toplevel):
    def __init__(self, master = None):
        super().__init__(master = master)
        self.title("Rotation")
        mainframe = ttk.Frame(self, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        ttk.Label(mainframe, text="Set angle").grid(column=1, row=1, sticky=W)
        ttk.Entry(mainframe).grid(column=2, row=1, sticky=W)

root = Tk()        

def key(event):
    # RotationWindow(root)
    if event.keysym=='r':
        RotationWindow(root)

root.title("Image Macro")
root.bind("<KeyRelease>", key)

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)


ttk.Button(mainframe, text="Import").grid(column=2, row=2, sticky=W)
ttk.Button(mainframe, text="Export").grid(column=3, row=2, sticky=W)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

root.mainloop()
