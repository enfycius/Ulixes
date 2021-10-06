from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from shutil import copyfile
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import tkinter.filedialog as fd
import numpy as np
import os
import subprocess
import platform
import threading
import cv2
import natsort

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
        self.specific = SpecificRotationWindow(self.master, self.lb)

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

class CropWindow(Toplevel):
    def __init__(self, master = None, lb = None):
        super().__init__(master = master)
        self.lb = lb
        self.title("Crop")
        self.progress_var = StringVar()
        self.progress_var.set("0%")

        self.get_start_width = StringVar()
        self.get_start_height = StringVar()
        self.get_end_width = StringVar()
        self.get_end_height = StringVar()

        self.mainframe = ttk.Frame(self, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        # ttk.Label(self.mainframe, text="Start Width: ").grid(column=1, row=1, sticky=W)
        # ttk.Label(self.mainframe, text="").grid(column=1, row=1, sticky=W)
        # ttk.Label(self.mainframe, text="Start Height: ").grid(column=3, row=1, sticky=W)
        # ttk.Label(self.mainframe, text="").grid(column=1, row=1, sticky=W)
        # ttk.Label(self.mainframe, text="End Width: ").grid(column=1, row=2, sticky=W)
        # ttk.Label(self.mainframe, text="").grid(column=1, row=1, sticky=W)
        # ttk.Label(self.mainframe, text="End Height: ").grid(column=3, row=2, sticky=W)
        # ttk.Label(self.mainframe, text="").grid(column=1, row=1, sticky=W)
    
        ttk.Label(self.mainframe, text="Start Width: ").grid(column=1, row=1, sticky=W)
        ttk.Label(self.mainframe, text="Start Height: ").grid(column=3, row=1, sticky=W)
        ttk.Label(self.mainframe, text="End Width: ").grid(column=1, row=2, sticky=W)
        ttk.Label(self.mainframe, text="End Height: ").grid(column=3, row=2, sticky=W)

        self.progress = ttk.Label(self.mainframe, textvariable = self.progress_var)
        self.progress.grid(column=5, row=3, sticky=W)
        self.pgb = ttk.Progressbar(self.mainframe, orient=HORIZONTAL, length=200, mode="determinate")
        self.pgb.grid(columnspan=5, row=3, padx=3, pady=3, sticky=N+S+E+W)
        
        ttk.Entry(self.mainframe, textvariable=self.get_start_width).grid(column=2, row=1, sticky=W)
        ttk.Entry(self.mainframe, textvariable=self.get_start_height).grid(column=4, row=1, sticky=W)
        ttk.Entry(self.mainframe, textvariable=self.get_end_width).grid(column=2, row=2, sticky=W)
        ttk.Entry(self.mainframe, textvariable=self.get_end_height).grid(column=4, row=2, sticky=W)

        ttk.Button(self.mainframe, text="Apply", command=self.crop_image).grid(columnspan=5, row=4, sticky=N+S+E+W)
    
    def execute(self):
        for i in self.lb.curselection():
            dir_path, file_name = os.path.split(self.lb.get(i))
            img = cv2.imread(self.lb.get(i))
            # croped_img = img.crop((int(self.get_start_width.get()), int(self.get_start_height.get()), int(self.get_end_width.get()), int(self.get_end_height.get())))
            # resized_img = croped_img.resize((int(self.get_end_width.get()) - int(self.get_start_width.get()), int(self.get_end_height.get()) - int(self.get_start_height.get())))
            crop_img = img[int(self.get_start_height.get()):int(self.get_end_height.get()), int(self.get_start_width.get()):int(self.get_end_width.get())]
            cv2.imwrite("./export/" + file_name, crop_img)
            self.pgb['value'] += (100 / len(self.lb.curselection()))
            self.progress_var.set(str(round(self.pgb['value'])) + "%")

    def crop_image(self):
        if(self.pgb['value'] != 0):
            self.pgb['value'] = 0
            self.progress_var.set('0%')

        if(self.get_start_width.get() == '' or self.get_start_height.get() == '' or self.get_end_width.get() == '' or self.get_end_height.get() == ''):
            messagebox.showinfo("Info", "No Input Data")
        else:
            apply_thread = threading.Thread(target=self.execute)
            apply_thread.start()

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

class LabelingWindow(Toplevel):
    def __init__(self, master = None, lb = None):
        super().__init__(master = master)
        self.lb = lb
        self.title("Image Labeling")
        self.progress_var = StringVar()
        self.progress_var.set("0%")

        self.mainframe = ttk.Frame(self, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
        
        self.l_value = IntVar()
        self.t_value = DoubleVar()
    
        ttk.Label(self.mainframe, text="Label Value: ").grid(column=1, row=1, sticky=W)
        ttk.Label(self.mainframe, text="Threshold: ").grid(column=1, row=2, sticky=W)
        self.progress = ttk.Label(self.mainframe, textvariable = self.progress_var)
        self.progress.grid(column=5, row=3, sticky=W)
        self.pgb = ttk.Progressbar(self.mainframe, orient=HORIZONTAL, length=200, mode="determinate")
        self.pgb.grid(columnspan=4, row=3, padx=3, pady=3, sticky=N+S+E+W)
        
        self.label_value = ttk.Entry(self.mainframe, textvariable=self.l_value)
        self.label_value.grid(column=2, row=1, sticky=W)
        
        self.threshold = ttk.Entry(self.mainframe, textvariable=self.t_value)
        self.threshold.grid(column=2, row=2, sticky=W)

        ttk.Button(self.mainframe, text="Apply", command=self.selected_item).grid(columnspan=3, row=4, sticky=N+S+E+W)
    
    def execute(self):
        if(not os.path.isdir("./export/")):
            os.mkdir("./export/")

        if(not os.path.isdir("./export/label/")):
            os.mkdir("./export/label/")

        for i in self.lb.curselection():
            dir_path, file_name = os.path.split(self.lb.get(i))

            src = cv2.imread(self.lb.get(i), 0)
            ret,th1 = cv2.threshold(src,float(self.threshold.get()),int(self.label_value.get()),cv2.THRESH_BINARY)
                    
            cv2.imwrite('./export/label/' + file_name, th1)

            self.pgb['value'] += (100 / len(self.lb.curselection()))
            self.progress_var.set(str(round(self.pgb['value'])) + "%")

    def selected_item(self):
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

class AutomaticCheckWindow(Toplevel):
    def __init__(self, master = None, lb = None):
        super().__init__(master = master)
        
        self.title("Automatic Checking")
        self.progress_var = StringVar()
        self.progress_var.set("0%")

        self.mainframe = ttk.Frame(self, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        self.ori_path_v = StringVar()
        self.label_path_v = StringVar()
        self.l_value = IntVar()
        
        ttk.Label(self.mainframe, text="Ori Path: ").grid(column=1, row=1, sticky=W)
        ttk.Label(self.mainframe, text="Label Path: ").grid(column=1, row=2, sticky=W)
        ttk.Label(self.mainframe, text="Label Value: ").grid(column=1, row=3, sticky=W)
        
        ttk.Label(self.mainframe, textvariable=self.ori_path_v).grid(column=2, row=1, sticky=W)
        ttk.Label(self.mainframe, textvariable=self.label_path_v).grid(column=2, row=2, sticky=W)
        
        self.progress = ttk.Label(self.mainframe, textvariable = self.progress_var)
        self.progress.grid(column=5, row=4, sticky=W)
        self.pgb = ttk.Progressbar(self.mainframe, orient=HORIZONTAL, length=200, mode="determinate")
        self.pgb.grid(columnspan=4, row=4, padx=3, pady=3, sticky=N+S+E+W)
        
        self.label_value = ttk.Entry(self.mainframe, textvariable=self.l_value)
        self.label_value.grid(column=2, row=3, sticky=W)

        ttk.Button(self.mainframe, text="Find", command=self.ori_path, state=NORMAL).grid(column=3, row=1, sticky=N+S+E+W)
        ttk.Button(self.mainframe, text="Find", command=self.label_path, state=NORMAL).grid(column=3, row=2, sticky=N+S+E+W)
        
        self.check_Btn = ttk.Button(self.mainframe, text="Check", command=self.check, state=DISABLED)
        self.check_Btn.grid(columnspan=4, row=5, sticky=N+S+E+W)

    def ori_path(self):
        self.ori_p = fd.askdirectory(parent=self, initialdir='/', title="Please select a directory")
        self.ori_path_v.set(self.ori_p)

        if(self.label_path_v.get() != ''):
            self.check_Btn['state'] = NORMAL

    def label_path(self):
        self.label_p = fd.askdirectory(parent=self, initialdir='/', title="Please select a directory")
        self.label_path_v.set(self.label_p)

        if(self.ori_path_v.get() != ''):
            self.check_Btn['state'] = NORMAL

    def check_pixel(self, l, image):
        h = image.shape[0]
        w = image.shape[1]

        for y in range(0, h):
            for x in range(0, w):
                if((image[y, x] != l) and (image[y, x] != 0)):
                    return False
        
        return True

    def execute(self):
        label_l = os.listdir(self.label_path_v.get())
        label_list = [label_f for label_f in label_l if label_f.endswith(".png")]
        label_list = natsort.natsorted(label_list, reverse=False)

        ori_l = os.listdir(self.ori_path_v.get())
        ori_list = [ori_f for ori_f in ori_l if ori_f.endswith(".jpg")]
        ori_list = natsort.natsorted(ori_list, reverse=False)

        f = open("./checking_result.txt", "w")

        if(len(label_list) == len(ori_list)):
            for i, j in zip(ori_list, label_list):
                ori_img = cv2.imread(self.ori_path_v.get() + '/' + i, cv2.IMREAD_GRAYSCALE)
                label_img = cv2.imread(self.label_path_v.get() + '/' + j, cv2.IMREAD_GRAYSCALE)
                
                if((ori_img.shape[0] == label_img.shape[0]) and (ori_img.shape[1] == label_img.shape[1])):
                    if(not self.check_pixel(self.l_value.get(), label_img)):
                        f.write('label: ' + i + '\n')
                else:
                    f.write('Not Matching Image Shape\n')
                    f.write('-------------------------\n')
                    f.write('ori: ' + j + ' ' + 'label: ' + i + '\n')

                self.pgb['value'] += (100 / len(label_list))
                self.progress_var.set(str(round(self.pgb['value'])) + "%")

            messagebox.showinfo("Info", str(len(label_list)) + ' ' + "Checking Completed.")
                
        else:
            messagebox.showinfo("Info", "Not Matching File Size")

        f.close()

    def check(self):
        apply_thread = threading.Thread(target=self.execute)
        apply_thread.start()
        

        # for i in self.lb.curselection():
        #     dir_path, file_name = os.path.split(self.lb.get(i))

        #     if('Label_' in file_name):
        #         src = cv2.imread(self.lb.get(i), 0)
        #         ret,th1 = cv2.threshold(src,0.1,255,cv2.THRESH_BINARY)
                        
        #         cv2.imshow(file_name, th1)
        #         cv2.moveWindow(file_name, 900, 0)
        #         cv2.waitKey(0)
        #         cv2.destroyAllWindows()
        #     else:
        #         src = cv2.imread(self.lb.get(i))

        #         cv2.imshow(file_name, src)
        #         cv2.moveWindow(file_name, 300, 0)
        #         cv2.waitKey(0)
        #         cv2.destroyAllWindows()

        

    def selected_item(self, ori):
        for i, j in enumerate(ori.get(0, ori.size())):
            dir_path, file_name = os.path.split(j)
            self.lb.insert(i, file_name)

class CopyWindow(Toplevel):
    def __init__(self, master = None, lb = None):
        super().__init__(master = master)
        self.lb = lb
        self.title("Copy & Paste")
        self.progress_var = StringVar()
        self.progress_var.set("0%")

        self.mainframe = ttk.Frame(self, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
        
        self.copy_count = IntVar()
    
        ttk.Label(self.mainframe, text="Copy Count: ").grid(column=1, row=1, sticky=W)
        self.progress = ttk.Label(self.mainframe, textvariable = self.progress_var)
        self.progress.grid(column=5, row=2, sticky=W)
        self.pgb = ttk.Progressbar(self.mainframe, orient=HORIZONTAL, length=200, mode="determinate")
        self.pgb.grid(columnspan=4, row=2, padx=3, pady=3, sticky=N+S+E+W)
        
        self.copy_count_value = ttk.Entry(self.mainframe, textvariable=self.copy_count)
        self.copy_count_value.grid(column=2, row=1, sticky=W)

        ttk.Button(self.mainframe, text="Apply", command=self.selected_item).grid(columnspan=3, row=3, sticky=N+S+E+W)
    
    def execute(self):
        if(not os.path.isdir("./export/")):
            os.mkdir("./export/")

        if(not os.path.isdir("./export/paste/")):
            os.mkdir("./export/paste/")

        print(self.lb.get(0))
        dir_path, file_name = os.path.split(self.lb.get(0))

        print(dir_path, file_name)

        for i in self.lb.curselection():
            for j in range(0, int(self.copy_count_value.get())):
                dir_path, file_name = os.path.split(self.lb.get(i))
                file_name, file_extension = os.path.splitext(file_name)

                if os.path.isfile('./export/paste/'+file_name+str(j)+file_extension):
                    os.remove('./export/paste/'+file_name+str(j)+file_extension)
                    
                copyfile(self.lb.get(i), './export/paste/'+file_name+str(j)+file_extension)

            self.pgb['value'] += (100 / len(self.lb.curselection()))
            self.progress_var.set(str(round(self.pgb['value'])) + "%")

    def selected_item(self):
        apply_thread = threading.Thread(target=self.execute)
        apply_thread.start()

            
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

        if event.keysym=='a':
            AutomaticCheckWindow(root, self.lb)
            
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

        if event.keysym=='t':
            if(len(self.lb.curselection())):
                LabelingWindow(root, self.lb)
            else:
                messagebox.showinfo("Info", "No Selected Data")

        if event.keysym=='o':
            if(len(self.lb.curselection())):
                CropWindow(root, self.lb)

        if event.keysym=='c':
            if(len(self.lb.curselection())):
                CheckWindow(root, self.lb)
            else:
                messagebox.showinfo("Info", "No Selected Data")

        if event.keysym=='e':
            if(len(self.lb.curselection())):
                for i in self.lb.curselection():
                    dir_path, file_name = os.path.split(self.lb.get(i))
                    self.open_folder(dir_path)
            else:
                messagebox.showinfo("Info", "No Selected Data")

        if event.keysym=='l':
            self.open_folder('./export/')

        if event.keysym=='x':
            if(len(self.lb.curselection())):
                CopyWindow(root, self.lb)
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

    def open_folder(self, path):
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])

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

        if(self.rotation.specific.Img == None):
            messagebox.showinfo("Info", "No Export Data")
        else:  
            SaveWindow(root, self.rotation.specific.Img)
        
if __name__ == "__main__":
    root = Tk()
    
    main = MainWindow(root)

    root.mainloop()












