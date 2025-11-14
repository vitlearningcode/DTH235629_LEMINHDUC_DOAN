# main/Function/function_QuanLy/quanly_report_view_logic.py
import tkinter as tk
class QuanLyReportViewLogic:
    def __init__(self, view):
        self.view = view
        self.db = view.db

    def load_view(self, tree):
        for item in tree.get_children():
            tree.delete(item)
        query = "EXEC sp_ThongKeTonKhoSanPham"
        records = self.db.fetch_all(query)
        if records:
            for rec in records:
                tree.insert("", tk.END, values=(
                    rec['MaSanPham'], rec['TenSanPham'], rec['TenHangXe'],
                    rec['TenLoaiXe'], rec['SoLuongTon'], f"{rec['GiaTriTonKho']:,.0f} VNĐ"
                ))