import sys
import os
from tkinter import Tk, Button, Entry, E, W, N, S, INSERT, PhotoImage, Menu
from tkinter import StringVar


def insert_text(field, text):
    field.insert(INSERT, text)
    return


def validate(text):
    raise Exception("Input recieved: {}".format(text))


def generate(textfield):
    try:
        validate(textfield.get())
        print("VALID")
    except Exception as ex:
        print(str(ex))


def callback(sv):
    print(sv.get())


def test():
    print("This is a test?!?!?")


class TruthTableGeneratorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Truth Table Generator")

        # create a menu bar
        menubar = Menu(master)

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

        master.config(menu=menubar)

        # declaring and defining widgets
        sv = StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv: generate(sv))
        self.entry = Entry(master, textvariable=sv)

        self.p_button = Button(master, text="p", width=1,
                               command=lambda: insert_text(self.entry, 'p '))

        self.q_button = Button(master, text="q", width=1,
                               command=lambda: insert_text(self.entry, 'q '))

        self.and_button = Button(master, text="AND", width=1,
                                 command=lambda: insert_text(self.entry,
                                                             ' /\ '))

        self.or_button = Button(master, text="OR", width=1,
                                command=lambda: insert_text(self.entry,
                                                            ' \/ '))

        self.not_button = Button(master, text="NOT", width=1,
                                 command=lambda: insert_text(self.entry,
                                                             ' ~ '))

        self.left_paren_button = Button(master, text="(", width=1,
                                        command=lambda: insert_text(self.entry,
                                                                    '('))

        self.right_paren_button = Button(master, text=")", width=1,
                                         command=lambda:
                                         insert_text(self.entry, ')'))

        self.if_button = Button(master, text="IF", width=1,
                                command=lambda: insert_text(self.entry,
                                                            ' -> '))

        self.iff_button = Button(master, text="IFF", width=1,
                                 command=lambda: insert_text(self.entry,
                                                             ' <-> '))

        self.generate_button = Button(master, text="GO!",
                                      command=lambda: generate(sv))

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

        master.columnconfigure(0, weight=1)
        master.columnconfigure(1, weight=1)
        master.columnconfigure(2, weight=1)
        master.columnconfigure(3, weight=1)
        master.columnconfigure(4, weight=1)



if __name__ == "__main__":
    root = Tk()
    # root.resizable(width=False, height=False)
    # root.geometry('{}x{}'.format(400, 500))

    program_directory = sys.path[0]
    root.iconphoto(True, PhotoImage(file=os.path.join(program_directory,
                                                      "icon.png")))
    gui = TruthTableGeneratorGUI(root)

    # start the main loop
    root.mainloop()
    
