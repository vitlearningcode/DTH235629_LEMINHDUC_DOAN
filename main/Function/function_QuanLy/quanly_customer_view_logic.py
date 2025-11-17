# main/Function/function_QuanLy/quanly_customer_view_logic.py
import tkinter as tk

class QuanLyCustomerViewLogic:
    def __init__(self, view):
        self.view = view
        self.db = view.db
        
        # Ánh xạ Loại Khách Hàng sang Tiếng Việt
        self.customer_type_map = {
            'ThanThiet': 'VIP',
            'ThongThuong': 'Thường',
            'TiemNang': 'Tiềm Năng',
        }

    def load_view(self, tree, keyword=None):
        """Tải dữ liệu Xem khách hàng, có hỗ trợ tìm kiếm"""
        for item in tree.get_children():
            tree.delete(item)
            
        query = "SELECT MaKhachHang, HoTen, SoDienThoai, DiaChi, LoaiKhachHang FROM KhachHang"
        params = []
        
        if keyword:
            query += " WHERE HoTen LIKE %s OR SoDienThoai LIKE %s"
            params.extend([f"%{keyword}%", f"%{keyword}%"])
            
        query += " ORDER BY MaKhachHang DESC"
        
        records = self.db.fetch_all(query, params)
        
        if records:
            for rec in records:
                # Ánh xạ loại khách hàng
                display_type = self.customer_type_map.get(rec['LoaiKhachHang'], rec['LoaiKhachHang'])
                
                tree.insert("", tk.END, values=(
                    rec['MaKhachHang'], rec['HoTen'], rec['SoDienThoai'],
                    rec['DiaChi'] or "", display_type
                ))