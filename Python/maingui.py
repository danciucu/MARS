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

        # create two buttons
        self.single_arch_button = tkinter.ttk.Button(self, text = "MARS Single Arch", command = self.single_arch)
        self.single_arch_button.place(relx = 0.5, rely = 0.5, anchor = tkinter.CENTER)

        self.multiple_archs_button = tkinter.ttk.Button(self, text = "MARS Multiple Archs", command = self.multiple_arches)
        self.multiple_archs_button.place(relx = 0.5, rely = 0.55, anchor = tkinter.CENTER)

        # create a label
        self.owner_label = tkinter.ttk.Label(self, text = "Created by Dan Ciucu")
        self.owner_label.place(relx = 0.5, rely = 1, anchor = tkinter.S)

    def single_arch(self):
        single_window = tkinter.Toplevel(self)
        single_window.title('Arch 1')
        single_window.geometry('600x600')
        single_window.iconphoto(False, tkinter.PhotoImage(file = "logo.png"))

        # create tab control
        single_tabControl = tkinter.ttk.Notebook(single_window)

        single_tab1 = tab1.Tab1(single_tabControl)
        single_tab2 = tab2.Tab2(single_tabControl)
        single_tab3 = tab3.Tab3(single_tabControl)

        single_tabControl.pack(expand = 1, fill = "both")

        # rerun single_window until the user closes it
        single_window.mainloop()

    def multiple_arches(self):
        multiple_window = tkinter.Toplevel(self)
        multiple_window.title('Arch 1')
        multiple_window.geometry('600x600')
        multiple_window.iconphoto(False, tkinter.PhotoImage(file = "logo.png"))

        # create tab control
        multiple_tabControl = tkinter.ttk.Notebook(multiple_window)

        multiple_tab1 = tab1.Tab1(multiple_tabControl)
        multiple_tab2 = tab2.Tab2(multiple_tabControl)
        multiple_tab3 = tab3.Tab3(multiple_tabControl)

        multiple_tabControl.pack(expand = 1, fill = "both")
        
        # rerun single_window until the user closes it
        multiple_window.mainloop()

if __name__ == "__main__":
    app = MARS()
    app.mainloop()