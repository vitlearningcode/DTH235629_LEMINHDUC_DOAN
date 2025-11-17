# main/Function/function_Admin/admin_invoice_logic.py

import tkinter as tk    
from tkinter import ttk, messagebox

class AdminInvoiceLogic:
    def __init__(self, view):
        self.view = view
        self.db = view.db

    def load_invoices(self, keyword=None):
        """Tải danh sách hóa đơn, hỗ trợ tìm kiếm theo Tên Khách Hàng hoặc Mã HĐ"""
        # Xóa dữ liệu cũ trên bảng
        for item in self.view.invoice_tree.get_children(): 
            self.view.invoice_tree.delete(item)
        
        # Câu truy vấn cơ bản
        query = """
            SELECT TOP 100 hd.MaHoaDon, kh.HoTen as KhachHang, nd.HoTen as NhanVien,
                   FORMAT(hd.NgayLap, 'dd/MM/yyyy HH:mm') as NgayLap,
                   hd.TongTien, hd.TongThanhToan, hd.TienConNo, hd.TrangThai
            FROM HoaDon hd
            JOIN KhachHang kh ON hd.MaKhachHang = kh.MaKhachHang
            JOIN NguoiDung nd ON hd.MaNguoiDung = nd.MaNguoiDung
        """
        
        params = []
        
        # Nếu có từ khóa tìm kiếm, thêm điều kiện WHERE
        if keyword:
            # Tìm theo Tên khách hàng HOẶC Mã hóa đơn
            query += " WHERE kh.HoTen LIKE %s OR CAST(hd.MaHoaDon AS VARCHAR(20)) LIKE %s"
            params.extend([f"%{keyword}%", f"%{keyword}%"])
            
        # --- SỬA LỖI 2: Sắp xếp từ nhỏ đến lớn (ASC thay vì DESC) ---
        query += " ORDER BY hd.MaHoaDon ASC" 
        
        invoices = self.db.fetch_all(query, params)
        
        if invoices:
            for inv in invoices:
                # --- SỬA LỖI 1: Chuyển đổi hiển thị trạng thái ---
                raw_status = inv['TrangThai']
                display_status = raw_status # Mặc định giữ nguyên nếu không khớp
                
                if raw_status == "DaThanhToan":
                    display_status = "Đã thanh toán"
                elif raw_status == "ConNo":
                    display_status = "Còn nợ"
                elif raw_status == "Huy": # Phòng trường hợp có trạng thái hủy
                    display_status = "Đã hủy"

                self.view.invoice_tree.insert("", tk.END, values=(
                    inv['MaHoaDon'], 
                    inv['KhachHang'], 
                    inv['NhanVien'], 
                    inv['NgayLap'],
                    f"{inv['TongTien']:,.0f}", 
                    f"{inv['TongThanhToan']:,.0f}",
                    f"{inv['TienConNo']:,.0f}", 
                    display_status  # <-- Dùng biến đã chuyển đổi text tiếng Việt
                ))
                
    
    def delete_invoice(self):
        """Xóa hóa đơn được chọn và các dữ liệu liên quan"""
        selected = self.view.invoice_tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một hóa đơn để xóa.")
            return

        item = self.view.invoice_tree.item(selected[0])
        invoice_id = item['values'][0]
        customer_name = item['values'][1]

        # Hộp thoại xác nhận
        confirm = messagebox.askyesno(
            "Xác nhận xóa", 
            f"Bạn có chắc muốn XÓA VĨNH VIỄN hóa đơn #{invoice_id} của khách hàng '{customer_name}'?\n\n"
            "CẢNH BÁO: Hành động này sẽ xóa cả chi tiết hóa đơn và phiếu bảo hành liên quan."
        )
        
        if confirm:
            try:
                # 1. Xóa chi tiết sản phẩm liên quan
                self.db.execute_query("DELETE FROM ChiTietHoaDonSanPham WHERE MaHoaDon = %s", (invoice_id,))
                
                # 2. Xóa chi tiết phụ tùng liên quan
                self.db.execute_query("DELETE FROM ChiTietHoaDonPhuTung WHERE MaHoaDon = %s", (invoice_id,))
                
                # 3. Xóa phiếu bảo hành liên quan (nếu có)
                self.db.execute_query("DELETE FROM PhieuBaoHanh WHERE MaHoaDon = %s", (invoice_id,))
                
                # 4. Xóa hóa đơn chính
                result = self.db.execute_query("DELETE FROM HoaDon WHERE MaHoaDon = %s", (invoice_id,))
                
                if result:
                    messagebox.showinfo("Thành công", f"Đã xóa hóa đơn #{invoice_id}.")
                    self.load_invoices() # Tải lại danh sách
                else:
                    messagebox.showerror("Lỗi", "Không thể xóa hóa đơn.")
                    
            except Exception as e:
                messagebox.showerror("Lỗi CSDL", f"Đã xảy ra lỗi khi xóa: {e}")

    def show_invoice_details(self):
        """Hiển thị chi tiết một hóa đơn (Sản phẩm và Phụ tùng)"""
        try:
            tree = self.view.invoice_tree # Lấy tree từ self.view (Admin)
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn một hóa đơn để xem!")
                return
                
            item = tree.item(selected[0])
            invoice_id = item['values'][0]
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lấy thông tin hóa đơn: {e}")
            return
        
        # Tạo cửa sổ pop-up
        dialog = tk.Toplevel(self.view.window)
        dialog.title(f"Chi tiết Hóa đơn #{invoice_id}")
        dialog.geometry("700x550")
        dialog.resizable(False, False)
        dialog.grab_set() # Giữ focus

        # --- 1. Hiển thị Sản phẩm (Xe máy) ---
        sp_frame = ttk.LabelFrame(dialog, text="Chi tiết Sản phẩm (Xe máy)", padding=(10, 10))
        sp_frame.pack(fill=tk.X, expand=True, padx=20, pady=10)
        
        cols_sp = ("Tên sản phẩm", "Số lượng", "Đơn giá", "Thành tiền")
        sp_tree = ttk.Treeview(sp_frame, columns=cols_sp, show="headings", height=5)
        for col in cols_sp: sp_tree.heading(col, text=col)
        sp_tree.column("Tên sản phẩm", width=300)
        sp_tree.pack(fill=tk.BOTH, expand=True)

        query_sp = """
            SELECT sp.TenSanPham, cthd.SoLuong, cthd.DonGia
            FROM ChiTietHoaDonSanPham cthd
            JOIN SanPham sp ON cthd.MaSanPham = sp.MaSanPham
            WHERE cthd.MaHoaDon = ?
        """
        # Lưu ý: Sử dụng %s nếu dùng thư viện pyodbc/pymssql hoặc ? nếu dùng sqlite/odbc chuẩn
        # Code gốc của bạn dùng %s ở trên, nhưng dùng ? ở dưới. Tôi giữ nguyên logic gốc của bạn ở đoạn này.
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

        # --- 2. Hiển thị Phụ tùng ---
        pt_frame = ttk.LabelFrame(dialog, text="Chi tiết Phụ tùng & Dịch vụ", padding=(10, 10))
        pt_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        cols_pt = ("Tên phụ tùng", "Số lượng", "Đơn giá", "Thành tiền")
        pt_tree = ttk.Treeview(pt_frame, columns=cols_pt, show="headings", height=5)
        for col in cols_pt: pt_tree.heading(col, text=col)
        pt_tree.column("Tên phụ tùng", width=300)
        pt_tree.pack(fill=tk.BOTH, expand=True)

        query_pt = """
            SELECT pt.TenPhuTung, cthd.SoLuong, cthd.DonGia
            FROM ChiTietHoaDonPhuTung cthd
            JOIN PhuTung pt ON cthd.MaPhuTung = pt.MaPhuTung
            WHERE cthd.MaHoaDon = ?
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

        # --- 3. Nút Đóng ---
        tk.Button(
            dialog, 
            text="Đóng", 
            font=("Arial", 11, "bold"), 
            bg="#dc3545", 
            fg="white", 
            command=dialog.destroy,
            relief="flat",
            padx=10,
            pady=5,
            cursor="hand2"
        ).pack(pady=10)