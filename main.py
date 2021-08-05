from tkinter import *
from tkinter import ttk
import tkinter.filedialog as fd

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

class MainWindow:
    def __init__(self, root):   
        root.title("Image Macro")
        root.bind("<KeyRelease>", self.key)
        
        self.lb = Listbox(root, selectmode="extended", height=10)
        self.lb.grid(columnspan=5, row=3, ipady=100, padx=5, pady=5, sticky=W+N+E+S)

        self.scrollbar = Scrollbar(self.lb, orient="vertical", command=self.lb.yview).pack(side=RIGHT, fill=Y)
        
        ttk.Button(root, text="Import", width=30, command=self.openDialog).grid(column=1, row=1, padx=5, pady=5, sticky=W)
        ttk.Button(root, text="Export", width=30).grid(column=3, row=1, padx=5, pady=5, sticky=W)
       
    def key(self, event):
    # RotationWindow(root)
        if event.keysym=='r':
            RotationWindow(root)

    def openDialog(self):
        self.filez = fd.askopenfilename(title="Choose a file", multiple=True, filetypes={
            ("image", ".jpeg"),
            ("image", ".png"),
            ("image", ".jpg"),
        })

        if(self.filez != None):
            for i, j in enumerate(self.filez):
                self.lb.insert(i, j)
        
if __name__ == "__main__":
    root = Tk()
    
    main = MainWindow(root)

    root.mainloop()












