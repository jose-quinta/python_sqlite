import tkinter as tk
from tkinter import ttk
from typing import Optional


class MainWn(tk.Frame):
    def __init__(self, master: tk.Tk | None = None):
        super().__init__(master=master)

        self.configure(bg='#f0f0f0')
        self.pack(fill=tk.BOTH, expand=True)

        self.master.title('Management System')
        self.master.geometry('1000x600')
        self.master.minsize(800, 500)

        self.setup_layout()
        self.show_dashboard()

    def setup_layout(self):
        self.header = tk.Frame(self, bg='#2c3e50', height=80)
        self.header.pack(fill=tk.X)
        self.header.pack_propagate(False)

        self.content_frame = tk.Frame(self, bg='#f0f0f0')
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        self.footer = tk.Frame(self, bg='#34495e', height=30)
        self.footer.pack(fill=tk.X, side=tk.BOTTOM)
        self.footer.pack_propagate(False)

        tk.Label(self.header, text='Management System',
                 font=('Segoe UI', 18, 'bold'),
                 fg='white', bg='#2c3e50').place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(self.footer, text='v3.0',
                 font=('Segoe UI', 8), fg='white', bg='#34495e').pack(expand=True)

    def clear_content(self):
        for w in self.content_frame.winfo_children():
            w.destroy()

    def show_dashboard(self):
        self.clear_content()

        nav_frame = tk.Frame(self.content_frame, bg='#f0f0f0')
        nav_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        card = tk.Frame(nav_frame, bg='white', highlightbackground='#d5d5d5',
                        highlightthickness=1, cursor='hand2')
        card.pack(padx=20, ipadx=40, ipady=30)

        card_content = tk.Frame(card, bg='white')
        card_content.pack(expand=True, padx=10, pady=10)

        icon_label = tk.Label(card_content, text='[ Users ]',
                              font=('Segoe UI', 16, 'bold'),
                              fg='#2c3e50', bg='#ecf0f1',
                              width=12, height=2)
        icon_label.pack(pady=(0, 10))

        tk.Label(card_content, text='User Management',
                 font=('Segoe UI', 14, 'bold'),
                 bg='white').pack()

        tk.Label(card_content, text='Register, edit, delete and list system users',
                 font=('Segoe UI', 10), fg='#7f8c8d',
                 bg='white', justify=tk.CENTER).pack(pady=(5, 10))

        ttk.Button(card_content, text='Open',
                   command=self.show_user_management).pack(pady=(5, 0))

        for widget in (card, card_content, icon_label):
            widget.bind('<Button-1>', lambda e: self.show_user_management(), add='+')

    def show_user_management(self):
        from app.interface.user_mgmt import UserManagementWn

        self.clear_content()
        UserManagementWn(
            master=self.content_frame,
            on_exit=self.show_dashboard
        )
