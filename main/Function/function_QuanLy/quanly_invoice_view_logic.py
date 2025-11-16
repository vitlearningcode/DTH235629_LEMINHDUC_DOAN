# main/Function/function_QuanLy/quanly_invoice_view_logic.py
# (Đã thêm chức năng show_invoice_details)

import tkinter as tk
from tkinter import ttk, messagebox

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
            # SỬA LỖI: Dùng %s
            query += " WHERE TenKhachHang LIKE %s OR SoDienThoai LIKE %s OR CAST(MaHoaDon AS VARCHAR(20)) = %s"
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

    def show_invoice_details(self):
        """Hiển thị chi tiết một hóa đơn (Sản phẩm và Phụ tùng)"""
        try:
            tree = self.view.invoice_tree
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn một hóa đơn để xem!")
                return
                
            item = tree.item(selected[0])
            invoice_id = item['values'][0]
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lấy thông tin hóa đơn: {e}")
            return
        
        dialog = tk.Toplevel(self.view.window)
        dialog.title(f"Chi tiết Hóa đơn #{invoice_id}")
        dialog.geometry("700x550")
        dialog.resizable(False, False)
        dialog.grab_set() 

        sp_frame = ttk.LabelFrame(dialog, text="Chi tiết Sản phẩm (Xe máy)", padding=(10, 10))
        sp_frame.pack(fill=tk.X, expand=True, padx=20, pady=10)
        
        cols_sp = ("Tên sản phẩm", "Số lượng", "Đơn giá", "Thành tiền")
        sp_tree = ttk.Treeview(sp_frame, columns=cols_sp, show="headings", height=5)
        for col in cols_sp: sp_tree.heading(col, text=col)
        sp_tree.column("Tên sản phẩm", width=300)
        sp_tree.pack(fill=tk.BOTH, expand=True)

        # SỬA LỖI: Dùng %s
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
                    p['TenSanPham'], p['SoLuong'], 
                    f"{p['DonGia']:,.0f}", f"{thanh_tien:,.0f}"
                ))

        pt_frame = ttk.LabelFrame(dialog, text="Chi tiết Phụ tùng & Dịch vụ", padding=(10, 10))
        pt_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        cols_pt = ("Tên phụ tùng", "Số lượng", "Đơn giá", "Thành tiền")
        pt_tree = ttk.Treeview(pt_frame, columns=cols_pt, show="headings", height=5)
        for col in cols_pt: pt_tree.heading(col, text=col)
        pt_tree.column("Tên phụ tùng", width=300)
        pt_tree.pack(fill=tk.BOTH, expand=True)

        # SỬA LỖI: Dùng %s
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
                    p['TenPhuTung'], p['SoLuong'], 
                    f"{p['DonGia']:,.0f}", f"{thanh_tien:,.0f}"
                ))

        tk.Button(
            dialog, 
            text="Đóng", 
            font=self.view.font_button, 
            bg="#dc3545", 
            fg="white", 
            command=dialog.destroy,
            relief="flat",
            padx=10,
            pady=5,
            cursor="hand2"
        ).pack(pady=10)