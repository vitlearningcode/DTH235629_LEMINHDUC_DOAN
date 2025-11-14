# main/Function/function_QuanLy/quanly_part_view_logic.py
import tkinter as tk
class QuanLyPartViewLogic:
    def __init__(self, view):
        self.view = view
        self.db = view.db

    def load_view(self, tree):
        for item in tree.get_children():
            tree.delete(item)
        query = """
            SELECT pt.MaPhuTung, pt.TenPhuTung, lpt.TenLoaiPhuTung, pt.GiaBan, pt.SoLuongTon
            FROM PhuTung pt
            LEFT JOIN LoaiPhuTung lpt ON pt.MaLoaiPhuTung = lpt.MaLoaiPhuTung
            ORDER BY pt.MaPhuTung
        """
        records = self.db.fetch_all(query)
        if records:
            for rec in records:
                tree.insert("", tk.END, values=(
                    rec['MaPhuTung'], rec['TenPhuTung'], rec['TenLoaiPhuTung'] or "N/A",
                    f"{rec['GiaBan']:,.0f} VNĐ", rec['SoLuongTon']
                ))