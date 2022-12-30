# para usar la entidad usuario
from entities.user import User
# para usar la conexion a la tabla de user en la base de datos
from data.user import UserDB

# para usar interfaz debemos de importar tkinter
import tkinter as tk
# importar la ventana principal
from interface.main import MainWn

# inicializar la instancia de la entidad usuario
user = User()
# inicializar la instancia de usuario con conexion a base de datos
userDb = UserDB()

""" # solo una funcion que devuelve un numero
def add_option() -> int:
    number:int = int(input('Select option >> '))
    return number

# una funcion que tiene parametro para ver cual de los dos fragmentos se va a utilizar
def user_data(action):
    if action == 1:
        user.name = input('Add your name: ')
        user.firstname = input('Add your firstname: ')
        user.lastname = input('Add your lastname: ')
        user.phonenumber = input('Add your phonenumber: ')
        user.email = input('Add your email: ')
        user.password = input('Add your password: ')

    if action == 2:
        user.name = input('Add your new name: ')
        user.firstname = input('Add your new firstname: ')
        user.lastname = input('Add your new lastname: ')
        user.phonenumber = input('Add your new phonenumber: ')
        user.email = input('Add your new email: ')
        user.password = input('Add your new password: ')

# funcion de menu donde esta las opciones a ejecutar
def menu():
    # variable de opcion
    opcion:int = 1000000000000000
    while opcion != 0:
        print('*'*10, 'Menu de opciones', '*'*10)
        print('1. Insert user\n2. Show user by id\n3. Show all user\n4. Update user\n5. Delete user\n0. Exit application')
        opcion = add_option()
        # match es una funcion que viene integrada desde la version 3.10 en adelante creo
        match opcion: # match compara las opciones
            case 1: # si la compracion es uno ejecutara el siguiente bloque de codigo
                user_data(1)
                userDb.insert_user(user)
                id = userDb.select_last_id()
                userDb.select_user(id)
                continue

            case 2:
                id = int(input('Add ID of the user you want to see: '))
                userDb.select_user(id)
                continue

            case 3:
                userDb.select_users()
                continue

            case 4:
                id = int(input('Add ID of the user you want to update: '))
                user_data(2)
                userDb.update_user(id, user)
                userDb.select_user(id)
                continue

            case 5:
                id = int(input('Add the ID of the user you want to delete: '))
                userDb.select_user(id)
                userDb.delete_user(id)
                continue

            case 0:
                print('Thank for using the application!!!')
                break

    userDb.close_connection()
    print('Farewell') """


if __name__ == '__main__': # esto es para cuando hay mas de un archivo main en las diferente carpeta, y con esto podemos identificar cual es el principal
    """ userDb.create_table()
    menu() # se llama la funcion menu """

    """ titles = ["ID", "Name", "Firstname", "Lastname", "Phonenumber", "Email", "Password"]
    data = userDb.select_users()
    rows = len(data)
    columns = len(data[0]) """

    root = tk.Tk()
    main = MainWn(master=root)
    main.mainloop()
