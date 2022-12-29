# import modulo de sqlite, para usar la base de dato que se crea en un fichero externo
from sqlite3 import connect, Error

class Database:
    def __init__(self) -> None:
        try:
            self.connection:any = connect('python_sqlite.db')
        except Error as e:
            print('An error has occurred: ',e)


    def close_connection(self) -> None:
        self.connection.close()

