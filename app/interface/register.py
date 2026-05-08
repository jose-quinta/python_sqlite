import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.messagebox import askquestion, showinfo, showerror
from typing import Optional, Tuple

from app.entities.user import User
from app.controllers.user import UserDB


class RegisterWn(tk.Toplevel):
    def __init__(
        self, master: Optional[tk.Tk] = None, type: int = 1,
        userDb: Optional[UserDB] = None, user: Optional[User] = None
    ) -> None:
        super().__init__(master=master)

        self.type: int = type
        self.userDb: UserDB = userDb or UserDB()
        self.user: User = user or User()
        self.password_changed: bool = False

        self.configure(bg='#f5f5f5')
        self.title(self.get_title())
        self.geometry('500x450')
        self.resizable(False, False)

        self.create_widgets()
        self.load_user_data()

        if self.type == 3:
            self.disable_fields()

    def get_title(self) -> str:
        titles: dict[int, str] = {1: 'Register New User', 2: 'Update User', 3: 'Delete User'}
        return titles.get(self.type, 'User Form')

    def create_widgets(self) -> None:
        main_frame: ttk.Frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_style: dict[str, object] = {'font': ('Segoe UI', 16, 'bold')}
        ttk.Label(main_frame, text=self.get_title(), **title_style).grid(
            row=0, column=0, columnspan=2, pady=(0, 20))

        self.entries: dict[str, tk.Widget] = {}
        fields: list[Tuple[str, str, type, bool]] = [
            ('ID', 'id', tk.Entry, True),
            ('Name', 'name', ttk.Entry, False),
            ('First Name', 'firstname', ttk.Entry, False),
            ('Last Name', 'lastname', ttk.Entry, False),
            ('Phone Number', 'phonenumber', ttk.Entry, False),
            ('Email', 'email', ttk.Entry, False),
            ('Password', 'password', ttk.Entry, False),
        ]

        row: int = 1
        for label_text, attr, widget_class, is_readonly in fields:
            ttk.Label(main_frame, text="{}:".format(label_text),
                      font=('Segoe UI', 10, 'bold')).grid(
                row=row, column=0, sticky='e', padx=(0, 10), pady=5)

            opts: dict[str, object] = {'width': 35, 'font': ('Segoe UI', 10)}

            if attr == 'password':
                opts['show'] = '\u2022'

            if is_readonly and self.type in (2, 3):
                var: tk.StringVar = tk.StringVar()
                widget: tk.Entry = tk.Entry(
                    main_frame, textvariable=var, state='readonly', **opts)
                if attr == 'id':
                    self.id_var: tk.StringVar = var
            else:
                widget = widget_class(main_frame, **opts)

            widget.grid(row=row, column=1, sticky='ew', pady=5)
            self.entries[attr] = widget
            row += 1

        main_frame.columnconfigure(1, weight=1)

        button_frame: ttk.Frame = ttk.Frame(main_frame)
        button_frame.grid(row=row, column=0, columnspan=2, pady=20)

        if self.type == 1:
            ttk.Button(button_frame, text='Register',
                       command=self.submit_register).pack(side=tk.LEFT, padx=5)
        elif self.type == 2:
            ttk.Button(button_frame, text='Update',
                       command=self.submit_update).pack(side=tk.LEFT, padx=5)
        elif self.type == 3:
            ttk.Button(button_frame, text='Delete',
                       command=self.submit_delete).pack(side=tk.LEFT, padx=5)

        ttk.Button(button_frame, text='Cancel',
                   command=self.destroy).pack(side=tk.LEFT, padx=5)

        if self.type == 1:
            ttk.Button(button_frame, text='Clear',
                       command=self.clear_fields).pack(side=tk.LEFT, padx=5)

    def on_password_key(self, event: object = None) -> None:
        """Track if the password field has been modified by the user"""
        self.password_changed = True

    def disable_fields(self) -> None:
        for attr, widget in self.entries.items():
            if attr != 'id':
                try:
                    widget.configure(state='disabled')
                except tk.TclError:
                    pass

    def clear_fields(self) -> None:
        for attr, widget in self.entries.items():
            if attr not in ('id',):
                try:
                    widget.delete(0, tk.END)
                except (tk.TclError, AttributeError):
                    pass

    def load_user_data(self) -> None:
        if self.type in (2, 3) and self.user:
            if hasattr(self, 'id_var') and self.user.id is not None:
                self.id_var.set(str(self.user.id))
            for field in ('name', 'firstname', 'lastname', 'phonenumber', 'email'):
                if field in self.entries:
                    value: str = getattr(self.user, field, '') or ''
                    self.entries[field].insert(0, value)

            if 'password' in self.entries and self.type != 3:
                placeholder: str = '\u2022' * 8
                self.entries['password'].insert(0, placeholder)
                self.entries['password'].bind('<Key>', self.on_password_key)

    def get_data(self) -> User:
        """Extract form data and return updated User object"""
        self.user.name = self.entries['name'].get().strip()
        self.user.firstname = self.entries['firstname'].get().strip()
        self.user.lastname = self.entries['lastname'].get().strip()
        self.user.phonenumber = self.entries['phonenumber'].get().strip()
        self.user.email = self.entries['email'].get().strip()

        password_value: str = self.entries['password'].get()
        if password_value:
            self.user.set_password(password_value)
            if self.type == 2:
                self.password_changed = True
        elif self.type == 1:
            self.user.set_password('')
        return self.user

    def submit_register(self) -> None:
        user: User = self.get_data()
        success, message = self.userDb.insert_user(user)
        if success:
            messagebox.showinfo('Success', message)
            self.destroy()
        else:
            messagebox.showerror('Error', message)

    def submit_update(self) -> None:
        try:
            user_id: int = int(self.id_var.get())
            user: User = self.get_data()
            success, message = self.userDb.update_user(
                user_id, user, password_changed=self.password_changed)
            if success:
                messagebox.showinfo('Success', message)
                self.destroy()
            else:
                messagebox.showerror('Error', message)
        except ValueError:
            messagebox.showerror('Error', 'Invalid user ID')
        except AttributeError:
            messagebox.showerror('Error', 'No user selected')

    def submit_delete(self) -> None:
        if askquestion('Confirm Delete', 'Are you sure you want to delete this user?') == 'yes':
            try:
                user_id: int = int(self.id_var.get())
                success, message = self.userDb.delete_user(user_id)
                if success:
                    messagebox.showinfo('Success', message)
                    self.destroy()
                else:
                    messagebox.showerror('Error', message)
            except ValueError:
                messagebox.showerror('Error', 'Invalid user ID')
            except AttributeError:
                messagebox.showerror('Error', 'No user selected')
