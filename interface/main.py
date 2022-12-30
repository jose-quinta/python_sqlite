import tkinter as tk
from tkinter.messagebox import askquestion, showinfo

# para usar la ventana de registro
from interface.register import RegisterWn

# importamos de data user para llamar la lista de usuario que estan en la base de datos
from data.user import UserDB

# instanciar la conexion de la tabla de usuario
userDb = UserDB()

class MainWn(tk.Frame):
    def __init__(self, master:any= None) -> None: # , titles:list= [], data:list= [], rows:int= 0, columns:int= 0
        tk.Frame.__init__(self, master)

        self.titles = ["ID", "Name", "Firstname", "Lastname", "Phonenumber", "Email", "Password"]
        self.list = userDb.select_users()
        self.rows = len(self.list)
        self.columns = len(self.list[0])

        self.pack()

        self.master.title('prueba con sqlite')
        self.master.geometry('1080x500')
        self.master.resizable(width=False, height=False)

        self.show_display()


    def register_windows(self, type:int):
        # root = tk.Toplevel(self)
        registerWn = RegisterWn(master= self, type= type)
        # registerWn.grab_set()
        registerWn.mainloop()


    def connect_database(self):
        userDb.create_table()


    def print_table(self):
        for i in range(0, self.rows):
            for j in range(0, self.columns):
                self.e = tk.Entry(self.table, width=15, fg='black', font=('Arial', 12, 'normal'))
                self.e.grid(row= i+1, column= j, sticky= "e")
                self.e.insert(tk.END, self.list[i][j])


    def update_table(self):
        self.list = userDb.select_users()
        self.rows = len(self.list)
        self.columns = len(self.list[0])
        self.print_table()


    def exit_application(self):
        value = askquestion(title= 'Exit', message= 'You want to exit the application?')
        if value == 'yes':
            userDb.close_connection()
            return self.master.destroy()


    def license(self):
        showinfo(title= 'license', message= 'license nothing is just a test!!!')


    def about_of(self):
        showinfo(title= 'about of', message= 'It is just a test no more!!!')


    def show_display(self):
        # barra de menu
        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label= "Conectar", command= lambda: self.connect_database())
        self.file_menu.add_command(label= "Nuevo registro", command= lambda: self.register_windows(1))
        self.file_menu.add_command(label= "Salir", command= lambda: self.exit_application())

        self.help_menu = tk.Menu(self.menu, tearoff=0)
        self.help_menu.add_command(label= "Licencia", command= lambda: self.license())
        self.help_menu.add_command(label= "Acerca de...", command= lambda: self.about_of())

        self.menu.add_cascade(label= "Archivo", menu= self.file_menu)
        self.menu.add_cascade(label= "Ayuda", menu= self.help_menu)

        # boton para registrar
        self.bar = tk.Frame(self.master)
        self.bar.pack(side= tk.TOP, padx= 5, pady= 5)

        self.hidden = tk.Label(self.bar, text= 'User table', width= 45, height= 1, font= ('Arial', 12, 'normal'))
        self.hidden.pack(side= tk.LEFT, padx= 5, pady= 5)

        self.btn_delete = tk.Button(self.bar, text= 'Delete User', width= 20, height= 1, font= ('Arial', 11, 'normal'), command= lambda: self.register_windows(3))
        self.btn_delete.pack(side= tk.LEFT, padx= 5, pady= 5)

        self.btn_update = tk.Button(self.bar, text= 'Update User', width= 20, height= 1, font= ('Arial', 11, 'normal'), command= lambda: self.register_windows(2))
        self.btn_update.pack(side= tk.LEFT, padx= 5, pady= 5)

        self.btn_register = tk.Button(self.bar, text= 'New Register', width= 20, height= 1, font= ('Arial', 11, 'normal'), command= lambda: self.register_windows(1))
        self.btn_register.pack(side= tk.LEFT, padx= 5, pady= 5)

        # Code for creating table
        self.table = tk.Frame(self.master)
        self.table.pack(side= tk.TOP, padx= 5, pady= 5)

        for i in range(0, len(self.titles)):
            self.i = tk.Entry(self.table, relief= 'flat', width= 15, fg= 'black', bg= None, justify= 'center', font= ('Arial', 12, 'normal'))
            self.i.grid(row= 0, column= i, sticky= "e")
            self.i.insert(tk.END, self.titles[i])

        # funcion para imprimir el contenido de la base de datos en la tabla.
        self.print_table()

        # boton de salida
        self.bar_exit = tk.Frame(self.master, width= 1000, height= 1)
        self.bar_exit.pack(side= tk.BOTTOM, padx= 5, pady= 5)

        self.hidden_exit = tk.Label(self.bar_exit, width= 80)
        self.hidden_exit.pack(side= tk.LEFT, padx= 5, pady= 5)

        self.btn_tbl_update = tk.Button(self.bar_exit, text= 'Update table', width= 20, height= 1, font= ('Arial', 11, 'normal'), command= lambda: self.update_table())
        self.btn_tbl_update.pack(side= tk.LEFT, padx= 5, pady= 5)

        self.btn_exit = tk.Button(self.bar_exit, text= 'Exit', width= 20, height= 1, font= ('Arial', 11, 'normal'), command= lambda: self.exit_application())
        self.btn_exit.pack(side= tk.LEFT, padx= 5, pady= 5)


