import tkinter as tk
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.data.db import init_db, close_db
from app.interface.main import MainWn

if __name__ == '__main__':
    init_db()
    root = tk.Tk()
    app = MainWn(master=root)
    root.mainloop()
    close_db()
