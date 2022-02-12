import tkinter, tkinter.filedialog
import tab1

class MARS(tkinter.Tk):
    def __init__(self):
        super().__init__()

        # configure the root window
        self.title('MARS')
        self.geometry('600x600')

        # create tab control
        self.tabControl = tkinter.ttk.Notebook(self)

        self.tab1 = tab1.Tab1(self.tabControl)


        self.tab2 = tkinter.ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab2, text = "Tab 2")

        self.tab3 = tkinter.ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab3, text = "Tab 3")

        self.tabControl.pack(expand = 1, fill = "both")


if __name__ == "__main__":
    app = MARS()
    app.mainloop()