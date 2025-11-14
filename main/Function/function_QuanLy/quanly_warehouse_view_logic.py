# main/Function/function_QuanLy/quanly_warehouse_view_logic.py
import tkinter as tk

class QuanLyWarehouseViewLogic:
    def __init__(self, view):
        self.view = view
        self.db = view.db

    def load_view(self, tree, keyword=None):
        """Tải dữ liệu Xem kho (Phiếu nhập), có hỗ trợ tìm kiếm"""
        for item in tree.get_children():
            tree.delete(item)
            
        query = """
            SELECT TOP 100 
                p.MaPhieuNhap, n.TenNhaCungCap, nd.HoTen AS NguoiNhap, 
                FORMAT(p.NgayNhap, 'dd/MM/yyyy HH:mm') as NgayNhap,
                p.TongTien, p.TrangThai
            FROM PhieuNhapKho p
            LEFT JOIN NhaCungCap n ON p.MaNhaCungCap = n.MaNhaCungCap
            LEFT JOIN NguoiDung nd ON p.MaNguoiDung = nd.MaNguoiDung
        """
        params = []

        if keyword:
            query += " WHERE n.TenNhaCungCap LIKE ? OR CAST(p.MaPhieuNhap AS VARCHAR(20)) = ?"
            params.extend([f"%{keyword}%", keyword])

        query += " ORDER BY p.MaPhieuNhap DESC"
        
        records = self.db.fetch_all(query, params)
        
        if records:
            for rec in records:
                tree.insert("", tk.END, values=(
                    rec['MaPhieuNhap'], rec['TenNhaCungCap'] or "N/A", rec['NguoiNhap'] or "N/A",
                    rec['NgayNhap'], f"{rec['TongTien']:,.0f} VNĐ", rec['TrangThai']
                ))