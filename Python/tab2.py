import tkinter, tkinter.filedialog
import ttkthemes

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler

import numpy as np
import globalvars

class Tab2(ttkthemes.ThemedTk):
    def __init__(self, arg):

        # import global variables
        globalvars.init()

        # create Tab 2
        self.tab2 = tkinter.ttk.Frame(arg)
        arg.add(self.tab2, text = "Regression and Data Plot")

        # create selection frame
        self.selection12_frame = tkinter.ttk.Frame(self.tab2)
        self.selection12_frame.pack()

        ## selection variable
        self.selection12_Value = tkinter.IntVar()

        ## selection 1 button
        self.selection1_button = tkinter.ttk.Radiobutton(self.selection12_frame, text = "Use the Maximum Degree of the Polynomial", variable = self.selection12_Value, value = 1, command = self.selection12_selected, state = tkinter.NORMAL)
        self.selection1_button.grid(row = 0, column = 0)

        ## selection 1 max degree text
        self.selection1_label = tkinter.ttk.Label(self.selection12_frame, text = "999", foreground = "#f5f4f2")
        self.selection1_label.grid(row = 0, column = 1)    

        ## selection 2 button
        self.selection2_button = tkinter.ttk.Radiobutton(self.selection12_frame, text = "Insert the Degree of Polynomial Manually", variable = self.selection12_Value, value = 2, command = self.selection12_selected, state = tkinter.NORMAL)
        self.selection2_button.grid(row = 1, column = 0)     

        ## selection 2 degree entry
        self.selection2_entry = tkinter.ttk.Entry(self.selection12_frame, width = 5, state = tkinter.DISABLED)
        self.selection2_entry.grid(row = 1, column = 1)  

        # plot button
        self.plot_button = tkinter.ttk.Button(self.tab2, text = "Plot", state = tkinter.DISABLED, command = self.plot)
        self.plot_button.pack()

        # plot error message
        self.plot_errormsg = tkinter.ttk.Label(self.tab2, text = "Error: Please input a natural number!", foreground = "#f5f4f2")
        self.plot_errormsg.pack()

        # initial plot
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.fig.patch.set_facecolor("#f5f4f2")
        self.ax.set_facecolor("#f5f4f2")
        plt.axis('off')
        self.canvas = FigureCanvasTkAgg(self.fig, master = self.tab2)
        self.canvas.get_tk_widget().pack(side = tkinter.BOTTOM, fill = tkinter.BOTH, expand = True)
        self.canvas.draw()
    
    def selection12_selected(self):
        print("Hello")
    
    def plot(self):
        print("Hello")