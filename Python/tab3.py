import tkinter, tkinter.filedialog, ttkthemes

import csv
import pyautocad
import win32com.client
import numpy as np

import globalvars

class Tab3(ttkthemes.ThemedTk):
    def __init__(self, arg):

        # import global variables
        globalvars.init()

        # create Tab 2
        self.tab3 = tkinter.ttk.Frame(arg)
        arg.add(self.tab3, text = "Generate AutoCAD Drawing")

        # input frame
        self.input_frame = tkinter.ttk.Frame(self.tab3)
        self.input_frame.pack()

        ## input entry
        self.input_entry = tkinter.ttk.Entry(self.input_frame, width = 50, text = "Enter the path where you want to save the CSV file")
        self.input_entry.grid(row = 0, column = 0)

        ## input filepath button
        self.input_button = tkinter.ttk.Button(self.input_frame, text = "...", state = tkinter.NORMAL, command = self.folder_path, width = 2)
        self.input_button.grid(row = 0, column = 1)

        # CSV generate button
        self.csv_button = tkinter.ttk.Button(self.tab3, text = "Generate CSV file", command = self.generate_csv)
        self.csv_button.pack()

        # error message
        self.csv_error = tkinter.ttk.Label(self.tab3, text = "Error: Nothing yet!", foreground = "#f5f4f2")
        self.csv_error.pack()

        # CAD generate button
        self.cad_button = tkinter.ttk.Button(self.tab3, text = "Generate AutoCAD drawing", command = self.generate_cad)
        self.cad_button.pack()

    def folder_path(self):
        # open the file path
        folder_path = tkinter.filedialog.askdirectory()
        # update the input entry box
        self.input_entry.insert(tkinter.END, folder_path)

    def generate_csv(self):
        # get the file path
        csv_path = self.input_entry.get()
        # create a CSV file named "Arch 1"
        with open(csv_path + "/Arch1.csv", "w", newline = "") as my_csv:
            writer = csv.writer(my_csv)
            # name the first row as X [units] and Y [units]
            writer.writerow(["X [" + globalvars.user_units + "]", "Y [" + globalvars.user_units + "]"])
            for i in range(globalvars.count):
                # add the values
                writer.writerow([globalvars.array_x[i], globalvars.array_y[i]])
    
    def generate_cad(self):
        # update units for the x and y coordinates
        array_x_units = [elements * globalvars.units_coef for elements in globalvars.array_x]
        array_y_units = [elements * globalvars.units_coef for elements in globalvars.array_y]
        # recreate the magnified shape
        polynome = np.polyfit(array_x_units, array_y_units, globalvars.user_degree)
        p = np.poly1d(polynome)
        # prepare the location of the points for AutoCAD draw
        for i in range(globalvars.no):
            globalvars.points_x[i] = i * max(array_x_units) / 8
            globalvars.points_y[i] = p(globalvars.points_x[i])
            globalvars.points_xyz[i * 3] =globalvars. points_x[i]
            if i != globalvars.no - 1:
                globalvars.points_xyz[(i * 3) + 1] = globalvars.points_y[i]
                globalvars.points_xyz[(i * 3) + 2] = 0 
        # open the AutoCAD file
        AutoCAD = win32com.client.Dispatch("AutoCAD.Application")
        # variable to refer to the app
        acad = pyautocad.Autocad(create_if_not_exists = False)
        # aDouble returns array.array of doubles (‘d’ code) for passing to AutoCAD
        p1 = pyautocad.aDouble(globalvars.points_xyz)
        # create a spline through the points of interest with 0 curvature at the ends
        sp1 = acad.model.AddSpline(p1, pyautocad.APoint(0, 0, 0),  pyautocad.APoint(0, 0, 0))
        # ???
        AutoCAD.Visible = True