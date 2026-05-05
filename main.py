import tkinter as tk

from app.utils.logger import setup_logger
from app.entities.user import User
from app.controllers.user import UserDB
from app.interface.main import MainWn

if __name__ == '__main__':
    setup_logger('python_sqlite', level='INFO') # type: ignore

    root = tk.Tk()
    userDb = UserDB()
    user = User()

    main = MainWn(master=root, userDb=userDb, user=user)
    root.mainloop()
