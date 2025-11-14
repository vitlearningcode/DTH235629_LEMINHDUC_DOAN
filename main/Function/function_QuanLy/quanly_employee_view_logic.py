# main/Function/function_QuanLy/quanly_employee_view_logic.py
import tkinter as tk
class QuanLyEmployeeViewLogic:
    def __init__(self, view):
        self.view = view
        self.db = view.db

    def load_view(self, tree):
        for item in tree.get_children():
            tree.delete(item)
        query = """
            SELECT MaNguoiDung, HoTen, SoDienThoai, Email, VaiTro, TrangThai
            FROM NguoiDung
            WHERE VaiTro = 'NhanVien' OR VaiTro = 'QuanLy'
            ORDER BY MaNguoiDung
        """
        records = self.db.fetch_all(query)
        if records:
            for rec in records:
                tree.insert("", tk.END, values=(
                    rec['MaNguoiDung'], rec['HoTen'], rec['SoDienThoai'] or "",
                    rec['Email'] or "", rec['VaiTro'], rec['TrangThai']
                ))