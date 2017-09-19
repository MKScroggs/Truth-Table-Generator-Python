from tkinter import Tk, Label, Button, Frame, Entry

class TruthTableGeneratorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Truth Table Generator")

        self.button_frame = Frame(master)

        self.p_button = Button(master, text="p", command=master.quit)
        self.p_button.grid(row=1, column=0)

        self.q_button = Button(master, text="q", command=master.quit)
        self.q_button.grid(row=1, column=1)

        self.and_button = Button(master, text="and", command=master.quit)
        self.and_button.grid(row=1, column=2)

        self.or_button = Button(master, text="or", command=master.quit)
        self.or_button.grid(row=1, column=3)

        self.not_button = Button(master, text="not", command=master.quit)
        self.not_button.grid(row=1, column=4)

        self.left_paren_button = Button(master, text="(", command=master.quit)
        self.left_paren_button.grid(row=1, column=5)

        self.right_paren_button = Button(master, text=")", command=master.quit)
        self.right_paren_button.grid(row=1, column=6)

        self.generate_button = Button(master, text="GO!",
                                      command=self.generate())
        self.generate_button.grid(row=2, column=0)

        self.entry = Entry(master)
        self.entry.grid(row=3, column=1, columnspan=7)

    def generate(self):
        print("greetings")


if __name__ == "__main__":
    root = Tk()
    my_gui = TruthTableGeneratorGUI(root)
    root.mainloop()
    
