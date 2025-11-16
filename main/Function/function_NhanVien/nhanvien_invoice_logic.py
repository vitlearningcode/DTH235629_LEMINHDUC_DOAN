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

    def show_invoice_details(self, tree_to_use=None):
        """Hiển thị chi tiết một hóa đơn (Tái sử dụng cho Lịch sử và Công nợ)"""
        
        # Nếu không có cây nào được truyền vào, dùng cây lịch sử mặc định
        if tree_to_use is None:
            tree_to_use = self.view.invoice_tree
            
        selected = tree_to_use.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một hóa đơn để xem!")
            return
            
        item = tree_to_use.item(selected[0])
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
    
    def load_debt_list(self):
        """Tải danh sách hóa đơn CÒN NỢ (do nhân viên này lập)"""
        
        # Lấy từ khóa tìm kiếm từ UI (self.view.debt_search_entry)
        keyword = self.view.debt_search_entry.get().strip()

        for item in self.view.debt_tree.get_children():
            self.view.debt_tree.delete(item)
            
        query = """
            SELECT 
                hd.MaHoaDon,
                kh.HoTen as TenKhachHang,
                kh.SoDienThoai,
                FORMAT(hd.NgayLap, 'dd/MM/yyyy HH:mm') as NgayLap,
                hd.TongThanhToan,
                hd.TienDaTra,
                hd.TienConNo
            FROM HoaDon hd
            JOIN KhachHang kh ON hd.MaKhachHang = kh.MaKhachHang
            WHERE 
                hd.MaNguoiDung = %s
                AND hd.TrangThai = 'ConNo'
                AND hd.TienConNo > 0
        """
        params = [self.view.user_info['MaNguoiDung']]
        
        if keyword:
            query += " AND (kh.HoTen LIKE %s OR kh.SoDienThoai LIKE %s)"
            params.extend([f"%{keyword}%", f"%{keyword}%"])
            
        query += " ORDER BY hd.NgayLap ASC" # Ưu tiên nợ cũ
        
        try:
            invoices = self.db.fetch_all(query, params)
            
            if invoices:
                for inv in invoices:
                    self.view.debt_tree.insert("", tk.END, values=(
                        inv['MaHoaDon'],
                        inv['TenKhachHang'],
                        inv['SoDienThoai'],
                        inv['NgayLap'],
                        f"{inv['TongThanhToan']:,.0f}",
                        f"{inv['TienDaTra']:,.0f}",
                        f"{inv['TienConNo']:,.0f}"
                    ))
            else:
                self.view.debt_tree.insert("", tk.END, values=("", "Không tìm thấy khách hàng nợ.", "", "", "", "", ""))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách công nợ: {e}")

    # -------------------------------------------------------------------
    # CÁC HÀM MỚI CHO VIỆC XỬ LÝ CÔNG NỢ
    # -------------------------------------------------------------------

    def _set_debt_entry_state(self, state):
        """Helper: Bật/tắt các ô chi tiết công nợ"""
        for key, entry in self.view.debt_entries.items():
            entry.config(state=state)

    def clear_debt_details(self):
        """Làm mới (xóa) khung chi tiết thanh toán"""
        self._set_debt_entry_state('normal') # Mở khóa để xóa
        for key, entry in self.view.debt_entries.items():
            entry.delete(0, tk.END)
        self.view.debt_payment_entry.delete(0, tk.END)
        self._set_debt_entry_state('readonly') # Khóa lại
        
        # Xóa ID hóa đơn đang chọn
        if hasattr(self.view, 'current_debt_id'):
            self.view.current_debt_id = None
        if hasattr(self.view, 'current_remaining_debt'):
            self.view.current_remaining_debt = 0

    def on_debt_select(self, event):
        """Sự kiện double-click vào một hóa đơn nợ"""
        try:
            selected = self.view.debt_tree.selection()
            if not selected:
                return
            
            item = self.view.debt_tree.item(selected[0])
            values = item['values']
            if not values[0]: # Bỏ qua nếu là dòng "Không tìm thấy"
                return
            
            self.clear_debt_details() # Xóa cái cũ trước
            
            # Lấy dữ liệu từ cây
            ma_hd = values[0]
            khach_hang = values[1]
            tong_tien_str = values[4].replace(',', '')
            da_tra_str = values[5].replace(',', '')
            con_no_str = values[6].replace(',', '')
            
            # Lưu lại ID và số nợ hiện tại để xử lý thanh toán
            self.view.current_debt_id = ma_hd
            self.view.current_remaining_debt = float(con_no_str)
            
            # Điền dữ liệu vào các ô entry
            self._set_debt_entry_state('normal') # Mở khóa
            
            self.view.debt_entries["ma_hd"].insert(0, ma_hd)
            self.view.debt_entries["khach_hang"].insert(0, khach_hang)
            self.view.debt_entries["tong_tien"].insert(0, f"{float(tong_tien_str):,.0f} VNĐ")
            self.view.debt_entries["da_tra"].insert(0, f"{float(da_tra_str):,.0f} VNĐ")
            self.view.debt_entries["con_no"].insert(0, f"{float(con_no_str):,.0f} VNĐ")
            
            self._set_debt_entry_state('readonly') # Khóa lại
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải chi tiết: {e}")
            self.clear_debt_details()

    def process_debt_payment(self):
        """Xử lý thanh toán nợ"""
        
        # 1. Kiểm tra đã chọn hóa đơn chưa
        if not getattr(self.view, 'current_debt_id', None):
            messagebox.showwarning("Cảnh báo", "Vui lòng double-click vào một hóa đơn để chọn trước!")
            return

        # 2. Lấy số tiền nhập vào
        try:
            payment_str = self.view.debt_payment_entry.get().strip()
            if not payment_str:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập số tiền thanh toán!")
                return
            
            payment_amount = float(payment_str)
            remaining_debt = self.view.current_remaining_debt
            invoice_id = self.view.current_debt_id

            if payment_amount <= 0:
                messagebox.showwarning("Cảnh báo", "Số tiền trả phải lớn hơn 0.")
                return
            
            # 3. Kiểm tra số tiền nhập
            if payment_amount > remaining_debt:
                messagebox.showwarning("Cảnh báo", 
                                      f"Số tiền trả ({payment_amount:,.0f}) không được lớn hơn số nợ còn lại ({remaining_debt:,.0f})!")
                return
                
        except ValueError:
            messagebox.showerror("Lỗi", "Số tiền thanh toán không hợp lệ!")
            return

        try:
            # 4. Xử lý Logic (Đã sửa cho Computed Column 'TienConNo')
            if payment_amount == remaining_debt:
                # TRẢ HẾT NỢ
                if not messagebox.askyesno("Xác nhận", "Khách hàng trả đủ nợ. Xác nhận thanh toán và đóng nợ?"):
                    return
                
                # Sửa: Bỏ cập nhật TienConNo
                query = """
                    UPDATE HoaDon
                    SET 
                        TienDaTra = TienDaTra + %s,
                        TrangThai = 'DaThanhToan'
                    WHERE MaHoaDon = %s
                """
                params = (payment_amount, invoice_id)
                
            else:
                # TRẢ MỘT PHẦN NỢ (payment_amount < remaining_debt)
                if not messagebox.askyesno("Xác nhận", f"Khách hàng trả thêm {payment_amount:,.0f} VNĐ. Xác nhận?"):
                    return
                
                # Sửa: Bỏ cập nhật TienConNo, chỉ cập nhật TienDaTra
                query = """
                    UPDATE HoaDon
                    SET 
                        TienDaTra = TienDaTra + %s
                    WHERE MaHoaDon = %s
                """
                params = (payment_amount, invoice_id)

            # 5. Thực thi Query
            result = self.db.execute_query(query, params)
            
            if result:
                messagebox.showinfo("Thành công", "Cập nhật thanh toán công nợ thành công!")
                # 6. Tải lại danh sách nợ (đơn vừa trả sẽ biến mất hoặc được cập nhật)
                self.load_debt_list()
                # 7. Xóa khung chi tiết
                self.clear_debt_details()
            else:
                messagebox.showerror("Lỗi", "Không thể cập nhật CSDL. (0 dòng bị ảnh hưởng)")

        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Đã xảy ra lỗi khi cập nhật: {e}")