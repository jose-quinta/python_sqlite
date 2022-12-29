

class User:
    def __init__(
            self, id:int = 0, name:str = 'annonimous', firstname:str = 'firstname',
            lastname:str = 'lastname', phonenumber:str = '0000-0000', email:str = 'example@gmail.com', passsword:str = '12345'
        ) -> None:
        self.id:int = id
        self.name:str = name
        self.firstname:str = firstname
        self.lastname:str = lastname
        self.phonenumber:str = phonenumber
        self.email:str = email
        self.passsword:str = passsword

    # es como el toString de cpp para imprimir la descripcion de la clase
    def __str__(self) -> str:
        return f'ID: {self.id}\nName: {self.name}\nFirstname: {self.firstname}\nLastname: {self.lastname}\nPhonenumber: {self.phonenumber}\nEmail: {self.email}\nPassword: {self.passsword}'