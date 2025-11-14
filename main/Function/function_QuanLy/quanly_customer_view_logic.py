# main/Function/function_QuanLy/quanly_customer_view_logic.py
import tkinter as tk
class QuanLyCustomerViewLogic:
    def __init__(self, view):
        self.view = view
        self.db = view.db

    def load_view(self, tree):
        for item in tree.get_children():
            tree.delete(item)
        query = """
            SELECT MaKhachHang, HoTen, SoDienThoai, DiaChi, LoaiKhachHang
            FROM KhachHang
            ORDER BY MaKhachHang DESC
        """
        records = self.db.fetch_all(query)
        if records:
            for rec in records:
                tree.insert("", tk.END, values=(
                    rec['MaKhachHang'], rec['HoTen'], rec['SoDienThoai'],
                    rec['DiaChi'] or "", rec['LoaiKhachHang']
                ))