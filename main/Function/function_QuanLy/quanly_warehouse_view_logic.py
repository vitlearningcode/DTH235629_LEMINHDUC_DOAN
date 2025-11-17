# main/Function/function_QuanLy/quanly_warehouse_view_logic.py
# (Đã thêm chức năng show_warehouse_details và Việt hóa trạng thái)

import tkinter as tk
from tkinter import ttk, messagebox

class QuanLyWarehouseViewLogic:
    def __init__(self, view):
        self.view = view
        self.db = view.db
        
        # Ánh xạ Trạng thái Phiếu nhập sang Tiếng Việt
        self.status_map = {
            'ChoXacNhan   ': 'Chờ xác nhận',
            'DaXacNhan': 'Đã xác nhận',
            'Huy': 'Đã hủy',
            # Thêm các trạng thái khác nếu có
        }

    def load_view(self, tree, keyword=None):
        """Tải dữ liệu Xem kho (Phiếu nhập), """
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
            query += " WHERE n.TenNhaCungCap LIKE %s OR CAST(p.MaPhieuNhap AS VARCHAR(20)) = %s"
            params.extend([f"%{keyword}%", keyword])

        query += " ORDER BY p.MaPhieuNhap DESC"
        
        records = self.db.fetch_all(query, params)
        
        if records:
            for rec in records:
                # Ánh xạ trạng thái
                display_status = self.status_map.get(rec['TrangThai'], rec['TrangThai'])
                
                tree.insert("", tk.END, values=(
                    rec['MaPhieuNhap'], rec['TenNhaCungCap'] or "N/A", rec['NguoiNhap'] or "N/A",
                    rec['NgayNhap'], f"{rec['TongTien']:,.0f} VNĐ", display_status
                ))

    def show_warehouse_details(self):
        """Hiển thị chi tiết một Phiếu Nhập Kho (Sản phẩm và Phụ tùng)"""
        try:
            tree = self.view.warehouse_tree
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn một phiếu kho để xem!")
                return
                
            item = tree.item(selected[0])
            phieu_id = item['values'][0]
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lấy thông tin phiếu kho: {e}")
            return
        
        dialog = tk.Toplevel(self.view.window)
        dialog.title(f"Chi tiết Phiếu Nhập #{phieu_id}")
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

        query_sp = """
            SELECT sp.TenSanPham, ctpn.SoLuong, ctpn.DonGia
            FROM ChiTietPhieuNhapSanPham ctpn
            JOIN SanPham sp ON ctpn.MaSanPham = sp.MaSanPham
            WHERE ctpn.MaPhieuNhap = %s
        """
        products = self.db.fetch_all(query_sp, (phieu_id,))
        if products:
            for p in products:
                thanh_tien = p['SoLuong'] * p['DonGia']
                sp_tree.insert("", tk.END, values=(
                    p['TenSanPham'], p['SoLuong'], 
                    f"{p['DonGia']:,.0f}", f"{thanh_tien:,.0f}"
                ))

        pt_frame = ttk.LabelFrame(dialog, text="Chi tiết Phụ tùng", padding=(10, 10))
        pt_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        cols_pt = ("Tên phụ tùng", "Số lượng", "Đơn giá", "Thành tiền")
        pt_tree = ttk.Treeview(pt_frame, columns=cols_pt, show="headings", height=5)
        for col in cols_pt: pt_tree.heading(col, text=col)
        pt_tree.column("Tên phụ tùng", width=300)
        pt_tree.pack(fill=tk.BOTH, expand=True)

        query_pt = """
            SELECT pt.TenPhuTung, ctpn.SoLuong, ctpn.DonGia
            FROM ChiTietPhieuNhapPhuTung ctpn
            JOIN PhuTung pt ON ctpn.MaPhuTung = pt.MaPhuTung
            WHERE ctpn.MaPhieuNhap = %s
        """
        parts = self.db.fetch_all(query_pt, (phieu_id,))
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