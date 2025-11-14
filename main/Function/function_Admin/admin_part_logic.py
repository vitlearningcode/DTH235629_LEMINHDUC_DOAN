# main/Function/function_Admin/admin_part_logic.py

import tkinter as tk
from tkinter import messagebox

class AdminPartLogic:
    def __init__(self, view):
        self.view = view
        self.db = view.db

    def load_parts(self):
        for item in self.view.part_tree.get_children(): 
            self.view.part_tree.delete(item)
        query = """
            SELECT pt.MaPhuTung, pt.TenPhuTung, lpt.TenLoaiPhuTung, pt.DonViTinh, pt.GiaNhap, pt.GiaBan, pt.SoLuongTon
            FROM PhuTung pt
            LEFT JOIN LoaiPhuTung lpt ON pt.MaLoaiPhuTung = lpt.MaLoaiPhuTung
            ORDER BY pt.MaPhuTung
        """
        parts = self.db.fetch_all(query)
        for p in parts:
            self.view.part_tree.insert("", tk.END, values=(
                p['MaPhuTung'], p['TenPhuTung'], p['TenLoaiPhuTung'], p['DonViTinh'], 
                f"{p['GiaNhap']:,.0f}", f"{p['GiaBan']:,.0f}", p['SoLuongTon']
            ))

    def add_part(self): 
        messagebox.showinfo("Info", "Chức năng Thêm Phụ Tùng")
    
    def edit_part(self): 
        messagebox.showinfo("Info", "Chức năng Sửa Phụ Tùng")
    
    def delete_part(self): 
        messagebox.showinfo("Info", "Chức năng Xóa Phụ Tùng")