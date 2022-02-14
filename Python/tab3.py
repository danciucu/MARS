import tkinter, tkinter.filedialog, ttkthemes

import globalvars

class Tab3(ttkthemes.ThemedTk):
    def __init__(self, arg):

        # import global variables
        globalvars.init()

        # create Tab 1
        self.tab3 = tkinter.ttk.Frame(arg)
        arg.add(self.tab3, text = "Load Data")
