import tkinter as tk
from tkinter.ttk import Button, Label

def open_second_toplevel():
    top_two = tk.Toplevel()
    top_two.title('Top Level Two')
    top_two.geometry('200x200')

    title = Label(top_two, text= 'I am label, and you are on the top level!!!')
    title.pack(ipadx= 5, ipady= 5, expand= True)

    button_exit = Button(top_two, text= 'Exit', command= lambda: top_two.destroy())
    button_exit.pack(ipadx= 5, ipady= 5, expand= True)

    top_two.mainloop()


def open_first_toplevel(root):
    top_one = tk.Toplevel(root)
    top_one.title('Top Level One')
    top_one.geometry('300x300')

    title = Label(top_one, text= 'I am label, and you are on the top level!!!')
    title.pack(ipadx= 5, ipady= 5, expand= True)

    button_open_toplevel_two = Button(top_one, text= 'Open Top Level Two', command= lambda: open_second_toplevel())
    button_open_toplevel_two.pack()

    button_exit = Button(top_one, text= 'Exit', command= lambda: top_one.destroy())
    button_exit.pack(ipadx= 5, ipady= 5, expand= True)

    top_one.mainloop()



# para ver
root = tk.Tk()
root.title('Test pendejo')
root.geometry('600x500')

botton = Button(root, text= 'Open', command= lambda: open_first_toplevel(root))
botton.pack(ipadx= 5, ipady= 5, expand= True)

root.mainloop()