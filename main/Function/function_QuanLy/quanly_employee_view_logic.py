# main/Function/function_QuanLy/quanly_employee_view_logic.py
# (ĐÃ SỬA LỖI BIẾN)

import tkinter as tk

class QuanLyEmployeeViewLogic:
    def __init__(self, view):
        self.view = view
        self.db = view.db

    def load_view(self, tree, keyword=None):
        """Tải dữ liệu Xem nhân viên, có hỗ trợ tìm kiếm"""
        for item in tree.get_children():
            tree.delete(item)
        
        query = """
            SELECT MaNguoiDung, HoTen, SoDienThoai, Email, VaiTro, TrangThai
            FROM NguoiDung
            WHERE (VaiTro = 'NhanVien' OR VaiTro = 'QuanLy')
        """
        params = []
        
        if keyword:
            query += " AND (HoTen LIKE ? OR SoDienThoai LIKE ?)"
            params.extend([f"%{keyword}%", f"%{keyword}%"])
            
        query += " ORDER BY MaNguoiDung"
        
        # --- SỬA LỖI TẠI ĐÂY ---
        # 1. Dùng tên 'records' (hoặc bất cứ tên nào)
        records = self.db.fetch_all(query, params)
        
        if records:
            # 2. Duyệt đúng biến 'records'
            for rec in records: 
                # 3. Dùng đúng biến 'rec'
                tree.insert("", tk.END, values=(
                    rec['MaNguoiDung'], rec['HoTen'], rec['SoDienThoai'] or "",
                    rec['Email'] or "", rec['VaiTro'], rec['TrangThai']
                ))