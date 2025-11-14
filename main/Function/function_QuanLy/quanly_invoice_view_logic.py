# main/Function/function_QuanLy/quanly_invoice_view_logic.py
import tkinter as tk

class QuanLyInvoiceViewLogic:
    def __init__(self, view):
        self.view = view
        self.db = view.db

    def load_view(self, tree, keyword=None):
        """Tải dữ liệu Xem hóa đơn, có hỗ trợ tìm kiếm"""
        for item in tree.get_children():
            tree.delete(item)
            
        query = """
            SELECT 
                MaHoaDon, FORMAT(NgayLap, 'dd/MM/yyyy HH:mm') as NgayLapFormatted, 
                TenKhachHang, NhanVienLap, TongThanhToan, TienConNo, TrangThai, SoDienThoai
            FROM v_ChiTietHoaDon
        """
        params = []
        
        if keyword:
            # Cho phép tìm theo Tên, SĐT, hoặc Mã Hóa Đơn
            query += " WHERE TenKhachHang LIKE ? OR SoDienThoai LIKE ? OR CAST(MaHoaDon AS VARCHAR(20)) = ?"
            params.extend([f"%{keyword}%", f"%{keyword}%", keyword])
            
        query += " ORDER BY MaHoaDon DESC"
        
        records = self.db.fetch_all(query, params)
        
        if records:
            for rec in records:
                tree.insert("", tk.END, values=(
                    rec['MaHoaDon'], rec['NgayLapFormatted'], rec['TenKhachHang'],
                    rec['NhanVienLap'], f"{rec['TongThanhToan']:,.0f} VNĐ",
                    f"{rec['TienConNo']:,.0f} VNĐ", rec['TrangThai']
                ))