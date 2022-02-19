import tkinter, tkinter.filedialog, ttkthemes

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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
        # update global variable
        if globalvars.count == 0:
            globalvars.max_degree = 0
        else:
            globalvars.max_degree = globalvars.count - 1

        # if first selection button pressed
        if self.selection12_Value.get() == 1:
            # disable seletion 2 input
            self.selection2_entry.config(state = tkinter.DISABLED)

            # "hide" the plot error
            self.plot_errormsg.config(foreground = "#f5f4f2")

            # modify selection 1 text & plot button
            self.selection1_label.config(text = str(globalvars.max_degree), foreground = "black")
            self.plot_button.config(state = tkinter.NORMAL)
        
        # if second selection button pressed
        else:
            # "hide" plot error & selection 1 text
            self.plot_errormsg.config(foreground = "#f5f4f2")
            self.selection1_label.config(foreground = "#f5f4f2")

            # enable seletion 2 input & plot button
            self.selection2_entry.config(state = tkinter.NORMAL)
            self.plot_button.config(state = tkinter.NORMAL)

    def plot(self):
        # define a bool variable
        test = False

        # update global variable
        if globalvars.count == 0:
            globalvars.max_degree = 0
        else:
            globalvars.max_degree = globalvars.count - 1

        # if second selection button pressed
        if self.selection12_Value.get() != 1:
            try:
                degree = int(self.selection2_entry.get())
                # check if the degree is positive
                if degree < 0:
                    # update the plot error
                    self.plot_errormsg.config(text = "Error: Please input a natural number! Positive number are not natural!" ,foreground = "black")
                elif degree > globalvars.max_degree:
                    # update the plot error
                    self.plot_errormsg.config(text = "Error: The maximum degree of the polynomial is " + str(globalvars.max_degree) +". Reduce the degree!", foreground = "black")
                else:
                    test = True
                    
            except ValueError:
                # update the plot error
                self.plot_errormsg.config(text = "Error: Please input a natural number!" ,foreground = "black")

            # if user inputed a natural number for the degree of polinomyal
            if test == True:
                # change the text of the plot button
                self.plot_button.config(text = "Replot")
                # "hide" plot error
                self.plot_errormsg.config(foreground = "#f5f4f2")
                # plot the graph
                self.graph(degree)
            
        else:
            # change the text of the plot button
            self.plot_button.config(text = "Replot")
            # plot the graph
            self.graph(globalvars.max_degree)
        
    def graph(self, arg):
        # define a variable to store the degree
        globalvars.user_degree = arg
        # make the plot "appear"
        self.fig.patch.set_facecolor("white")
        self.ax.set_facecolor("white")
        plt.axis("on")

        # clear the previous plot and update it
        self.ax.clear()
        polynome = np.polyfit(globalvars.array_x, globalvars.array_y, globalvars.user_degree)
        p = np.poly1d(polynome)
        xp = np.linspace(0, max(globalvars.array_x), 100)
        self.ax.plot(globalvars.array_x, globalvars.array_y, 'o', label = 'Input Points')
        self.ax.plot(xp, p(xp), label = 'Interpolated Shape')
        plt.xlabel("Span [" + globalvars.user_units + "]")
        plt.ylabel("Height [" + globalvars.user_units + "]")
        plt.xlim(0, max(globalvars.array_x))
        plt.ylim(0, max(globalvars.array_y) * 2)
        plt.legend(loc = 'upper right')

        # update canvas
        self.canvas.get_tk_widget().pack(side = tkinter.BOTTOM, fill = tkinter.BOTH, expand = True)
        self.canvas.draw()