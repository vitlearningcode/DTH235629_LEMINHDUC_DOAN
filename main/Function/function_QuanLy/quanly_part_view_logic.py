# main/Function/function_QuanLy/quanly_part_view_logic.py
import tkinter as tk

class QuanLyPartViewLogic:
    def __init__(self, view):
        self.view = view
        self.db = view.db

    def load_view(self, tree, keyword=None):
        """Tải dữ liệu Xem phụ tùng, có hỗ trợ tìm kiếm"""
        for item in tree.get_children():
            tree.delete(item)
            
        query = """
            SELECT pt.MaPhuTung, pt.TenPhuTung, lpt.TenLoaiPhuTung, pt.GiaBan, pt.SoLuongTon
            FROM PhuTung pt
            LEFT JOIN LoaiPhuTung lpt ON pt.MaLoaiPhuTung = lpt.MaLoaiPhuTung
        """
        params = []
        
        if keyword:
            query += " WHERE pt.TenPhuTung LIKE %s" # <-- SỬA LỖI
            params.append(f"%{keyword}%")
            
        query += " ORDER BY pt.MaPhuTung"
        
        records = self.db.fetch_all(query, params)
        
        if records:
            for rec in records:
                tree.insert("", tk.END, values=(
                    rec['MaPhuTung'], rec['TenPhuTung'], rec['TenLoaiPhuTung'] or "N/A",
                    f"{rec['GiaBan']:,.0f} VNĐ", rec['SoLuongTon']
                ))