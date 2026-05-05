import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.messagebox import askquestion, showinfo, showerror

from app.entities.user import User
from app.controllers.user import UserDB


class RegisterWn(tk.Toplevel):
    def __init__(self, master=None, type: int = 1, userDb: UserDB = None, user: User = None) -> None:
        super().__init__(master)

        self.type = type
        self.userDb = userDb or UserDB()
        self.user = user or User()

        self.configure(bg='#f5f5f5')
        self.title(self.get_title())
        self.geometry('500x450')
        self.resizable(False, False)

        self.create_widgets()
        self.load_user_data()

        if self.type == 3:
            self.disable_fields()


    def get_title(self) -> str:
        titles = {1: 'Register New User', 2: 'Update User', 3: 'Delete User'}
        return titles.get(self.type, 'User Form')


    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_style = {'font': ('Segoe UI', 16, 'bold'), 'foreground': self.get_title_color()}
        ttk.Label(main_frame, text=self.get_title(), **title_style).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        self.entries = {}
        fields = [
            ('ID', 'id', tk.Entry if self.type == 1 else ttk.Entry, {'state': 'readonly'} if self.type in (2, 3) else None),
            ('Name', 'name', ttk.Entry, None),
            ('First Name', 'firstname', ttk.Entry, None),
            ('Last Name', 'lastname', ttk.Entry, None),
            ('Phone Number', 'phonenumber', ttk.Entry, None),
            ('Email', 'email', ttk.Entry, None),
            ('Password', 'password', ttk.Entry, {'show': '•'}),
        ]
        
        row = 1
        for label_text, attr, widget_class, extra_opts in fields:
            ttk.Label(main_frame, text=f"{label_text}:", font=('Segoe UI', 10, 'bold')).grid(
                row=row, column=0, sticky='e', padx=(0, 10), pady=5)
            
            opts = {'width': 35, 'font': ('Segoe UI', 10)}
            if extra_opts:
                opts.update(extra_opts)
            
            if attr == 'id' and self.type in (2, 3):
                var = tk.StringVar()
                widget = widget_class(main_frame, textvariable=var, **opts)
                self.id_var = var
            else:
                widget = widget_class(main_frame, **opts)

            widget.grid(row=row, column=1, sticky='ew', pady=5)
            self.entries[attr] = widget
            row += 1

        main_frame.columnconfigure(1, weight=1)

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=row, column=0, columnspan=2, pady=20)

        if self.type == 1:
            ttk.Button(button_frame, text='Register', command=self.submit_register,
                      style='Success.TButton').pack(side=tk.LEFT, padx=5)
        elif self.type == 2:
            ttk.Button(button_frame, text='Update', command=self.submit_update,
                      style='Warning.TButton').pack(side=tk.LEFT, padx=5)
        elif self.type == 3:
            ttk.Button(button_frame, text='Delete', command=self.submit_delete,
                      style='Danger.TButton').pack(side=tk.LEFT, padx=5)

        ttk.Button(button_frame, text='Cancel', command=self.destroy).pack(side=tk.LEFT, padx=5)

        if self.type == 1:
            ttk.Button(button_frame, text='Clear', command=self.clear_fields).pack(side=tk.LEFT, padx=5)


    def get_title_color(self) -> str:
        colors = {1: '#2E7D32', 2: '#F57C00', 3: '#C62828'}
        return colors.get(self.type, '#000000')


    def load_user_data(self):
        if self.type in (2, 3) and self.user:
            if hasattr(self, 'id_var'):
                self.id_var.set(str(self.user.id))
            self.entries['name'].insert(0, self.user.name)
            self.entries['firstname'].insert(0, self.user.firstname)
            self.entries['lastname'].insert(0, self.user.lastname)
            self.entries['phonenumber'].insert(0, self.user.phonenumber)
            self.entries['email'].insert(0, self.user.email)
            if self.type != 3:
                self.entries['password'].insert(0, self.user.password if not self.user._is_hashed(self.user.password) else '')


    def disable_fields(self):
        for attr, widget in self.entries.items():
            if attr != 'id':
                widget.configure(state='disabled')


    def clear_fields(self):
        for attr, widget in self.entries.items():
            if attr not in ('id',):
                widget.delete(0, tk.END)


    def get_data(self) -> User:
        self.user.name = self.entries['name'].get()
        self.user.firstname = self.entries['firstname'].get()
        self.user.lastname = self.entries['lastname'].get()
        self.user.phonenumber = self.entries['phonenumber'].get()
        self.user.email = self.entries['email'].get()
        self.user.password = self.entries['password'].get()
        return self.user


    def submit_register(self):
        user = self.get_data()
        success, message = self.userDb.insert_user(user)
        if success:
            messagebox.showinfo('Success', message)
            self.destroy()
        else:
            messagebox.showerror('Error', message)


    def submit_update(self):
        try:
            user_id = int(self.id_var.get())
            user = self.get_data()
            success, message = self.userDb.update_user(user_id, user)
            if success:
                messagebox.showinfo('Success', message)
                self.destroy()
            else:
                messagebox.showerror('Error', message)
        except ValueError:
            messagebox.showerror('Error', 'Invalid user ID')


    def submit_delete(self):
        if askquestion('Confirm Delete', 'Are you sure you want to delete this user?') == 'yes':
            try:
                user_id = int(self.id_var.get())
                success, message = self.userDb.delete_user(user_id)
                if success:
                    messagebox.showinfo('Success', message)
                    self.destroy()
                else:
                    messagebox.showerror('Error', message)
            except ValueError:
                messagebox.showerror('Error', 'Invalid user ID')
