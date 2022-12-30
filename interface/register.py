import tkinter as tk
from tkinter.messagebox import askquestion, showinfo, showerror
# from tkinter.ttk import Button

# ahora se importa la entidad usuario
from entities.user import User
# y de data la conexion a la tabla User
from data.user import UserDB

# instanciar la entidad y la conexion del usuario a base de datos
user = User()
userDb = UserDB()

class RegisterWn(tk.Toplevel):
    def __init__(self, master:any= None, type:int = 0) -> None:
        tk.Toplevel.__init__(self, master)

        self.type = type

        if self.type == 1:
            self.title('Register')
        elif self.type == 2:
            self.title('Update')
        elif self.type == 3:
            self.title('Delete')

        self.geometry('600x500')
        self.resizable(width=False, height=False)

        self.show_display()


    def destroy_app(self):
        return self.destroy()


    def cancel_registration(self):
        # value = askquestion(title= 'Exit', message= 'Do you want to hang out!!!')
        value = askquestion(title= 'Cancel', message= 'Do you want to cancel the registration!!!')
        if value == 'yes':
            self.clear_data()
            return self.destroy()


    def clear_data(self):
        self.txt_name.delete(0, tk.END)
        self.txt_firstname.delete(0, tk.END)
        self.txt_lastname.delete(0, tk.END)
        self.txt_phonenumber.delete(0, tk.END)
        self.txt_email.delete(0, tk.END)
        self.txt_password.delete(0, tk.END)


    def insert_data(self, user):
        self.txt_name.insert(tk.END, user[1])
        self.txt_firstname.insert(tk.END, user[2])
        self.txt_lastname.insert(tk.END, user[3])
        self.txt_phonenumber.insert(tk.END, user[4])
        self.txt_email.insert(tk.END, user[5])
        self.txt_password.insert(tk.END, user[6])


    def get_data(self):
        user.name = self.txt_name.get()
        user.firstname = self.txt_firstname.get()
        user.lastname = self.txt_lastname.get()
        user.phonenumber = self.txt_phonenumber.get()
        user.email = self.txt_email.get()
        user.password = self.txt_password.get()

        return user


    def submit_register(self):
        # showinfo(title= 'Register', message= 'The user was successfully inserted!!!')
        user = self.get_data()
        userDb.insert_user(user)
        self.destroy_app()


    def search_id(self):
        id = int(self.txt_id.get())
        user = userDb.select_user(id)
        self.insert_data(user)


    def submit_update(self):
        id = int(self.txt_id.get())
        user = self.get_data()
        userDb.update_user(id, user)
        self.destroy_app()


    def submit_delete(self):
        id = int(self.txt_id.get())
        userDb.delete_user(id)
        self.destroy_app()


    def show_display(self):
        self.frame = tk.Frame(self)
        self.frame.pack(side= tk.TOP)

        # title
        if (self.type == 1):
            self.lbl_title = tk.Label(self.frame, text= 'Register User', width= 50, bg= 'blue', height= 2, font=('Arial', 14, 'normal'))
        elif (self.type == 2):
            self.lbl_title = tk.Label(self.frame, text= 'Update User', width= 50, bg= 'blue', height= 2, font=('Arial', 14, 'normal'))
        elif (self.type == 3):
            self.lbl_title = tk.Label(self.frame, text= 'Delete User', width= 50, bg= 'blue', height= 2, font=('Arial', 14, 'normal'))

        self.lbl_title.grid(row= 0, column=0, columnspan= 2, sticky= 'e', padx= 5, pady= 5)

        # content
        if (self.type == 2 or self.type == 3):
            self.lbl_id = tk.Label(self.frame, text= 'Id', anchor= 'w', width= 12, height= 2, font=('Arial', 12, 'normal'))
            self.lbl_id.grid(row= 1, column= 0, sticky= 'e', padx= 5, pady= 5)
            self.txt_id = tk.Entry(self.frame, width= 40, fg= 'black', font= ('Arial', 12, 'normal'))
            self.txt_id.grid(row= 1, column= 1, sticky= 'e', padx= 5, pady= 5)

        self.lbl_name = tk.Label(self.frame, text= 'Name', anchor= 'w', width= 12, height= 2, font=('Arial', 12, 'normal'))
        self.lbl_name.grid(row= 2, column= 0, sticky= 'e', padx= 5, pady= 5)
        self.txt_name = tk.Entry(self.frame, width= 40, fg= 'black', font= ('Arial', 12, 'normal'))
        self.txt_name.grid(row= 2, column= 1, sticky= 'e', padx= 5, pady= 5)

        self.lbl_firstname = tk.Label(self.frame, text= 'First name', anchor= 'w', width= 12, height= 2, font=('Arial', 12, 'normal'))
        self.lbl_firstname.grid(row= 3, column= 0, sticky= 'e', padx= 5, pady= 5)
        self.txt_firstname = tk.Entry(self.frame, width= 40, fg= 'black', font= ('Arial', 12, 'normal'))
        self.txt_firstname.grid(row= 3, column= 1, sticky= 'e', padx= 5, pady= 5)

        self.lbl_lastname = tk.Label(self.frame, text= 'Last name', anchor= 'w', width= 12, height= 2, font=('Arial', 12, 'normal'))
        self.lbl_lastname.grid(row= 4, column= 0, sticky= 'e', padx= 5, pady= 5)
        self.txt_lastname = tk.Entry(self.frame, width= 40, fg= 'black', font= ('Arial', 12, 'normal'))
        self.txt_lastname.grid(row= 4, column= 1, sticky= 'e', padx= 5, pady= 5)

        self.lbl_phonenumber = tk.Label(self.frame, text= 'Phone number', anchor= 'w', width= 12, height= 2, font=('Arial', 12, 'normal'))
        self.lbl_phonenumber.grid(row= 5, column= 0, sticky= 'e', padx= 5, pady= 5)
        self.txt_phonenumber = tk.Entry(self.frame, width= 40, fg= 'black', font= ('Arial', 12, 'normal'))
        self.txt_phonenumber.grid(row= 5, column= 1, sticky= 'e', padx= 5, pady= 5)

        self.lbl_email = tk.Label(self.frame, text= 'Email', anchor= 'w', width= 12, height= 2, font=('Arial', 12, 'normal'))
        self.lbl_email.grid(row= 6, column= 0, sticky= 'e', padx= 5, pady= 5)
        self.txt_email = tk.Entry(self.frame, width= 40, fg= 'black', font= ('Arial', 12, 'normal'))
        self.txt_email.grid(row= 6, column= 1, sticky= 'e', padx= 5, pady= 5)

        self.lbl_password = tk.Label(self.frame, text= 'Password', anchor= 'w', width= 12, height= 2, font=('Arial', 12, 'normal'))
        self.lbl_password.grid(row= 7, column= 0, sticky= 'e', padx= 5, pady= 5)
        self.txt_password = tk.Entry(self.frame, width= 40, fg= 'black', font= ('Arial', 12, 'normal'))
        self.txt_password.grid(row= 7, column= 1, sticky= 'e', padx= 5, pady= 5)

        # buttons de register and cancel
        self.btn_frame = tk.Frame(self)
        self.btn_frame.pack(side= tk.BOTTOM, padx= 10, pady= 10)

        self.btn_cancel = tk.Button(self.btn_frame, text= 'Cancel', width= 15, command= lambda: self.cancel_registration())
        self.btn_cancel.pack(side= tk.LEFT, padx= 3, pady= 3)

        self.btn_clear = tk.Button(self.btn_frame, text= 'Clear', width= 15, command= lambda: self.clear_data())
        self.btn_clear.pack(side= tk.LEFT, padx= 3, pady= 3)

        if (self.type == 1):
            self.btn_register = tk.Button(self.btn_frame, text= 'Register', width= 15, command= lambda: self.submit_register())
            self.btn_register.pack(side= tk.LEFT, padx= 3, pady= 3)

        else:
            self.btn_search = tk.Button(self.btn_frame, text= 'Search ID', width= 15, command= lambda: self.search_id())
            self.btn_search.pack(side= tk.LEFT, padx= 3, pady= 3)

            if (self.type == 2):
                self.btn_update = tk.Button(self.btn_frame, text= 'Update', width= 15, command= lambda: self.submit_update())
                self.btn_update.pack(side= tk.LEFT, padx= 3, pady= 3)
            elif (self.type == 3):
                self.btn_delete = tk.Button(self.btn_frame, text= 'Delete', width= 15, command= lambda: self.submit_delete())
                self.btn_delete.pack(side= tk.LEFT, padx= 3, pady= 3)

        # frame donde estar el boton de prueba para salir de la ventana de registro
        # self.botton = Button(self, text= 'Exit', width= 15, command= lambda: self.cancel_registration())
        # self.botton.pack(ipadx=5, ipady=5, expand= True)


