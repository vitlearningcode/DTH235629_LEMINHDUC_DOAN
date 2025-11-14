# main/Function/function_QuanLy/quanly_employee_view_logic.py
# (Hãy đảm bảo tên class là 'QuanLyEmployeeViewLogic')

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
            # SQL Server dùng '?' làm placeholder, database_connection.py sẽ tự đổi %s
            # Nhưng để an toàn, ta dùng '?'
            params.extend([f"%{keyword}%", f"%{keyword}%"])
            
        query += " ORDER BY MaNguoiDung"
        
        records = self.db.fetch_all(query, params)
        
        if records:
            for rec in records:
                tree.insert("", tk.END, values=(
                    rec['MaNguoiDung'], rec['HoTen'], rec['SoDienThoai'] or "",
                    rec['Email'] or "", rec['VaiTro'], rec['TrangThai']
                ))