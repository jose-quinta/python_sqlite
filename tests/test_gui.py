#!/usr/bin/env python3
"""GUI test for ORM-based application - loads without displaying"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Initialize database
from app.data.db import init_db
init_db()

import tkinter as tk

def test_gui_loads():
    """Test that GUI components load without errors"""
    print("Test GUI: Loading interface components...")

    # Test that we can import and create the dashboard and user management windows
    from app.interface.main import MainWn
    print("  MainWn imported OK")

    from app.interface.user_mgmt import UserManagementWn
    print("  UserManagementWn imported OK")

    from app.interface.register import RegisterWn
    print("  RegisterWn imported OK")

    # Create root window (but don't display it)
    root = tk.Tk()
    root.withdraw()  # Hide the window

    try:
        dash_app = MainWn(master=root)
        print("  MainWn (Dashboard) created OK")

        container = tk.Frame(root)
        container.pack()
        mgmt_app = UserManagementWn(master=container, on_exit=lambda: None)
        print("  UserManagementWn embedded OK")

        from app.entities.user import User
        from app.controllers.user import UserDB

        test_user = User()
        test_user.name = "GUI"
        test_user.firstname = "Test";
        test_user.lastname = "User";
        test_user.email = "gui@example.com";
        test_user.set_password("test123");

        reg_container = tk.Frame(root)
        reg_container.pack()
        reg_called = [False]
        def on_reg_complete(refresh):
            reg_called[0] = True
        reg_win = RegisterWn(master=reg_container, type=1, userDb=UserDB(), user=test_user, on_complete=on_reg_complete)
        print("  RegisterWn created OK")
        reg_win.destroy()
        reg_container.destroy()

        mgmt_app.destroy()
        container.destroy()
        dash_app.destroy()
        print("  PASSED")
        return True
    except Exception as e:
        print(f"  FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        root.destroy()

if __name__ == "__main__":
    print("=" * 50)
    print("GUI Test for ORM-based Application")
    print("=" * 50)
    print()

    try:
        if test_gui_loads():
            print()
            print("=" * 50)
            print("GUI TEST PASSED!")
            print("=" * 50)
            sys.exit(0)
        else:
            print()
            print("GUI TEST FAILED!")
            sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
