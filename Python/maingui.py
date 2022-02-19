import tkinter, ttkthemes

import tab1, tab2, tab3

class MARS(ttkthemes.ThemedTk):
    def __init__(self):
        super().__init__()

        # configure the root window
        self.title('MARS')
        self.geometry('600x600')
        self.iconphoto(False, tkinter.PhotoImage(file = "logo.png"))
        self.set_theme('radiance')

        # create tab control
        self.tabControl = tkinter.ttk.Notebook(self)

        self.tab1 = tab1.Tab1(self.tabControl)
        self.tab2 = tab2.Tab2(self.tabControl)
        self.tab3 = tab3.Tab3(self.tabControl)

        self.tabControl.pack(expand = 1, fill = "both")

        ## create two buttons
        #self.single_arch_button = tkinter.ttk.Button(self, text = "MARS Single Arch", command = self.single_arch)
        #self.single_arch_button.place(relx = 0.5, rely = 0.5, anchor = tkinter.CENTER)

        #self.multiple_archs_button = tkinter.ttk.Button(self, text = "MARS Multiple Archs")
        #self.multiple_archs_button.place(relx = 0.5, rely = 0.55, anchor = tkinter.CENTER)

    #def single_arch(self):
    #    single_arch_window = tkinter.Toplevel(self)
    #    single_arch_window.title('Arch 1')
    #    single_arch_window.geometry('600x600')
    #    single_arch_window.iconphoto(False, tkinter.PhotoImage(file = "logo.png"))

    #    # create tab control
    #    tabControl = tkinter.ttk.Notebook(single_arch_window)

    #    sa_tab1 = tab1.Tab1(tabControl)
    #    sa_tab2 = tab2.Tab2(tabControl)
    #    sa_tab3 = tab3.Tab3(tabControl)

    #    tabControl.pack(expand = 1, fill = "both")

if __name__ == "__main__":
    app = MARS()
    app.mainloop()