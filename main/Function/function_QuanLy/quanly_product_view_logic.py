# main/Function/function_QuanLy/quanly_product_view_logic.py
import tkinter as tk
class QuanLyProductViewLogic:
    def __init__(self, view):
        self.view = view
        self.db = view.db

    def load_view(self, tree):
        for item in tree.get_children():
            tree.delete(item)
        query = """
            SELECT sp.MaSanPham, sp.TenSanPham, hx.TenHangXe, lx.TenLoaiXe, sp.GiaBan, sp.SoLuongTon
            FROM SanPham sp
            LEFT JOIN HangXe hx ON sp.MaHangXe = hx.MaHangXe
            LEFT JOIN LoaiXe lx ON sp.MaLoaiXe = lx.MaLoaiXe
            ORDER BY sp.MaSanPham
        """
        records = self.db.fetch_all(query)
        if records:
            for rec in records:
                tree.insert("", tk.END, values=(
                    rec['MaSanPham'], rec['TenSanPham'], rec['TenHangXe'] or "N/A",
                    rec['TenLoaiXe'] or "N/A", f"{rec['GiaBan']:,.0f} VNĐ", rec['SoLuongTon']
                ))