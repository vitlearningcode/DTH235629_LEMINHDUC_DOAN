# main/Function/function_NhanVien/nhanvien_invoice_logic.py

import tkinter as tk
from tkinter import messagebox, ttk

class NhanVienInvoiceLogic:
    def __init__(self, view):
        self.view = view
        self.db = view.db

    def load_invoice_history(self):
        """Tải danh sách hóa đơn do nhân viên này lập"""
        for item in self.view.invoice_tree.get_children():
            self.view.invoice_tree.delete(item)
            
        query = """
            SELECT TOP 100
                hd.MaHoaDon,
                kh.HoTen as TenKhachHang,
                FORMAT(hd.NgayLap, 'dd/MM/yyyy HH:mm') as NgayLap,
                hd.TongThanhToan,
                hd.TrangThai
            FROM HoaDon hd
            JOIN KhachHang kh ON hd.MaKhachHang = kh.MaKhachHang
            WHERE hd.MaNguoiDung = %s
            ORDER BY hd.MaHoaDon DESC
        """
        try:
            invoices = self.db.fetch_all(query, (self.view.user_info['MaNguoiDung'],))
            
            if invoices:
                for inv in invoices:
                    self.view.invoice_tree.insert("", tk.END, values=(
                        inv['MaHoaDon'],
                        inv['TenKhachHang'],
                        inv['NgayLap'],
                        f"{inv['TongThanhToan']:,.0f}",
                        inv['TrangThai']
                    ))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải lịch sử hóa đơn: {e}")

    def show_invoice_details(self):
        """Hiển thị chi tiết một hóa đơn"""
        selected = self.view.invoice_tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một hóa đơn để xem!")
            return
            
        item = self.view.invoice_tree.item(selected[0])
        invoice_id = item['values'][0]
        
        dialog = tk.Toplevel(self.view.window)
        dialog.title(f"Chi tiết Hóa đơn #{invoice_id}")
        dialog.geometry("700x500")
        dialog.resizable(False, False)
        
        # Frame Sản phẩm
        sp_frame = tk.LabelFrame(dialog, text="Chi tiết Sản phẩm (Xe máy)", 
                                 font=("Arial", 12, "bold"), padx=10, pady=10)
        sp_frame.pack(fill=tk.X, expand=True, padx=20, pady=10)
        
        cols_sp = ("Tên sản phẩm", "Số lượng", "Đơn giá", "Thành tiền")
        sp_tree = ttk.Treeview(sp_frame, columns=cols_sp, show="headings", height=5)
        for col in cols_sp: sp_tree.heading(col, text=col)
        sp_tree.pack(fill=tk.BOTH, expand=True)

        query_sp = """
            SELECT sp.TenSanPham, cthd.SoLuong, cthd.DonGia
            FROM ChiTietHoaDonSanPham cthd
            JOIN SanPham sp ON cthd.MaSanPham = sp.MaSanPham
            WHERE cthd.MaHoaDon = %s
        """
        products = self.db.fetch_all(query_sp, (invoice_id,))
        if products:
            for p in products:
                thanh_tien = p['SoLuong'] * p['DonGia']
                sp_tree.insert("", tk.END, values=(
                    p['TenSanPham'], 
                    p['SoLuong'], 
                    f"{p['DonGia']:,.0f}", 
                    f"{thanh_tien:,.0f}"
                ))

        # Frame Phụ tùng
        pt_frame = tk.LabelFrame(dialog, text="Chi tiết Phụ tùng & Dịch vụ", 
                                 font=("Arial", 12, "bold"), padx=10, pady=10)
        pt_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        cols_pt = ("Tên phụ tùng", "Số lượng", "Đơn giá", "Thành tiền")
        pt_tree = ttk.Treeview(pt_frame, columns=cols_pt, show="headings", height=5)
        for col in cols_pt: pt_tree.heading(col, text=col)
        pt_tree.pack(fill=tk.BOTH, expand=True)

        query_pt = """
            SELECT pt.TenPhuTung, cthd.SoLuong, cthd.DonGia
            FROM ChiTietHoaDonPhuTung cthd
            JOIN PhuTung pt ON cthd.MaPhuTung = pt.MaPhuTung
            WHERE cthd.MaHoaDon = %s
        """
        parts = self.db.fetch_all(query_pt, (invoice_id,))
        if parts:
            for p in parts:
                thanh_tien = p['SoLuong'] * p['DonGia']
                pt_tree.insert("", tk.END, values=(
                    p['TenPhuTung'], 
                    p['SoLuong'], 
                    f"{p['DonGia']:,.0f}", 
                    f"{thanh_tien:,.0f}"
                ))

        tk.Button(
            dialog, 
            text="Đóng", 
            font=("Arial", 11, "bold"), 
            bg="#dc3545", 
            fg="white", 
            command=dialog.destroy
        ).pack(pady=10)