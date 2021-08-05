from tkinter import *
from tkinter import ttk
from PIL import Image
import tkinter.filedialog as fd
import os
import threading

class RotationWindow(Toplevel):
    def __init__(self, master = None, lb = None):
        super().__init__(master = master)
        self.lb = lb
        self.title("Rotation")
        self.progress_var = StringVar()
        self.progress_var.set("0%")

        self.mainframe = ttk.Frame(self, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
    
        ttk.Label(self.mainframe, text="Set angle:").grid(column=1, row=1, sticky=W)
        self.progress = ttk.Label(self.mainframe, textvariable = self.progress_var)
        self.progress.grid(column=5, row=2, sticky=W)
        self.pgb = ttk.Progressbar(self.mainframe, orient=HORIZONTAL, length=200, mode="determinate")
        self.pgb.grid(columnspan=4, row=2, padx=3, pady=3, sticky=N+S+E+W)
        
        self.angle = ttk.Entry(self.mainframe)
        self.angle.grid(column=2, row=1, sticky=W)

        ttk.Button(self.mainframe, text="Apply", command=self.selected_item).grid(column=3, row=1, sticky=W)
    
    def execute(self):
        for i in self.lb.curselection():
            self.Img.append(Image.open(self.lb.get(i)).rotate(float(Entry.get(self.angle))))
            self.pgb['value'] += (100 / len(self.lb.curselection()))
            self.progress_var.set(str(round(self.pgb['value'])) + "%")

    def selected_item(self):
        self.Img = []

        apply_thread = threading.Thread(target=self.execute)
        apply_thread.start()

class SaveWindow(Toplevel):
    def __init__(self, master = None, Img = None):
        super().__init__(master = master)
        self.Img = Img

        self.title("Export")
        self.progress_var = StringVar()
        self.progress_var.set("0%")

        self.mainframe = ttk.Frame(self, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        self.progress = ttk.Label(self.mainframe, textvariable = self.progress_var)
        self.progress.grid(column=5, row=1, sticky=W)
        self.pgb = ttk.Progressbar(self.mainframe, orient=HORIZONTAL, length=200, mode="determinate")
        self.pgb.grid(columnspan=4, row=1, padx=3, pady=3, sticky=N+S+E+W)

        save_thread = threading.Thread(target=self.execute)
        save_thread.start()
        
    def execute(self):
        for i, j in enumerate(self.Img):
            j.save("./export/" + str(i) + ".png")
            self.pgb['value'] += (100 / len(self.Img))
            self.progress_var.set(str(round(self.pgb['value'])) + "%")
            
class MainWindow(threading.Thread):
    def __init__(self, root):   
        root.title("Image Macro")
        root.bind("<KeyRelease>", self.key)
        
        self.lb = Listbox(root, selectmode="multiple", height=10)
        self.lb.grid(columnspan=5, row=3, ipady=100, padx=5, pady=5, sticky=W+N+E+S)

        self.scrollbar = Scrollbar(self.lb, orient="vertical", command=self.lb.yview).pack(side=RIGHT, fill=Y)
        
        ttk.Button(root, text="Import", width=30, command=self.openDialog).grid(column=1, row=1, padx=5, pady=5, sticky=W)
        ttk.Button(root, text="Export", width=30, command=self.save).grid(column=3, row=1, padx=5, pady=5, sticky=W)
       
    def key(self, event):
        self.rotation = None
        
        if event.keysym=='r':
            self.rotation = RotationWindow(root, self.lb)

    def openDialog(self):
        self.filez = fd.askopenfilename(title="Choose a file", multiple=True, filetypes={
            ("image", ".jpeg"),
            ("image", ".png"),
            ("image", ".jpg"),
        })

        if(self.filez != None):
            for i, j in enumerate(self.filez):
                self.lb.insert(i, j)
        
    def save(self):
        if(not os.path.isdir("./export")):
            os.mkdir("./export")
        
        SaveWindow(root, self.rotation.Img)
        
if __name__ == "__main__":
    root = Tk()
    
    main = MainWindow(root)

    root.mainloop()












