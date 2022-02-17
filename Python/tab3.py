import tkinter, tkinter.filedialog, ttkthemes

import csv
import pyautocad
import win32com.client

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
        print("Hello")