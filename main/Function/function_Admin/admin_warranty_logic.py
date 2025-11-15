# Mở file mới: main/Function/function_Admin/admin_warranty_logic.py

import tkinter as tk
from tkinter import messagebox, ttk

class AdminWarrantyLogic:
    def __init__(self, view):
        """Khởi tạo logic cho màn hình Quản lý Bảo hành (Admin)"""
        self.view = view
        self.db = view.db

    def load_all_warranties(self, keyword=None):
        """Tải TẤT CẢ các phiếu bảo hành, hỗ trợ tìm kiếm"""
        
        for item in self.view.warranty_tree.get_children():
            self.view.warranty_tree.delete(item)
        
        #
        query = """
            SELECT TOP 200
                pb.MaPhieuBaoHanh, 
                kh.HoTen AS TenKhachHang,
                kh.SoDienThoai,
                sp.TenSanPham, 
                FORMAT(pb.NgayBatDau, 'dd/MM/yyyy') as NgayBatDau, 
                FORMAT(pb.NgayKetThuc, 'dd/MM/yyyy') as NgayKetThuc,
                pb.TrangThai
            FROM PhieuBaoHanh pb
            JOIN SanPham sp ON pb.MaSanPham = sp.MaSanPham
            JOIN KhachHang kh ON pb.MaKhachHang = kh.MaKhachHang
        """
        params = []
        
        if keyword:
            query += " WHERE kh.HoTen LIKE %s OR kh.SoDienThoai LIKE %s OR sp.TenSanPham LIKE %s"
            params.extend([f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"])
            
        query += " ORDER BY pb.MaPhieuBaoHanh DESC"
        
        try:
            records = self.db.fetch_all(query, params)
            if records:
                for rec in records:
                    self.view.warranty_tree.insert("", tk.END, values=(
                        rec['MaPhieuBaoHanh'],
                        rec['TenKhachHang'],
                        rec['SoDienThoai'],
                        rec['TenSanPham'],
                        rec['NgayBatDau'],
                        rec['NgayKetThuc'],
                        rec['TrangThai']
                    ))
            else:
                self.view.warranty_tree.insert("", tk.END, values=("", "Không tìm thấy phiếu bảo hành nào.", "", "", "", "", ""))
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Không thể tải danh sách bảo hành: {e}")

    def on_warranty_select(self, event=None):
        """Khi Admin click vào một phiếu bảo hành, tải lịch sử của phiếu đó"""
        # Xóa cây lịch sử trước
        for item in self.view.history_tree.get_children():
            self.view.history_tree.delete(item)
            
        try:
            selected = self.view.warranty_tree.selection()
            if not selected:
                return
            
            item = self.view.warranty_tree.item(selected[0])
            warranty_id = item['values'][0]
            if not warranty_id:
                return

            self.load_warranty_history(warranty_id)
        except Exception as e:
            pass # Bỏ qua lỗi

    def load_warranty_history(self, warranty_id):
        """Tải lịch sử sửa chữa của một phiếu bảo hành cụ thể"""
        #
        query = """
            SELECT 
                ls.MaLichSu,
                FORMAT(ls.NgaySuaChua, 'dd/MM/yyyy') as NgaySuaChua, 
                ls.MoTaLoi, 
                nd.HoTen AS NguoiXuLy, 
                ls.ChiPhiPhatSinh,
                ls.TrangThai
            FROM LichSuBaoHanh ls
            LEFT JOIN NguoiDung nd ON ls.NguoiXuLy = nd.MaNguoiDung
            WHERE ls.MaPhieuBaoHanh = %s
            ORDER BY ls.NgaySuaChua DESC
        """
        records = self.db.fetch_all(query, (warranty_id,))
        
        if records:
            for rec in records:
                self.view.history_tree.insert("", tk.END, values=(
                    rec['MaLichSu'],
                    rec['NgaySuaChua'],
                    rec['MoTaLoi'],
                    rec['NguoiXuLy'] or "Không rõ",
                    f"{rec['ChiPhiPhatSinh']:,.0f} VNĐ",
                    rec['TrangThai']
                ))
        else:
            self.view.history_tree.insert("", tk.END, values=("", "Phiếu này chưa có lịch sử sửa chữa.", "", "", "", ""))

    def delete_history_entry(self):
        """Xóa một mục LỊCH SỬ SỬA CHỮA"""
        selected = self.view.history_tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một mục trong bảng 'Lịch Sử Sửa Chữa' (bên phải) để xóa.")
            return

        item = self.view.history_tree.item(selected[0])
        history_id = item['values'][0]
        history_desc = item['values'][2]
        
        if not history_id:
            return

        if messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc muốn XÓA VĨNH VIỄN mục lịch sử:\n\n'{history_desc}' (ID: {history_id})"):
            try:
                #
                query = "DELETE FROM LichSuBaoHanh WHERE MaLichSu = %s"
                result = self.db.execute_query(query, (history_id,))
                
                if result:
                    messagebox.showinfo("Thành công", "Đã xóa mục lịch sử sửa chữa.")
                    self.on_warranty_select() # Tải lại lịch sử
                else:
                    messagebox.showerror("Lỗi", "Xóa thất bại.")
            except Exception as e:
                messagebox.showerror("Lỗi CSDL", f"Không thể xóa: {e}")

    def delete_warranty_entry(self):
        """Xóa toàn bộ PHIẾU BẢO HÀNH (và các lịch sử liên quan)"""
        selected = self.view.warranty_tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một 'Phiếu Bảo Hành' (bên trái) để xóa.")
            return

        item = self.view.warranty_tree.item(selected[0])
        warranty_id = item['values'][0]
        warranty_desc = item['values'][3] # Tên xe
        
        if not warranty_id:
            return

        if messagebox.askyesno("Xác nhận xóa", 
            f"BẠN CÓ CHẮC MUỐN XÓA TOÀN BỘ PHIẾU BẢO HÀNH?\n\n"
            f"Xe: {warranty_desc} (ID Phiếu: {warranty_id})\n\n"
            f"CẢNH BÁO: Toàn bộ lịch sử sửa chữa liên quan đến phiếu này cũng sẽ bị XÓA VĨNH VIỄN.",
            icon='warning'):
            
            try:
                # Phải xóa lịch sử trước do ràng buộc khóa ngoại
                query_history = "DELETE FROM LichSuBaoHanh WHERE MaPhieuBaoHanh = %s"
                self.db.execute_query(query_history, (warranty_id,))
                
                # Xóa phiếu bảo hành
                query_warranty = "DELETE FROM PhieuBaoHanh WHERE MaPhieuBaoHanh = %s"
                result = self.db.execute_query(query_warranty, (warranty_id,))

                if result:
                    messagebox.showinfo("Thành công", "Đã xóa toàn bộ phiếu bảo hành và lịch sử liên quan.")
                    self.load_all_warranties() # Tải lại danh sách phiếu
                    # Xóa cây lịch sử
                    for item in self.view.history_tree.get_children():
                        self.view.history_tree.delete(item)
                else:
                    messagebox.showerror("Lỗi", "Xóa thất bại (bước xóa Phiếu Bảo Hành).")
            except Exception as e:
                messagebox.showerror("Lỗi CSDL", f"Không thể xóa: {e}")