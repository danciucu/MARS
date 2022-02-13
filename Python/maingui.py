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


if __name__ == "__main__":
    app = MARS()
    app.mainloop()