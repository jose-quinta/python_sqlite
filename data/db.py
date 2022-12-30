# import modulo de sqlite, para usar la base de dato que se crea en un fichero externo
from sqlite3 import connect, Error

# importar cajas/cuadros de mensajes
from tkinter.messagebox import showerror

class Database:
    def __init__(self) -> None:
        try:
            self.connection:any = connect('python_sqlite.db')
        except Error as e:
            showerror(
                title= 'Connection error',
                message= e
            )
            # print('An error has occurred: ',e)


    def close_connection(self) -> None:
        try:
            self.connection.close()
        except Error as e:
            showerror(
                title= 'Failed to close',
                message= e
            )
            # print('An error has occurred: ',e)

