from tkinter import Tk, Label, Button, Frame, Entry, E, W, INSERT


def insert_text(field, text):
    field.insert(INSERT, text)
    return


def validate(text):
    raise Exception("Input recieved: {}".format(text))


class TruthTableGeneratorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Truth Table Generator")

        # declaring and defining widgets
        self.entry = Entry(master)

        self.p_button = Button(master, text="p",
                               command=lambda: insert_text(self.entry, 'p'))

        self.q_button = Button(master, text="q",
                               command=lambda: insert_text(self.entry, 'q'))

        self.and_button = Button(master, text="and",
                                 command=lambda: insert_text(self.entry, '*'))

        self.or_button = Button(master, text="or",
                                command=lambda: insert_text(self.entry, '+'))

        self.not_button = Button(master, text="not",
                                 command=lambda: insert_text(self.entry, '!'))

        self.left_paren_button = Button(master, text="(",
                                        command=lambda: insert_text(self.entry,
                                                                    '('))

        self.right_paren_button = Button(master, text=")",
                                         command=lambda:
                                         insert_text(self.entry, ')'))

        self.generate_button = Button(master, text="GO!",
                                      command=self.generate)

        # adding widgets to the grid
        self.p_button.grid(row=1, column=0)
        self.q_button.grid(row=1, column=1)
        self.and_button.grid(row=1, column=2)
        self.or_button.grid(row=1, column=3)
        self.not_button.grid(row=1, column=4)
        self.left_paren_button.grid(row=1, column=5)
        self.right_paren_button.grid(row=1, column=6)
        self.generate_button.grid(row=2, column=6)
        self.entry.grid(row=2, column=0, columnspan=6, sticky=E+W)

    def generate(self):
        try:
            validate(self.entry.get())
            print("VALID")
        except Exception as ex:
            print(str(ex))


if __name__ == "__main__":
    root = Tk()
    root.resizable(width=False, height=False)
    root.geometry('{}x{}'.format(400, 500))
    root.iconbitmap('@icon.xbm')

    gui = TruthTableGeneratorGUI(root)

    # start the main loop
    root.mainloop()
    
