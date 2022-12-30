# importar la conexion para usarla en este fichero
from data.db import Database
# por que no quiero escribir uso la entidad de usuario
from entities.user import User

# ya que estamos con la interfaz vamos a usar cuadros de mensage
from tkinter.messagebox import showinfo, showerror

class UserDB(Database): # para usar la herencia
    def __init__(self) -> None:
        super().__init__() # para usar los atributos que se heredaran
        self.cursor:any = self.connection.cursor()


    def create_table(self):
        try:
            sql_query ='''CREATE TABLE IF NOT EXISTS user(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VAR(60) NOT NULL,
                firstname VAR(60) NOT NULL,
                lastname VAR(60) NOT NULL,
                phonenumber VAR(10),
                email VAR(60) NOT NULL UNIQUE,
                password VAR(17) NOT NULL
            );'''
            self.cursor.execute(sql_query)
            self.connection.commit()
            showinfo(title= 'Successfully', message= 'Connected successfully!!!')
            # print('Connected successfully!!!')
        except Exception as e:
            showerror(title= 'Error', message= e)
            # print('An error has occurred: ', e)


    def select_last_id(self):
        sql = 'SELECT id FROM user ORDER BY id DESC LIMIT 1;'
        try: # tratar si no hay error
            self.cursor.execute(sql) # el cursor ejecuta la consulta
            id = self.cursor.fetchone() # ya que es solo una fila se procesa con fecthone
            return id[0] # ya que nos devuelve una tupla, solo le ponemos la posicion para retornar el valor
        except Exception as e: # si hay error
            showerror(title= 'Error', message= e)
            # print('An error has occurred: ',e) # manda la alerta


    def insert_user(self, user:User):
        try:
            query = f'INSERT INTO user(id, name, firstname, lastname, phonenumber, email, password) VALUES (NULL, "{user.name}", "{user.firstname}", "{user.lastname}", "{user.phonenumber}", "{user.email}", "{user.password}");'
            self.cursor.execute(query)
            self.connection.commit()
            showinfo(title= 'Successfully', message= 'The user was successfully registered!!!')
            # print('The user was successfully registered!!!')
        except Exception as e:
            showerror(title= 'Error', message= e)
            # print('An error has occurred: ', e)


    def select_users(self):
        try:
            query = 'SELECT id, name, firstname, lastname, phonenumber, email, password FROM user;'
            self.cursor.execute(query)
            users = self.cursor.fetchall()
            # for user in users:
                # print(f'ID: {user[0]}\nName: {user[1]}\nFirstname: {user[2]}\nLastname: {user[3]}\nPhonenumber: {user[4]}\nEmail: {user[5]}\nPassword: {user[6]}')
            return users
        except Exception as e:
            showerror(title= 'Error', message= e)
            # print('An error has occurred: ', e)


    def select_user(self, id:int):
        try:
            query = f'SELECT id, name, firstname, lastname, phonenumber, email, password FROM user WHERE id={id};'
            self.cursor.execute(query)
            user = self.cursor.fetchone()
            # print(f'ID: {user[0]}\nName: {user[1]}\nFirstname: {user[2]}\nLastname: {user[3]}\nPhonenumber: {user[4]}\nEmail: {user[5]}\nPassword: {user[6]}')
            return user
        except Exception as e:
            showerror(title= 'Error', message= e)
            # print('An error has occurred: ', e)


    def update_user(self, id:int, user:User):
        try:
            query = f'UPDATE user SET name="{user.name}", firstname="{user.firstname}", lastname="{user.lastname}", phonenumber="{user.phonenumber}", email="{user.email}", password="{user.password}" WHERE id={id};'
            self.cursor.execute(query)
            self.connection.commit()
            showinfo(title= 'Successfully', message= 'The user was successfully updated!!!')
            # print('The user was successfully updated!!!')
        except Exception as e:
            showerror(title= 'Error', message= e)
            # print('An error has occurred: ', e)


    def delete_user(self, id:int):
        try:
            query = f'DELETE FROM user WHERE id={id};'
            self.cursor.execute(query)
            self.connection.commit()
            showinfo(title= 'Successfully', message= 'The user was successfully removed!!!')
            # print('The user was successfully removed!!!')
        except Exception as e:
            showerror(title= 'Error', message= e)
            # print('An error has occurred: ', e)