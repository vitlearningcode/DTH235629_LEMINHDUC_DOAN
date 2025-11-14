# main/Function/function_QuanLy/quanly_invoice_view_logic.py
import tkinter as tk
class QuanLyInvoiceViewLogic:
    def __init__(self, view):
        self.view = view
        self.db = view.db

    def load_view(self, tree):
        for item in tree.get_children():
            tree.delete(item)
        query = """
            SELECT 
                MaHoaDon, FORMAT(NgayLap, 'dd/MM/yyyy HH:mm') as NgayLapFormatted, 
                TenKhachHang, NhanVienLap, TongThanhToan, TienConNo, TrangThai
            FROM v_ChiTietHoaDon
            ORDER BY MaHoaDon DESC
        """
        records = self.db.fetch_all(query)
        if records:
            for rec in records:
                tree.insert("", tk.END, values=(
                    rec['MaHoaDon'], rec['NgayLapFormatted'], rec['TenKhachHang'],
                    rec['NhanVienLap'], f"{rec['TongThanhToan']:,.0f} VNĐ",
                    f"{rec['TienConNo']:,.0f} VNĐ", rec['TrangThai']
                ))