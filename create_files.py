#!/usr/bin/env python3
"""Script to create interface files with correct syntax"""

import os

# MainWn interface
main_py = '''import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.messagebox import askquestion, showinfo

from app.interface.register import RegisterWn
from app.controllers.user import UserDB
from app.entities.user import User
from app.data.db import init_db

class MainWn(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        
        self.userDb = UserDB()
        
        self.configure(bg='#f0f0f0')
        self.pack(fill=tk.BOTH, expand=True)
        
        self.master.title('User Management System')
        self.master.geometry('1000x600')
        self.master.minsize(800, 500)
        
        self.setup_ui()
        self.load_users()

    def setup_ui(self):
        self.setup_menu()
        self.setup_toolbar()
        self.setup_table()
        self.setup_statusbar()

    def setup_menu(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New User", command=lambda: self.open_register(1))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_application)
        menubar.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.about_of)
        menubar.add_cascade(label="Help", menu=help_menu)

    def setup_toolbar(self):
        toolbar = ttk.Frame(self)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        ttk.Button(toolbar, text="New User", command=lambda: self.open_register(1)).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Edit", command=lambda: self.open_register(2)).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Delete", command=lambda: self.open_register(3)).pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=10, fill=tk.Y)
        
        ttk.Button(toolbar, text="Refresh", command=self.load_users).pack(side=tk.LEFT, padx=2)

    def setup_table(self):
        table_frame = ttk.Frame(self)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        columns = ('ID', 'Name', 'First Name', 'Last Name', 'Phone', 'Email', 'Password')
        
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.tree.heading(col, text=col)
            width = 80 if col == 'ID' else 150 if col in ('Name', 'Email') else 120
            self.tree.column(col, width=width, minwidth=50, anchor=tk.W)
        
        self.tree.column('Password', width=100, anchor=tk.CENTER)

        vsb = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        self.tree.bind('<Double-1>', lambda e: self.open_register(2))

    def setup_statusbar(self):
        self.status_bar = ttk.Label(self, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def load_users(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        users = self.userDb.select_users()
        
        for user in users:
            data = user.to_tuple()
            display_data = list(data)
            if user._is_hashed():
                display_data[6] = '******'
            self.tree.insert('', tk.END, values=display_data)
        
        self.status_bar.config(text="Total users: {}".format(len(users)))

    def open_register(self, type_val):
        selected = self.tree.selection()
        
        if type_val in (2, 3) and not selected:
            messagebox.showwarning('No Selection', 'Please select a user from the table')
            return
        
        user_to_edit = None
        if type_val in (2, 3) and selected:
            item = self.tree.item(selected[0])
            user_id = item['values'][0]
            user_to_edit = self.userDb.select_user(user_id)
        
        registerWn = RegisterWn(self, type=type_val, userDb=self.userDb, user=user_to_edit)
        self.wait_window(registerWn)
        self.load_users()

    def exit_application(self):
        if askquestion('Exit', 'Are you sure you want to exit?') == 'yes':
            self.userDb.close()
            self.master.destroy()

    def about_of(self):
        showinfo('About', 'User Management System\\nVersion 2.0 (ORM-based)\\n\\nA simple CRUD application with SQLite and custom ORM')
'''

# Register window
register_py = '''import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.messagebox import askquestion, showinfo, showerror

from app.entities.user import User
from app.controllers.user import UserDB

class RegisterWn(tk.Toplevel):
    def __init__(self, master=None, type=1, userDb=None, user=None):
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

    def get_title(self):
        titles = {1: 'Register New User', 2: 'Update User', 3: 'Delete User'}
        return titles.get(self.type, 'User Form')

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_style = {'font': ('Segoe UI', 16, 'bold')}
        ttk.Label(main_frame, text=self.get_title(), **title_style).grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        self.entries = {}
        fields = [
            ('ID', 'id', tk.Entry, True),
            ('Name', 'name', ttk.Entry, False),
            ('First Name', 'firstname', ttk.Entry, False),
            ('Last Name', 'lastname', ttk.Entry, False),
            ('Phone Number', 'phonenumber', ttk.Entry, False),
            ('Email', 'email', ttk.Entry, False),
            ('Password', 'password', ttk.Entry, False),
        ]
        
        row = 1
        for label_text, attr, widget_class, is_readonly in fields:
            ttk.Label(main_frame, text="{}:".format(label_text), font=('Segoe UI', 10, 'bold')).grid(
                row=row, column=0, sticky='e', padx=(0, 10), pady=5)
            
            opts = {'width': 35, 'font': ('Segoe UI', 10)}
            
            if attr == 'password':
                opts['show'] = '•'
            
            if is_readonly and self.type in (2, 3):
                var = tk.StringVar()
                widget = tk.Entry(main_frame, textvariable=var, state='readonly', **opts)
                if attr == 'id':
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
            ttk.Button(button_frame, text='Register', command=self.submit_register).pack(side=tk.LEFT, padx=5)
        elif self.type == 2:
            ttk.Button(button_frame, text='Update', command=self.submit_update).pack(side=tk.LEFT, padx=5)
        elif self.type == 3:
            ttk.Button(button_frame, text='Delete', command=self.submit_delete).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text='Cancel', command=self.destroy).pack(side=tk.LEFT, padx=5)
        
        if self.type == 1:
            ttk.Button(button_frame, text='Clear', command=self.clear_fields).pack(side=tk.LEFT, padx=5)

    def disable_fields(self):
        for attr, widget in self.entries.items():
            if attr != 'id':
                widget.configure(state='disabled')

    def clear_fields(self):
        for attr, widget in self.entries.items():
            if attr not in ('id',):
                widget.delete(0, tk.END)

    def load_user_data(self):
        if self.type in (2, 3) and self.user:
            if hasattr(self, 'id_var'):
                self.id_var.set(str(self.user.id))
            if 'name' in self.entries:
                self.entries['name'].insert(0, self.user.name)
            if 'firstname' in self.entries:
                self.entries['firstname'].insert(0, self.user.firstname)
            if 'lastname' in self.entries:
                self.entries['lastname'].insert(0, self.user.lastname)
            if 'phonenumber' in self.entries:
                self.entries['phonenumber'].insert(0, self.user.phonenumber)
            if 'email' in self.entries:
                self.entries['email'].insert(0, self.user.email)
            if 'password' in self.entries and self.type != 3:
                if not self.user._is_hashed():
                    self.entries['password'].insert(0, self.user.password)

    def get_data(self):
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
'''

base_dir = r"C:\Users\User\Documents\Proyectos\Python\python_sqlite"

# Write files
with open(os.path.join(base_dir, "app", "interface", "main.py"), "w", encoding="utf-8") as f:
    f.write(main_py)

with open(os.path.join(base_dir, "app", "interface", "register.py"), "w", encoding="utf-8") as f:
    f.write(register_py)

print("Interface files created successfully!")
