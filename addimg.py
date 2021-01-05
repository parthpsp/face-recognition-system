# Python program to create
# a file explorer in Tkinter

# import all components
# from the tkinter library
from tkinter import *

# import filedialog module
from tkinter import filedialog

import shutil



def add_new():
    # Function for opening the
    # file explorer window
    filename = ""

    def browseFiles():
        filename = filedialog.askopenfilename(initialdir="/",
                                              title="Select a File",
                                              filetypes=(("Text files",
                                                          "*.jpg*"),
                                                         ("all files",
                                                          "*.*")))

        # Change label contents
        label_file_explorer.configure(text="File selected: " + filename)

    # canvas = Canvas(window, width = 300, height = 300)
    # canvas.grid(column = 2, row = 4)

    # img = ImageTk.PhotoImage(Image.open(filename))
    # canvas.create_image(20,20, anchor=NW, image=img)

    def submitfun():
        name = "/pics/" + E1.get() + ".jpg"
        label_file_explorer.configure(text="File selected: " + name)
        shutil.copy(filename, name)

    # Create the root window
    window = Tk()

    # Set window title
    window.title('File Explorer')

    # Set window size
    window.geometry("500x500")

    # Set window background color
    window.config(background="white")

    # Create a File Explorer label
    label_file_explorer = Label(window,
                                text="no image selected",
                                height=4,
                                fg="blue")
    L1 = Label(window, text="bandit Name", fg="blue")
    # L1.pack( side = LEFT)
    E1 = Entry(window, bd=5)
    # E1.pack(side = RIGHT)

    button_explore = Button(window,
                            text="select image",
                            command=browseFiles)

    button_submit = Button(window,
                           text="submit information",
                           command=submitfun)

    button_exit = Button(window,
                         text="Exit",
                         command=exit)

    # Grid method is chosen for placing
    # the widgets at respective positions
    # in a table like structure by
    # specifying rows and columns
    label_file_explorer.grid(column=2, row=2)
    L1.grid(column=1, row=1)
    E1.grid(column=2, row=1)
    button_explore.grid(column=2, row=3)
    button_submit.grid(column=2, row=5)

    button_exit.grid(column=2, row=6)

    # Let the window wait for any events
    window.mainloop()
