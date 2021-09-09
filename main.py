from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import tkinter.filedialog as fd
import numpy as np
import os
import threading
import cv2

matplotlib.use("TkAgg") # set the backends

class SpecificRotationWindow(Toplevel):
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
    
        self.set_angle_label = ttk.Label(self.mainframe, text="Set angle:")
        self.set_angle_label.grid(column=1, row=1, sticky=W)
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

class RotationWindow(Toplevel):
    def __init__(self, master = None, lb = None):
        super().__init__(master = master)
        self.master = master
        self.lb = lb
        self.title("Rotation Selection")

        self.mainframe = ttk.Frame(self, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
    
        ttk.Button(self.mainframe, text="Specific Rotation", command=self.specific_rotation).grid(column=3, row=1, sticky=W)
        ttk.Button(self.mainframe, text="Rough Rotation", command=self.rough_rotation).grid(column=1, row=1, sticky=W)
    
    def specific_rotation(self):
        self.Img = SpecificRotationWindow(self.master, self.lb)

    def rough_rotation(self):
        RoughRotationWindow(self.master, self.lb)

class RoughRotationWindow(Toplevel):
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
    
        # ttk.Label(self.mainframe, text="angle: ").grid(column=2, row=1, sticky=W)
        # self.angle_label = ttk.Label(self.mainframe, text="0")
        # self.angle_label.grid(column=3, row=1, sticky=W)
        self.progress = ttk.Label(self.mainframe, textvariable = self.progress_var)
        self.progress.grid(column=5, row=2, sticky=W)
        self.pgb = ttk.Progressbar(self.mainframe, orient=HORIZONTAL, length=100, mode="determinate")
        self.pgb.grid(columnspan=4, row=2, padx=3, pady=3, sticky=N+S+E+W)

        # ttk.Button(self.mainframe, text="Apply", command=self.set_rotation).grid(columnspan=5, row=4, sticky=N+S+E+W)
        ttk.Button(self.mainframe, text="+90", command=self.right_rotation).grid(column=1, row=1, sticky=W)
        ttk.Button(self.mainframe, text="180", command=self.one_rotation).grid(column=2, row=1, sticky=W)
        ttk.Button(self.mainframe, text="-90", command=self.left_rotation).grid(column=3, row=1, sticky=W)
    
    def right_execute(self):
        for i in self.lb.curselection():
            # self.Img.append(Image.open(self.lb.get(i)).rotate(float(Entry.get(self.angle))))
            dir_path, file_name = os.path.split(self.lb.get(i))

            if(not os.path.isdir("./export")):
                os.mkdir("./export")

            cv2.imwrite('./export/' + file_name, cv2.rotate(cv2.imread(self.lb.get(i)), cv2.ROTATE_90_CLOCKWISE))
            self.pgb['value'] += (100 / len(self.lb.curselection()))
            self.progress_var.set(str(round(self.pgb['value'])) + "%")

    def one_execute(self):
        for i in self.lb.curselection():
            dir_path, file_name = os.path.split(self.lb.get(i))

            if(not os.path.isdir("./export")):
                os.mkdir("./export")

            cv2.imwrite('./export/' + file_name, cv2.rotate(cv2.imread(self.lb.get(i)), cv2.ROTATE_180))
            self.pgb['value'] += (100 / len(self.lb.curselection()))
            self.progress_var.set(str(round(self.pgb['value'])) + "%")

    def left_execute(self):
        for i in self.lb.curselection():
            dir_path, file_name = os.path.split(self.lb.get(i))

            if(not os.path.isdir("./export")):
                os.mkdir("./export")

            cv2.imwrite('./export/' + file_name, cv2.rotate(cv2.imread(self.lb.get(i)), cv2.ROTATE_90_COUNTERCLOCKWISE))
            self.pgb['value'] += (100 / len(self.lb.curselection()))
            self.progress_var.set(str(round(self.pgb['value'])) + "%")

    # def plus(self):
    #     angle = int(self.angle_label['text'])
    #     angle = angle + 90
    #     self.angle_label.configure(text = str(angle))
        
    # def minus(self):
    #     angle = int(self.angle_label['text'])
    #     angle = angle - 90
    #     self.angle_label.configure(text = str(angle))

    def right_rotation(self):
        if(self.pgb['value'] != 0):
            self.pgb['value'] = 0
            self.progress_var.set('0%')


        apply_thread = threading.Thread(target=self.right_execute)
        apply_thread.start()
    
    def one_rotation(self):
        if(self.pgb['value'] != 0):
            self.pgb['value'] = 0
            self.progress_var.set('0%')

        apply_thread = threading.Thread(target=self.one_execute)
        apply_thread.start()
    
    def left_rotation(self):
        if(self.pgb['value'] != 0):
            self.pgb['value'] = 0
            self.progress_var.set('0%')

        apply_thread = threading.Thread(target=self.left_execute)
        apply_thread.start()

    # def set_zero(self):
    #     self.angle_label.configure(text="0")

class NamingWindow(Toplevel):
    def __init__(self, master = None, lb = None):
        super().__init__(master = master)
        self.lb = lb
        self.title("Automatic Naming")
        self.progress_var = StringVar()
        self.progress_var.set("0%")

        self.mainframe = ttk.Frame(self, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
    
        ttk.Label(self.mainframe, text="Start Name: ").grid(column=1, row=1, sticky=W)
        self.progress = ttk.Label(self.mainframe, textvariable = self.progress_var)
        self.progress.grid(column=5, row=3, sticky=W)
        self.pgb = ttk.Progressbar(self.mainframe, orient=HORIZONTAL, length=200, mode="determinate")
        self.pgb.grid(columnspan=4, row=3, padx=3, pady=3, sticky=N+S+E+W)
        
        self.name = ttk.Entry(self.mainframe)
        self.name.grid(column=2, row=1, sticky=W)

        self.var1 = IntVar()

        ttk.Button(self.mainframe, text="Apply", command=self.selected_item).grid(column=3, row=1, sticky=W)
        ttk.Checkbutton(self.mainframe, text="Labeled", variable=self.var1, onvalue=1, offvalue=0).grid(column=3, row=2, padx=3, sticky=W)

    def execute(self):
        j_f = False
        l_f = False

        if(not self.name is None):
            j = self.name.get()
            cur_len = len(self.lb.curselection())
            
            if(self.var1.get() == 1):
                l_f = True
            
            if(j[0] == '0'):
                j_f = True
                j = int(j)
    
            for i in self.lb.curselection():
                dir_path, file_name = os.path.split(self.lb.get(i))
                file_path, file_extension = os.path.splitext(file_name)
            
                self.lb.delete(i)

                if(j_f == True):
                    if(l_f == True):
                        os.rename(dir_path+'/'+file_name, dir_path+'/'+'Label_0'+str(j)+file_extension)
                        self.lb.insert(i, dir_path+'/'+'Label_0'+str(j)+file_extension)
                    else:
                        os.rename(dir_path+'/'+file_name, dir_path+'/'+'0'+str(j)+file_extension)
                        self.lb.insert(i, dir_path+'/'+'0'+str(j)+file_extension)
                else:
                    if(l_f == True):
                        os.rename(dir_path+'/'+file_name, dir_path+'/'+'Label_'+str(j)+file_extension)
                        self.lb.insert(i, dir_path+'/'+'Label_'+str(j)+file_extension)
                    else:
                        os.rename(dir_path+'/'+file_name, dir_path+'/'+str(j)+file_extension)
                        self.lb.insert(i, dir_path+'/'+str(j)+file_extension)

                self.pgb['value'] += (100 / cur_len)
                self.progress_var.set(str(round(self.pgb['value'])) + "%")
                j = j + 1

    def selected_item(self):
        self.Img = []

        apply_thread = threading.Thread(target=self.execute)
        apply_thread.start()

class PreviewWindow(Toplevel):
    def __init__(self, master = None, lb = None):
        super().__init__(master = master)
        
        self.lb = lb
        self.images = []

        self.title("Preview")

        self.i = 0
        
        self.mainframe = ttk.Frame(self, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        for i in self.lb.curselection():
            j = Image.open(self.lb.get(i))
            j.thumbnail((550, 450))
            self.images.append(ImageTk.PhotoImage(j))

        self.image_label = Label(self.mainframe, image=self.images[self.i])
        self.image_label.grid(columnspan=10, rowspan=10, padx=3, pady=3, sticky=N+S+E+W)
        self.image_label.image = self.images
        self.image_label.place(x=0, y=0)
  
        self.btn1 = Button(self.mainframe, text="Previous", bg='black', fg='gold', font=('ariel 15 bold'), relief=GROOVE, command=self.previous)
        self.btn1.grid(column=2, row=5, padx=3, pady=3, sticky=N+S+E+W)
        self.btn2 = Button(self.mainframe, text="Next", width=8, bg='black', fg='gold', font=('ariel 15 bold'), relief=GROOVE, command=self.next)
        self.btn2.grid(column=4, row=5, padx=3, pady=3, sticky=N+S+E+W)

    def previous(self):
        self.i = self.i - 1
        try:
            self.image_label.config(image=self.images[self.i])
        except:
            self.i = 0
            self.previous()

    def next(self):
        self.i = self.i + 1
        try:
            self.image_label.config(image=self.images[self.i])
        except:
            self.i = -1
            self.next()

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

class CheckWindow(Toplevel):
    def __init__(self, master = None, lb = None):
        super().__init__(master = master)
        
        self.title("Checking Export")

        self.mainframe = ttk.Frame(self, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        self.lb = Listbox(self.mainframe, selectmode=EXTENDED, height=10)
        self.lb.grid(columnspan=5, row=3, ipady=100, padx=5, pady=5, sticky=W+N+E+S)

        self.scrollbar = Scrollbar(self.lb, orient="vertical", command=self.lb.yview).pack(side=RIGHT, fill=Y)
        
        ttk.Button(self.mainframe, text="Export", width=30, command=self.extract).grid(column=3, row=1, padx=5, pady=5, sticky=W)

        self.data_input(lb)

    def extract(self):
        f = open("./extract.txt", "a")

        for i in self.lb.curselection():
            f.write(self.lb.get(i)+'\n')
        
        f.close()

    def data_input(self, ori):
        for i, j in enumerate(ori.get(0, ori.size())):
            dir_path, file_name = os.path.split(j)
            self.lb.insert(i, file_name)
            
class MainWindow(threading.Thread):
    def __init__(self, root):   
        root.title("Image Macro")
        root.bind("<KeyRelease>", self.key)
        
        self.rotation = None

        self.lb = Listbox(root, selectmode=EXTENDED, height=10)
        self.lb.grid(columnspan=5, row=3, ipady=100, padx=5, pady=5, sticky=W+N+E+S)

        self.scrollbar = Scrollbar(self.lb, orient="vertical", command=self.lb.yview).pack(side=RIGHT, fill=Y)
        
        ttk.Button(root, text="Import", width=30, command=self.openDialog).grid(column=1, row=1, padx=5, pady=5, sticky=W)
        ttk.Button(root, text="Export", width=30, command=self.save).grid(column=3, row=1, padx=5, pady=5, sticky=W)
       
    def key(self, event):
        if event.keysym=='r':
            if(len(self.lb.curselection())):
                self.rotation = RotationWindow(root, self.lb)
            else:
                messagebox.showinfo("Info", "No Selected Data")
        
        if event.keysym=='n':
            if(len(self.lb.curselection())):            
                NamingWindow(root, self.lb)
            else:
                messagebox.showinfo("Info", "No Selected Data")

        if event.keysym=='d':
            if(len(self.lb.curselection())):
                sel = self.lb.curselection()
                for i in sel[::-1]:
                    self.lb.delete(i)
            else:
                messagebox.showinfo("Info", "No Selected Data")

        if event.keysym=='c':
            if(len(self.lb.curselection())):
                CheckWindow(root, self.lb)
            else:
                messagebox.showinfo("Info", "No Selected Data")

        if event.keysym=='p':
            if(len(self.lb.curselection())):            
                for i in self.lb.curselection():
                    dir_path, file_name = os.path.split(self.lb.get(i))

                    if('Label_' in file_name):
                        src = cv2.imread(self.lb.get(i), 0)
                        ret,th1 = cv2.threshold(src,0.1,255,cv2.THRESH_BINARY)
                        
                        cv2.imshow(file_name, th1)
                        cv2.moveWindow(file_name, 900, 0)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
                    else:
                        src = cv2.imread(self.lb.get(i))

                        cv2.imshow(file_name, src)
                        cv2.moveWindow(file_name, 300, 0)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
            else:
                messagebox.showinfo("Info", "No Selected Data")
    
    def callback_right_button(self):
        print("Test")

    def bisect(self, list_of_items, item):    
        lo = 0
        hi = len(list_of_items)
    
        while lo < hi:
            mid = (lo+hi)//2

            if item < list_of_items[mid]: hi = mid
            else: lo = mid+1

        return lo
            
    def openDialog(self):
        self.filez = fd.askopenfilename(title="Choose a file", multiple=True, filetypes={
            ("image", ".jpeg"),
            ("image", ".png"),
            ("image", ".jpg"),
        })

        if(self.filez != None):
            for j in self.filez:
                index = self.bisect(self.lb.get(0, self.lb.size()), j)
                if(not j in self.lb.get(0, self.lb.size())):
                    self.lb.insert(index, j)
        
    def save(self):
        if(not os.path.isdir("./export")):
            os.mkdir("./export")

        if(self.rotation == None):
            messagebox.showinfo("Info", "No Export Data")
        else:  
            SaveWindow(root, self.rotation.Img)
        
if __name__ == "__main__":
    root = Tk()
    
    main = MainWindow(root)

    root.mainloop()












