# main/Function/function_QuanLy/quanly_system_logic.py
from tkinter import messagebox

class QuanLySystemLogic:
    def __init__(self, view):
        self.view = view
        self.db = view.db

    def logout(self):
        """Đăng xuất"""
        from login import Login # Import khi cần
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn đăng xuất?"):
            self.db.disconnect()
            self.view.window.destroy()
            Login().run()
    
    def on_closing(self):
        """Xử lý đóng cửa sổ"""
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn thoát?"):
            self.db.disconnect()
            self.view.window.destroy()