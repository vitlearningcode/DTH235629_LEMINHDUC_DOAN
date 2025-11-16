# main/Function/function_QuanLy/quanly_customer_view_logic.py
import tkinter as tk

class QuanLyCustomerViewLogic:
    def __init__(self, view):
        self.view = view
        self.db = view.db

    def load_view(self, tree, keyword=None):
        """Tải dữ liệu Xem khách hàng, có hỗ trợ tìm kiếm"""
        for item in tree.get_children():
            tree.delete(item)
            
        query = "SELECT MaKhachHang, HoTen, SoDienThoai, DiaChi, LoaiKhachHang FROM KhachHang"
        params = []
        
        if keyword:
            query += " WHERE HoTen LIKE %s OR SoDienThoai LIKE %s" # <-- SỬA LỖI
            params.extend([f"%{keyword}%", f"%{keyword}%"])
            
        query += " ORDER BY MaKhachHang DESC"
        
        records = self.db.fetch_all(query, params)
        
        if records:
            for rec in records:
                tree.insert("", tk.END, values=(
                    rec['MaKhachHang'], rec['HoTen'], rec['SoDienThoai'],
                    rec['DiaChi'] or "", rec['LoaiKhachHang']
                ))