import tkinter, tkinter.filedialog
import pandas as pd
import globalvars

class Tab1(tkinter.Tk):
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
        self.units_ddlist = tkinter.ttk.Combobox(self.tab1, textvariable = self.units_ddlistValue, values = ["mm", "cm", "dm", "m", "dam", "hm", "km"])
        self.units_ddlist.pack()
        self.units_ddlist.bind("<<ComboboxSelected>>", self.units_update)

        # selection variable
        self.selection12_Value = tkinter.IntVar()

        # selection 1 button
        self.selection1_button = tkinter.Radiobutton(self.tab1, text = "Import a CSV or DXF file", variable = self.selection12_Value, value = 1, command = self.selection12_selected, state = tkinter.DISABLED)
        self.selection1_button.pack()

        # define frame 1
        self.path_frame = tkinter.Frame(self.tab1)
        self.path_frame.pack()

        ## input file path
        self.path_entry = tkinter.Entry(self.path_frame, width = 40, state = tkinter.DISABLED)
        self.path_entry.grid(row = 0, column = 0)

        ## open window path button
        self.path_button = tkinter.Button(self.path_frame, text = "...", state = tkinter.DISABLED, command = self.open_path, width = 2)
        self.path_button.grid(row = 0, column = 1)

        # selection 2 button
        self.selection2_button = tkinter.Radiobutton(self.tab1, text = "Input datapoints (X & Y) manually", variable = self.selection12_Value, value = 2, command = self.selection12_selected, state = tkinter.DISABLED)
        self.selection2_button.pack()

        # treeview (table) for manual input
        ## define a style to show the table is not functional
        self.style = tkinter.ttk.Style()
        self.disabled_bg = self.style.lookup("TEntry", "fieldbackground", ("disabled",))
        self.disabled_fg = self.style.lookup("TEntry", "foreground", ("disabled",))
        
        self.style.map("Treeview", 
            fieldbackground=[("disabled", self.disabled_bg)],
            foreground=[("disabled", "gray")],
            background=[("disabled", self.disabled_fg)])

        self.style.configure("Treeview.Heading", foreground='gray')
        self.style.configure("Treeview", background = "gray",
            fieldbackground = "gray", foreground = "gray")
        
        ## define the table
        self.table = tkinter.ttk.Treeview(self.tab1, selectmode = "none")
        self.table.pack()

        self.table["columns"] = ("no", "x", "y")
        self.table.column("#0", width = 0, stretch = tkinter.NO)
        self.table.column("no", anchor = tkinter.CENTER, width = 80)
        self.table.column("x" , anchor = tkinter.CENTER, width = 80)
        self.table.column("y", anchor = tkinter.CENTER, width = 80)

        self.table.heading("#0", text = "", anchor = tkinter.CENTER)
        self.table.heading("no", text = "No", anchor = tkinter.CENTER)
        self.table.heading("x", text = "X [-]", anchor = tkinter.CENTER)
        self.table.heading("y", text = "Y [-]", anchor = tkinter.CENTER)

        # define frame 2
        self.input_frame = tkinter.Frame(self.tab1)
        self.input_frame.pack()

        ## entry values for x and y
        self.x_label = tkinter.Label(self.input_frame, text = "X [-]", state = tkinter.DISABLED)
        self.x_label.grid(row = 0, column = 0)

        self.y_label = tkinter.Label(self.input_frame, text = "Y [-]", state = tkinter.DISABLED)
        self.y_label.grid(row = 0, column = 1)

        self.x_entry = tkinter.Entry(self.input_frame, state = tkinter.DISABLED)
        self.x_entry.grid(row = 1, column = 0)

        self.y_entry = tkinter.Entry(self.input_frame, state = tkinter.DISABLED)
        self.y_entry.grid(row = 1, column = 1)

        # command frame
        self.command_frame = tkinter.Frame(self.tab1)
        self.command_frame.pack()

        ## input, delete & delete all buttons
        self.input_button = tkinter.Button(self.command_frame, text = "Insert A Point", state = tkinter.DISABLED, command = self.input_record)
        self.input_button.grid(row = 0, column = 0, padx = 10, pady = 10)

        self.delete_button = tkinter.Button(self.command_frame, text = "Delete A Point", state = tkinter.DISABLED, command = self.delete_record)
        self.delete_button.grid(row = 0, column = 1, padx = 10, pady = 10)

        self.deleteall_button = tkinter.Button(self.command_frame, text = "Delete All Points", state = tkinter.DISABLED, command = self.deleteall_records)
        self.deleteall_button.grid(row = 0, column = 2, padx = 10, pady = 10)

    def units_update(self, arg):
        arg = self.units_ddlistValue.get()
        globalvars.user_units = arg # store the value selected by the user into a global variable

        # enable selection buttons
        self.selection1_button.config(state = tkinter.NORMAL)
        self.selection2_button.config(state = tkinter.NORMAL)

        array = ["No", "X [" + arg + "]", "Y [" + arg + "]"] # array to change the titles of the table and add units
        print(arg)
    
    def selection12_selected(self):
        if self.selection12_Value.get() == 1:
            # delete all the data recored
            globalvars.count = 0
            globalvars.array_x = []
            globalvars.array_y = []

            # enable path functions
            self.path_entry.config(state = tkinter.NORMAL)
            self.path_button.config(state = tkinter.NORMAL)

            # change the table style
            self.style.configure("Treeview.Heading", foreground='grey')
            self.table.state(("disabled",))
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
            self.table.state(("!disabled",))
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
        print("Hello")
    
    def input_record(self):
        print("Hello")

    def delete_record(self):
        print("Hello") 

    def deleteall_records(self):
        print("Hello")


