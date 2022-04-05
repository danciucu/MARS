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

        # csv error message
        self.csv_error = tkinter.ttk.Label(self.tab3, text = "Error: Nothing yet!", foreground = "#f5f4f2")
        self.csv_error.pack()

        # pier frame
        self.pier_frame = tkinter.ttk.Frame(self.tab3)
        self.pier_frame.pack()

        ## pier height text
        self.pier_height_label1 = tkinter.ttk.Label(self.pier_frame, text = "Pier Height :")
        self.pier_height_label1.grid(row = 0, column = 0)

        ## pier height entry box
        self.pier_height_entry = tkinter.ttk.Entry(self.pier_frame, width = 10, justify = 'center')
        self.pier_height_entry.grid(row = 0, column = 1)
        
        ## pier height units
        self.pier_height_label2 = tkinter.ttk.Label(self.pier_frame, text = "mm")
        self.pier_height_label2.grid(row = 0, column = 2)

        ## pier width text
        self.pier_width_label1 = tkinter.ttk.Label(self.pier_frame, text = "Pier Width :")
        self.pier_width_label1.grid(row = 1, column = 0)

        ## pier width entry box
        self.pier_width_entry = tkinter.ttk.Entry(self.pier_frame, width = 10, justify = 'center')
        self.pier_width_entry.grid(row = 1, column = 1)
        
        ## pier width units
        self.pier_width_label2 = tkinter.ttk.Label(self.pier_frame, text = "mm")
        self.pier_width_label2.grid(row = 1, column = 2)

        ## arch barrel text
        self.archbarrel_label1 = tkinter.ttk.Label(self.pier_frame, text = "Arch Barrel Thickness :")
        self.archbarrel_label1.grid(row = 2, column = 0)

        ## arch barrel entry box
        self.archbarrel_entry = tkinter.ttk.Entry(self.pier_frame, width = 10, justify = 'center')
        self.archbarrel_entry.grid(row = 2, column = 1)
        
        ## arch barrel units
        self.archbarrel_label2 = tkinter.ttk.Label(self.pier_frame, text = "mm")
        self.archbarrel_label2.grid(row = 2, column = 2)

        # pier & arch barrel error message
        self.pier_error = tkinter.ttk.Label(self.tab3, text = "Error: Please input a rational number!", foreground = "#f5f4f2")
        self.pier_error.pack()

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
        # interpolate for the nine points of interest
        self.interp_nine_points(globalvars.array_x, globalvars.array_y, 0, 0)
        # create a CSV file named "Arch 1"
        with open(csv_path + "/Arch1.csv", "w", newline = "") as my_csv:
            writer = csv.writer(my_csv)
            # name the first row as X [units] and Y [units]
            writer.writerow(["X [" + globalvars.user_units + "]", "Y [" + globalvars.user_units + "]"])
            for i in range(globalvars.no):
                # add the values
                writer.writerow([globalvars.points_x[i], globalvars.points_y[i]])
    
    def generate_cad(self):
        test = False
        # hide the pier error 
        self.pier_error.config(foreground = "#f5f4f2")
        # check if the pier height & width are float() data type
        try: 
            pier_height = float(self.pier_height_entry.get())
            pier_width = float(self.pier_width_entry.get())
            arch_barrel = float(self.archbarrel_entry.get())
            test = True
        except ValueError:
            self.pier_error.config(foreground = "black")

        if test == True:
            # update units for the x and y coordinates
            array_x_units = [elements * globalvars.units_coef for elements in globalvars.array_x]
            array_y_units = [elements * globalvars.units_coef for elements in globalvars.array_y]
            # interpolate for the nine points of interest
            self.interp_nine_points(array_x_units, array_y_units, pier_width, pier_height)
            # open the AutoCAD file
            AutoCAD = win32com.client.Dispatch("AutoCAD.Application")
            AutoCAD.Visible = True
            # variable to refer to the app
            acad = pyautocad.Autocad(create_if_not_exists = False)
            # set of points for pier width
            p_width1 = pyautocad.APoint(0, 0)
            p_width2 = pyautocad.APoint(pier_width, 0)
            p_width3 = pyautocad.APoint(max(globalvars.points_x) + pier_width, 0)
            p_width4 = pyautocad.APoint(max(globalvars.points_x) + 2 * pier_width, 0)
            # set of points for pier height
            p_height1 = pyautocad.APoint(0, pier_height)
            p_height2 = pyautocad.APoint(pier_width, pier_height)
            p_height3 = pyautocad.APoint(max(globalvars.points_x) + pier_width, pier_height)
            p_height4 = pyautocad.APoint(max(globalvars.points_x) + 2 * pier_width, pier_height)
            # pier lines
            line_width1 = acad.model.AddLine(p_width1, p_width2)
            line_width2 = acad.model.AddLine(p_width3, p_width4)
            line_height1 = acad.model.AddLine(p_width1, p_height1)
            line_height2 = acad.model.AddLine(p_width2, p_height2)
            line_height3 = acad.model.AddLine(p_width3, p_height3)
            line_height4 = acad.model.AddLine(p_width4, p_height4)
            # aDouble returns array.array of doubles (‘d’ code) for passing to AutoCAD
            p1_arch = pyautocad.aDouble(globalvars.points_xyz)
            # create a spline through the points of interest with 0 curvature at the ends
            sp1 = acad.model.AddSpline(p1_arch, pyautocad.APoint(0, 0, 0),  pyautocad.APoint(0, 0, 0))
            try:
                sp2 = sp1.Offset(-arch_barrel)
            except:
                pass

            t1 = acad.model.AddText(globalvars.points_x[4], p_height4, globalvars.units_coef / 10)
        
    def interp_nine_points(self, array_x_units, array_y_units, pier_width, pier_height):
        # reset the global variables
        globalvars.points_x = [0] * globalvars.no
        globalvars.points_y = [0] * globalvars.no
        globalvars.points_xyz = [0] * globalvars.no * 3
        # recreate the magnified shape
        polynome = np.polyfit(array_x_units, array_y_units, globalvars.user_degree)
        p = np.poly1d(polynome)
        # prepare the location of the points for AutoCAD draw
        for i in range(globalvars.no):
            globalvars.points_x[i] = i * max(array_x_units) / 8 
            globalvars.points_y[i] = p(globalvars.points_x[i]) 
            globalvars.points_xyz[i * 3] = globalvars.points_x[i] + pier_width
            globalvars.points_xyz[i * 3 + 1] = globalvars.points_y[i] + pier_height
            globalvars.points_xyz[i * 3 + 2] = 0
            if i == globalvars.no - 1:
                globalvars.points_xyz[(i * 3) + 1] = int(self.pier_height_entry.get())
