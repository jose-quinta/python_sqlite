import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.messagebox import askquestion, showinfo
from typing import Optional

from app.entities.user import User
from app.interface.register import RegisterWn
from app.controllers.user import UserDB


class UserManagementWn(tk.Frame):
    def __init__(self, master: tk.Tk | None = None, on_exit: Optional[callable] = None):
        super().__init__(master=master)

        self.on_exit = on_exit
        self.userDb = UserDB()

        self.configure(bg='#f0f0f0')
        self.pack(fill=tk.BOTH, expand=True)

        if hasattr(self.master, 'title'):
            self.master.title('User Management System')
        if hasattr(self.master, 'geometry'):
            self.master.geometry('1000x600')
        if hasattr(self.master, 'minsize'):
            self.master.minsize(800, 500)

        self.setup_ui()
        self.load_users()

    def setup_ui(self):
        self.setup_menu()
        self.setup_toolbar()
        self.setup_table()
        self.setup_statusbar()

    def setup_menu(self):
        if not isinstance(self.master, (tk.Tk, tk.Toplevel)):
            return

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
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)
        except tk.TclError:
            return

        users = self.userDb.select_users()

        try:
            for user in users:
                data = user.to_tuple()
                display_data = list(data)
                if user._is_hashed():
                    display_data[6] = '******'
                self.tree.insert('', tk.END, values=display_data)

            self.status_bar.config(text="Total users: {}".format(len(users)))
        except tk.TclError:
            pass

    def open_register(self, type_val: int):
        selected = self.tree.selection()

        if type_val in (2, 3) and not selected:
            messagebox.showwarning('No Selection', 'Please select a user from the table')
            return

        user_to_edit = None
        if type_val in (2, 3) and selected:
            item = self.tree.item(selected[0])
            user_id = int(item['values'][0])
            user_to_edit: Optional[User | object | None] = self.userDb.select_user(user_id)

        registerWn = RegisterWn(self, type=type_val, userDb=self.userDb, user=user_to_edit)
        self.wait_window(registerWn)
        self.load_users()

    def exit_application(self):
        if askquestion('Exit', 'Are you sure you want to exit?') == 'yes':
            self.userDb.close()
            if self.on_exit:
                self.destroy()
                self.on_exit()
            else:
                self.master.destroy()

    def about_of(self):
        showinfo('About', 'User Management System\nVersion 2.0 (ORM-based)\n\nA simple CRUD application with SQLite and custom ORM')
