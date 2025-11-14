# main/Function/function_Admin/admin_product_logic.py

import tkinter as tk
from tkinter import messagebox

class AdminProductLogic:
    def __init__(self, view):
        self.view = view
        self.db = view.db

    def load_products(self):
        for item in self.view.product_tree.get_children(): 
            self.view.product_tree.delete(item)
        query = """
            SELECT sp.MaSanPham, sp.TenSanPham, hx.TenHangXe, lx.TenLoaiXe,
                   sp.MauSac, sp.GiaBan, sp.SoLuongTon, sp.TrangThai
            FROM SanPham sp
            LEFT JOIN HangXe hx ON sp.MaHangXe = hx.MaHangXe
            LEFT JOIN LoaiXe lx ON sp.MaLoaiXe = lx.MaLoaiXe
            ORDER BY sp.MaSanPham
        """
        products = self.db.fetch_all(query)
        for p in products:
            self.view.product_tree.insert("", tk.END, values=(
                p['MaSanPham'], p['TenSanPham'], p['TenHangXe'], p['TenLoaiXe'],
                p['MauSac'], f"{p['GiaBan']:,.0f}", p['SoLuongTon'], p['TrangThai']
            ))

    def add_product(self): 
        messagebox.showinfo("Info", "Chức năng Thêm Sản Phẩm")
    
    def edit_product(self): 
        messagebox.showinfo("Info", "Chức năng Sửa Sản Phẩm")
    
    def delete_product(self): 
        messagebox.showinfo("Info", "Chức năng Xóa Sản Phẩm")