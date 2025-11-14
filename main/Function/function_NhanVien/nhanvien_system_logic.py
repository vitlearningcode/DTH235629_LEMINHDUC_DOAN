# main/Function/function_NhanVien/nhanvien_system_logic.py

from tkinter import messagebox
# 1. KHÔNG IMPORT LOGIN Ở ĐÂY
# from login import Login  <-- XÓA DÒNG NÀY

class NhanVienSystemLogic:
    def __init__(self, view):
        self.view = view
        self.db = view.db

    def logout(self):
        """Đăng xuất"""
        # 2. IMPORT LOGIN TẠI ĐÂY
        from login import Login 

        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn đăng xuất?"):
            self.db.disconnect()
            self.view.window.destroy()
            Login().run() # Tạo mới và chạy cửa sổ Login
    
    def on_closing(self):
        """Xử lý đóng cửa sổ"""
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn thoát?"):
            self.db.disconnect()
            self.view.window.destroy()