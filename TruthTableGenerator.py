import sys
import os
from tkinter import Tk, Button, Entry, E, W, N, S, INSERT, PhotoImage, Menu, \
    StringVar, Frame, Canvas, GROOVE
from AutoScrollBar import AutoScrollbar
program_directory = sys.path[0]


def insert_text(field, text):
    field.insert(INSERT, text)
    return


def validate(text):
    raise Exception("Input recieved: {}".format(text))


def test():
    print("This is a test?!?!?")


class TruthTableGeneratorGUI:
    def __init__(self, root):
        self.root = root
        root.title("Truth Table Generator")
        root.iconphoto(True, PhotoImage(file=os.path.join(program_directory,
                                                          "icon.png")))

        # create a menu bar
        menubar = Menu(root)

        # create the file menu
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=root.quit)

        # create the help menu
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help", command=test)
        helpmenu.add_command(label="About", command=test)

        # attach the menus to the menu bar
        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_cascade(label="Help", menu=helpmenu)
        menubar.add_command(label="test", command=test)

        root.config(menu=menubar)

        # create the table area and scrollbars
        tableframe = Frame(root, relief=GROOVE, padx=5, pady=5, bd=2)
        tableframe.grid(row=3, column=0, columnspan=5, sticky=E+W+N+S)

        root.grid_rowconfigure(3, weight=1)
        tableframe.grid_rowconfigure(0, weight=1)
        tableframe.grid_columnconfigure(0, weight=1)

        # make the scroll bars
        tablevsb = AutoScrollbar(tableframe, orient="vertical")
        tablehsb = AutoScrollbar(tableframe, orient="horizontal")

        tablevsb.grid(row=0, column=1, sticky=N+S)
        tablehsb.grid(row=1, column=0, sticky=E+W)

        # make the canvas that will hold the window with the table in it
        self.tablecanvas = Canvas(tableframe,
                                  yscrollcommand=tablevsb.set,
                                  xscrollcommand=tablehsb.set)
        self.tablecanvas.grid(row=0, column=0, sticky=N+S+E+W)

        tablevsb.config(command=self.tablecanvas.yview)
        tablehsb.config(command=self.tablecanvas.xview)

        # declaring and defining widgets
        sv = StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv: generate(sv))
        self.entry = Entry(root, textvariable=sv)

        self.p_button = Button(root, text="p", width=1,
                               command=lambda: insert_text(self.entry, 'p '))

        self.q_button = Button(root, text="q", width=1,
                               command=lambda: insert_text(self.entry, 'q '))

        self.and_button = Button(root, text="AND", width=1,
                                 command=lambda: insert_text(self.entry,
                                                             ' /\ '))

        self.or_button = Button(root, text="OR", width=1,
                                command=lambda: insert_text(self.entry,
                                                            ' \/ '))

        self.not_button = Button(root, text="NOT", width=1,
                                 command=lambda: insert_text(self.entry,
                                                             ' ~ '))

        self.left_paren_button = Button(root, text="(", width=1,
                                        command=lambda: insert_text(self.entry,
                                                                    '('))

        self.right_paren_button = Button(root, text=")", width=1,
                                         command=lambda:
                                         insert_text(self.entry, ')'))

        self.if_button = Button(root, text="IF", width=1,
                                command=lambda: insert_text(self.entry,
                                                            ' -> '))

        self.iff_button = Button(root, text="IFF", width=1,
                                 command=lambda: insert_text(self.entry,
                                                             ' <-> '))

        self.generate_button = Button(root, text="GO!",
                                      command=self.generate_table)

        # adding widgets to the grid
        self.p_button.grid(row=1, column=0, sticky=E+W+N+S)
        self.q_button.grid(row=1, column=1, sticky=E+W)
        self.and_button.grid(row=1, column=2, sticky=E+W)
        self.or_button.grid(row=1, column=3, sticky=E+W)
        self.not_button.grid(row=1, column=4, sticky=E+W)
        self.left_paren_button.grid(row=2, column=0, sticky=E+W)
        self.right_paren_button.grid(row=2, column=1, sticky=E+W)
        self.if_button.grid(row=2, column=3, sticky=E+W)
        self.iff_button.grid(row=2, column=4, sticky=E+W)
        self.generate_button.grid(row=0, column=4, sticky=E+W)
        self.entry.grid(row=0, column=0, columnspan=4, sticky=E+W+N+S)

        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_columnconfigure(2, weight=1)
        root.grid_columnconfigure(3, weight=1)
        root.grid_columnconfigure(4, weight=1)

    def generate_table(self):
        # clear the canvas of past tables
        self.tablecanvas.delete("all")

        # create the frame to hold the table
        frame = Frame(self.tablecanvas)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        # PLACE HOLDER FOR REAL TABLE GENERATION
        for i in range(25):
            Button(frame, text=i).grid(row=i, column=i)

        # make the window that holds the frame
        self.tablecanvas.create_window(0, 0, window=frame, anchor=N+W)
        frame.update_idletasks()

        # update the scrollable area to the new width
        self.tablecanvas.config(scrollregion=self.tablecanvas.bbox("all"))


if __name__ == "__main__":
    root = Tk()
    # root.resizable(width=False, height=False)
    # root.geometry('{}x{}'.format(400, 500))

    # create the GUI
    gui = TruthTableGeneratorGUI(root)

    # start the main loop
    root.mainloop()
