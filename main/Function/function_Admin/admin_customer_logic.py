# main/Function/function_Admin/admin_customer_logic.py

import tkinter as tk
from tkinter import messagebox

class AdminCustomerLogic:
    def __init__(self, view):
        self.view = view
        self.db = view.db

    def load_customers(self):
        for item in self.view.customer_tree.get_children(): 
            self.view.customer_tree.delete(item)
        
        query = """
            SELECT TOP 100 MaKhachHang, HoTen, SoDienThoai, Email, DiaChi, 
                   LoaiKhachHang, FORMAT(NgayTao, 'dd/MM/yyyy') as NgayTao
            FROM KhachHang
            ORDER BY MaKhachHang DESC
        """
        try:
            customers = self.db.fetch_all(query)
            for c in customers:
                self.view.customer_tree.insert("", tk.END, values=(
                    c['MaKhachHang'], c['HoTen'], c['SoDienThoai'], c['Email'], c['DiaChi'], c['LoaiKhachHang'], c['NgayTao']
                ))
        except Exception as e:
            messagebox.showerror("Lỗi Query", str(e))

    def search_customers(self, keyword):
        # Đây mới chỉ là placeholder, bạn có thể nâng cấp sau
        messagebox.showinfo("Info", f"Tìm kiếm: {keyword}")
        # (Sau khi nâng cấp, bạn sẽ gọi self.load_customers(keyword) ở đây)