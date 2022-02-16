import tkinter, tkinter.filedialog, ttkthemes

import pandas as pd
import ezdxf

import globalvars

class Tab1(ttkthemes.ThemedTk):
    def __init__(self, arg):

        # import global variables
        globalvars.init()

        # create Tab 1
        self.tab1 = tkinter.ttk.Frame(arg)
        arg.add(self.tab1, text = "Load Data")

        # units text and drop-down list
        self.units_label = tkinter.ttk.Label(self.tab1, text = "Please select a unit:")
        self.units_label.pack()

        self.units_ddlistValue = tkinter.StringVar()
        self.units_ddlist = tkinter.ttk.Combobox(self.tab1, textvariable = self.units_ddlistValue, values = ["mm", "cm", "m", "in", "ft", "yd"], justify='center')
        self.units_ddlist.pack()
        self.units_ddlist.bind("<<ComboboxSelected>>", self.units_update)

        # selection variable
        self.selection12_Value = tkinter.IntVar()

        # selection 1 button
        self.selection1_button = tkinter.ttk.Radiobutton(self.tab1, text = "Import a CSV or DXF file", variable = self.selection12_Value, value = 1, command = self.selection12_selected, state = tkinter.DISABLED)
        self.selection1_button.pack()

        # define frame 1
        self.path_frame = tkinter.ttk.Frame(self.tab1)
        self.path_frame.pack()

        ## input file path
        self.path_entry = tkinter.ttk.Entry(self.path_frame, width = 40, state = tkinter.DISABLED)
        self.path_entry.grid(row = 0, column = 0)

        ## open window path button
        self.path_button = tkinter.ttk.Button(self.path_frame, text = "...", state = tkinter.DISABLED, command = self.open_path, width = 2)
        self.path_button.grid(row = 0, column = 1)

        # selection 2 button
        self.selection2_button = tkinter.ttk.Radiobutton(self.tab1, text = "Input datapoints (X & Y) manually", variable = self.selection12_Value, value = 2, command = self.selection12_selected, state = tkinter.DISABLED)
        self.selection2_button.pack()

        # treeview (table) for manual input
        ## define a style to show the table is not functional
        self.style = tkinter.ttk.Style(self.tab1)
        self.disabled_bg = self.style.lookup("TEntry", "fieldbackground", ("disabled",))
        self.disabled_fg = self.style.lookup("TEntry", "foreground", ("disabled",))
        
        self.style.map("Treeview", 
            fieldbackground=[("disabled", self.disabled_bg)],
            foreground=[("disabled", "gray")],
            background=[("disabled", self.disabled_fg)])

        self.style.configure("Treeview.Heading", foreground='gray')
        self.style.configure("Treeview", background = "gray",
            fieldbackground = "gray", foreground = "gray")

        ## define a table frame
        self.table_frame = tkinter.ttk.Frame(self.tab1)
        self.table_frame.pack()

        ## define a scrollbar
        self.table_scrollbar = tkinter.ttk.Scrollbar(self.table_frame)
        self.table_scrollbar.pack(side = tkinter.RIGHT, fill = tkinter.Y)

        ## define the table
        self.table = tkinter.ttk.Treeview(self.table_frame, selectmode = "none", yscrollcommand = self.table_scrollbar.set)
        self.table.pack()

        self.table["columns"] = ("no", "x", "y")
        self.table.column("#0", width = 0, stretch = tkinter.NO)
        self.table.column("no", width = 80, stretch = tkinter.NO)
        self.table.column("x" , anchor = tkinter.CENTER, width = 80, stretch = tkinter.NO)
        self.table.column("y", anchor = tkinter.CENTER, width = 80, stretch = tkinter.NO)

        self.table.heading("#0", text = "", anchor = tkinter.CENTER)
        self.table.heading("no", text = "No", anchor = tkinter.CENTER)
        self.table.heading("x", text = "X [-]", anchor = tkinter.CENTER)
        self.table.heading("y", text = "Y [-]", anchor = tkinter.CENTER)

        ## configure the scrollbar
        self.table_scrollbar.config(command = self.table.yview)

        # define input frame
        self.input_frame = tkinter.ttk.Frame(self.tab1)
        self.input_frame.pack()

        ## entry values for x and y
        self.x_label = tkinter.ttk.Label(self.input_frame, text = "X [-]", state = tkinter.DISABLED)
        self.x_label.grid(row = 0, column = 0)

        self.y_label = tkinter.ttk.Label(self.input_frame, text = "Y [-]", state = tkinter.DISABLED)
        self.y_label.grid(row = 0, column = 1)

        self.x_entry = tkinter.ttk.Entry(self.input_frame, state = tkinter.DISABLED, justify = 'center')
        self.x_entry.grid(row = 1, column = 0)

        self.y_entry = tkinter.ttk.Entry(self.input_frame, state = tkinter.DISABLED, justify = 'center')
        self.y_entry.grid(row = 1, column = 1)

        # command frame
        self.command_frame = tkinter.ttk.Frame(self.tab1)
        self.command_frame.pack()

        ## input, delete & delete all buttons
        self.input_button = tkinter.ttk.Button(self.command_frame, text = "Insert A Point", state = tkinter.DISABLED, command = self.input_record)
        self.input_button.grid(row = 0, column = 0, padx = 10, pady = 10)

        self.delete_button = tkinter.ttk.Button(self.command_frame, text = "Delete A Point", state = tkinter.DISABLED, command = self.delete_record)
        self.delete_button.grid(row = 0, column = 1, padx = 10, pady = 10)

        self.deleteall_button = tkinter.ttk.Button(self.command_frame, text = "Delete All Points", state = tkinter.DISABLED, command = self.deleteall_records)
        self.deleteall_button.grid(row = 0, column = 2, padx = 10, pady = 10)

        ## error message if input is not a float()
        self.error = tkinter.ttk.Label(self.tab1, text = "Error: Please imput a rational number!", foreground = "#f5f4f2")
        self.error.pack()

    def units_update(self, arg):
        arg = self.units_ddlistValue.get()

        # define a dictionary (hash table) for searching the units
        user_units_dict = {"mm": 1, "cm": 10, "m": 1000, "in": 25.4, "ft": 304.8, "yd": 914.4}
        
        # store the value selected by the user into a global variable
        globalvars.user_units = arg 
        # search for the magnification factor and update global variable
        globalvars.units_coef = user_units_dict[globalvars.user_units]
                
        # enable selection buttons
        self.selection1_button.config(state = tkinter.NORMAL)
        self.selection2_button.config(state = tkinter.NORMAL)

        # change the units for x and y
        array = ["No", "X [" + arg + "]", "Y [" + arg + "]"] 
        self.table.heading("x", text = array[1])
        self.table.heading("y", text = array[2])
        self.x_label.config(text = array[1])
        self.y_label.config(text = array[2])
    
    def selection12_selected(self):
        # if first selection button pressed
        if self.selection12_Value.get() == 1:
            # delete all the data recored
            globalvars.count = 0
            globalvars.array_x = []
            globalvars.array_y = []

            # enable path functions
            self.path_entry.config(state = tkinter.NORMAL)
            self.path_button.config(state = tkinter.NORMAL)

            # delete all the values frp, the table
            for record in self.table.get_children():
                self.table.delete(record)

            # change the table style
            self.style.configure("Treeview.Heading", foreground='grey')
            self.style.configure("Treeview", background = "gray",
                        fieldbackground = "gray", foreground = "gray")
            
            # disable x and y functions
            self.x_label.config(state = tkinter.DISABLED)
            self.x_entry.config(state = tkinter.DISABLED)
            self.y_label.config(state = tkinter.DISABLED)
            self.y_entry.config(state = tkinter.DISABLED)

            # disable input, delete & delete all buttons
            self.input_button.config(state = tkinter.DISABLED)
            self.delete_button.config(state = tkinter.DISABLED)
            self.deleteall_button.config(state = tkinter.DISABLED)

            # change the color of the error back to gray to hide it
            self.error.config(foreground = "#f0f0ed")

        # if second selection button pressed
        else:
            # delete all the data recored
            globalvars.count = 0
            globalvars.array_x = []
            globalvars.array_y = []

            # clean and disable the path functions
            self.path_entry.delete(0, 'end')
            self.path_entry.config(state = tkinter.DISABLED)
            self.path_button.config(state = tkinter.DISABLED)

            # change the table style
            self.style.configure("Treeview.Heading", foreground='black')
            self.style.configure("Treeview", background = "white",
                        fieldbackground = "white", foreground = "black")

            # enable x and y functions
            self.x_label.config(state = tkinter.NORMAL)
            self.x_entry.config(state = tkinter.NORMAL)
            self.y_label.config(state = tkinter.NORMAL)
            self.y_entry.config(state = tkinter.NORMAL)

            # enable input, delete & delete all buttons
            self.input_button.config(state = tkinter.NORMAL)
            self.delete_button.config(state = tkinter.NORMAL)
            self.deleteall_button.config(state = tkinter.NORMAL)

    def open_path(self):
        # variable to store the path user opens
        path = tkinter.filedialog.askopenfilename(filetypes = (
            ("DXF Files", "*.DXF"),
            ("CSV Files", "*.CSV")
        ))
        
        # fill the entry bar with the path
        self.path_entry.insert(tkinter.END, path)

        try:
            # try to see if the file is DXF type
            doc = ezdxf.readfile(path)
            msp = doc.modelspace()
            # check for the "crosses" in the DXF file
            query = msp.query("INSERT[name=='CROSS']")
            
            # a variable to count the points
            count = 0
            # arrays to store the coorinates of the points locally
            array_x = []
            array_y = []
            array_z = []
            # variables to store the first coodinate and move the arch back to origin
            origin_x = 0
            origin_y = 0
            origin_z = 0
            # variables to store the second element after positioning again to origin
            second_x = 0
            second_y = 0
            second_z = 0
            
            # populate local arrays with the values of the points
            for point in query:
                array_x.append(float(point.dxf.insert.x))
                array_y.append(float(point.dxf.insert.y))
                array_z.append(float(point.dxf.insert.z))
                # set the origin to the first element
                if count == 0:
                    origin_x = array_x[0]
                    origin_y = array_y[0]
                    origin_z = array_z[0]
                # set up the second element
                if count == 1:
                    second_x = array_x[count] - origin_x
                    second_y = array_y[count] - origin_y
                    second_z = array_z[count] - origin_z
                # check the sign of second element and swich the sign if negative
                # set the local arrays to the origin and start with (0, 0, 0)
                ## for array_x
                if second_x < 0:
                    array_x[count] = -(array_x[count] - origin_x)
                else:
                    array_x[count] = array_x[count] - origin_x
                ## for array_y
                if second_y < 0:
                    array_y[count] = -(array_y[count] - origin_y)
                else:
                    array_y[count] = array_y[count] - origin_y
                ## for array_z
                if second_z < 0:
                    array_z[count] = -(array_z[count] - origin_z)
                else:
                    array_z[count] = array_z[count] - origin_z
                
                count += 1

            # update the global variable
            globalvars.count = count

            # check for the final element and if it's the biggest from all arrays, then that's globalvars.array_x
            if (abs(array_x[globalvars.count - 1]) > abs(array_y[globalvars.count - 1])) and (abs(array_x[globalvars.count - 1]) > abs(array_z[globalvars.count - 1])):
                globalvars.array_x = array_x
            elif (abs(array_y[globalvars.count - 1]) > abs(array_x[globalvars.count - 1])) and (abs(array_y[globalvars.count - 1]) > abs(array_z[globalvars.count - 1])):
                globalvars.array_x = array_y
            else:
                globalvars.array_x = array_z

            # check if first and last elements are equal and next pair is not equal, then that's globalvars.array_y
            if int(array_x[0]) == int(array_x[globalvars.count - 1])  and int(array_x[1]) != int(array_x[globalvars.count - 2]):
                globalvars.array_y = array_x
            elif int(array_y[0]) == int(array_y[globalvars.count - 1]) and int(array_y[1]) != int(array_y[globalvars.count - 2]):
                globalvars.array_y = array_y
            else:
                globalvars.array_y = array_z

        except OSError:
            # if not DXF then CSV and open the csv fie
            arch_data = pd.read_csv(path, header=0, names=["x", "y"])
            # update global variables
            globalvars.array_x = arch_data['x'].values
            globalvars.array_y = arch_data['y'].values
            globalvars.count = len(globalvars.array_x)

    def input_record(self):
        # define a bool variable to check if input is float()
        check = False
        # change the color of the error back to gray to hide it
        self.error.config(foreground = "#f0f0ed")
        try:
            input_x = float(self.x_entry.get())
            input_y = float(self.y_entry.get())
            check = True
        except ValueError:
            # make the error "appear" since input is not a float()
            self.error.config(foreground = "black")
        
        # update units
        if check == True:
            # insert values with center alignment
            self.table.column("no" , anchor = tkinter.CENTER)
            self.table.column("x" , anchor = tkinter.CENTER)
            self.table.column("y", anchor = tkinter.CENTER)
            self.table.insert(parent = '', index = 'end', iid = globalvars.count, text = '', values = (globalvars.count + 1, input_x, input_y))

            # clean the input boxes
            self.x_entry.delete(0, tkinter.END)
            self.y_entry.delete(0, tkinter.END)

            # upadte the global variables
            globalvars.count += 1
            globalvars.array_x.append(input_x)
            globalvars.array_y.append(input_y)

            # move to the bottom of the table
            self.table.yview_moveto(globalvars.count + 1)

    def delete_record(self):
        # check if there are any values left to delete
        if globalvars.count == 0:
            return
        # delete the last value from the table
        else:
            self.table.delete(globalvars.count - 1)

            # update the global variables
            globalvars.count -= 1
            globalvars.array_x.pop(globalvars.count - 1)
            globalvars.array_y.pop(globalvars.count - 1)

    def deleteall_records(self):
        # delete all values from the table
        for record in self.table.get_children():
            self.table.delete(record)
        
        # update the global variables
        globalvars.count = 0
        globalvars.array_x = []
        globalvars.array_y = []