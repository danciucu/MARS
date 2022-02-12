from tkinter import ttk
from tkinter import Tk
from tkinter import *

# Source: https://djangocentral.com/creating-tabbed-widget-with-python-for-gui-application/
global user_units, count

user_units = ""
count = 0

def main():

    # intializing the window
    window = Tk()
    window.title("MARS")
    window.iconbitmap('C:/Users/dan.ciucu/OneDrive - AECOM Directory/Documents/Projects/CS Development/Masonry Arches AutoCAD Plot/logo4.ico')


    # configuring size of the window
    window.geometry('550x550')


    # Create Tab Control
    TAB_CONTROL = ttk.Notebook(window)


    # Tab1
    TAB1 = ttk.Frame(TAB_CONTROL)
    TAB_CONTROL.add(TAB1, text='Load Data')

    ## Functions
    def R_Selected():
        if tab1RVar.get() == 1:
            tab1E1.config(state = NORMAL)
            Input_button.config(state = DISABLED)
            # To Do: Disable the Treeview
            tab1X.config(state = DISABLED)
            tab1Y.config(state = DISABLED)
            tab1X_entry.config(state = DISABLED)
            tab1Y_entry.config(state = DISABLED)

        else:
            tab1E1.delete(0, 'end')
            tab1E1.config(state = DISABLED)
            Input_button.config(state = NORMAL)
            # To Do: Enable the Treeview
            tab1X.config(state = NORMAL)
            tab1Y.config(state = NORMAL)
            tab1X_entry.config(state = NORMAL)
            tab1Y_entry.config(state = NORMAL)

    def Units_Update(event = None):
        tab1R1.config(state = NORMAL)
        tab1R2.config(state = NORMAL)
        array = ['No', 'X [' + tab1UnitsValue.get() + ']', 'Y [' + tab1UnitsValue.get() + ']']
        tab1Table.heading("x", text = array[1])
        tab1Table.heading("y", text = array[2])
        tab1X.config(text = array[1])
        tab1Y.config(text = array[2])
        user_units = tab1UnitsValue.get()

    def Path_Show():
        print(tab1E1.get())

    def Input_Record():
        global count
        tab1Table.insert(parent = '', index = 'end', iid = count, text = '', values = (count + 1, float(tab1X_entry.get()), float(tab1Y_entry.get())))
        count += 1

        tab1X_entry.delete(0,END)
        tab1Y_entry.delete(0,END)

    ## Units List
    tab1L1 = ttk.Label(TAB1, text = "Please select a dimension:")
    tab1L1.pack()

    tab1UnitsValue = StringVar()
    tab1Units = ttk.Combobox(TAB1, textvariable = tab1UnitsValue, values = ('km', 'hm', 'dam', 'm', 'dm', 'cm', 'mm'))
    tab1Units.pack()
    tab1Units.bind("<<ComboboxSelected>>", Units_Update)

    ## Radio Button 1
    tab1RVar = IntVar()
    tab1R1 = ttk.Radiobutton(TAB1, text = "Import a CSV file", variable = tab1RVar, value = 1, command = R_Selected, state = DISABLED)
    tab1R1.pack()

    ### Input File Path
    tab1E1 = ttk.Entry(TAB1, width = 50, state = DISABLED)
    tab1E1.bind('<Return>', Path_Show)
    tab1E1.pack()

    ##Radio Button 2
    tab1R2 = ttk.Radiobutton(TAB1, text = "Input datapoints (X & Y) manually", variable = tab1RVar, value = 2, command = R_Selected, state = DISABLED)
    tab1R2.pack()

    ### Treeview (table)
    #### Treeview style

    style = ttk.Style(TAB1)

    #### Definition of Treeview
    tab1Table = ttk.Treeview(TAB1)
    tab1Table.pack()

    tab1Table['columns']= ('no', 'x', 'y')
    tab1Table.column("#0", width = 0, stretch = NO)
    tab1Table.column("no", anchor = CENTER, width = 80)
    tab1Table.column("x" , anchor = CENTER, width = 80)
    tab1Table.column("y", anchor = CENTER, width = 80)

    tab1Table.heading("#0", text = "", anchor = CENTER)
    tab1Table.heading("no", text = "No", anchor = CENTER)
    tab1Table.heading("x", text = "X [-]", anchor = CENTER)
    tab1Table.heading("y", text = "Y [-]", anchor = CENTER)

    ### Input Frame
    tab1Input_frame = ttk.Frame(TAB1)
    tab1Input_frame.pack()

    tab1X= ttk.Label(tab1Input_frame ,text = "X [-]", state = DISABLED)
    tab1X.grid(row = 0,column = 1)

    tab1Y = ttk.Label(tab1Input_frame, text = "Y [-]", state = DISABLED)
    tab1Y.grid(row = 0, column = 2)

    tab1X_entry = ttk.Entry(tab1Input_frame, state = DISABLED)
    tab1X_entry.grid(row = 1, column = 1)

    tab1Y_entry = ttk.Entry(tab1Input_frame, state = DISABLED)
    tab1Y_entry.grid(row = 1,column = 2)


    ### Input Button
    Input_button = ttk.Button(TAB1, text = "Input A Point", state = DISABLED, command = Input_Record)

    Input_button.pack()

    ### Error Message
    tab1Error= ttk.Label(TAB1 ,text = "")
    tab1Error.pack()




    # Tab2
    TAB2 = ttk.Frame(TAB_CONTROL)
    TAB_CONTROL.add(TAB2, text='Regression and Data Plot')
    TAB_CONTROL.pack(expand=1, fill="both")


    # Tab3
    TAB3 = ttk.Frame(TAB_CONTROL)
    TAB_CONTROL.add(TAB3, text='Generate AutoCAD Drawing')
    TAB_CONTROL.pack(expand=1, fill="both")


    # Tab Name Labels
    ttk.Label(TAB2, text="This is Tab 2").grid(column=0, row=0, padx=10, pady=10)
    ttk.Label(TAB3, text="This is Tab 3").grid(column=0, row=0, padx=10, pady=10)


    #Calling Main()
    window.mainloop()

main()
