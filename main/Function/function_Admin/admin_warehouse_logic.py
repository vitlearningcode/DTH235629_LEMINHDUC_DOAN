import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
#------------------------------------------------------------
# MÔ TẢ: Logic cho Quản lý Kho (Admin)
# FILE NÀY ĐÃ ĐƯỢC VIỆT HÓA TRẠNG THÁI HIỂN THỊ
#------------------------------------------------------------

class AdminWarehouseLogic:
    def __init__(self, view):
        """
        Khởi tạo logic cho Quản lý Kho.
        :param view: Thể hiện của lớp Admin (admin_window.py)
        """
        self.view = view
        self.db = view.db # Lấy kết nối CSDL từ view

    def load_phieu_nhap(self):
        """Tải danh sách các phiếu nhập kho lên Treeview"""
        
        # Truy cập Treeview từ file UI (self.view.phieu_nhap_tree)
        for item in self.view.phieu_nhap_tree.get_children():
            self.view.phieu_nhap_tree.delete(item)
        
        # Câu query này JOIN 3 bảng để lấy tên thay vì chỉ ID
        query = """
            SELECT 
                p.MaPhieuNhap, 
                n.TenNhaCungCap, 
                u.HoTen AS NguoiNhap,
                FORMAT(p.NgayNhap, 'dd/MM/yyyy HH:mm') as NgayNhap,
                p.TongTien,
                p.TrangThai
            FROM PhieuNhapKho p
            LEFT JOIN NhaCungCap n ON p.MaNhaCungCap = n.MaNhaCungCap
            LEFT JOIN NguoiDung u ON p.MaNguoiDung = u.MaNguoiDung
            ORDER BY p.MaPhieuNhap ASC
        """
        phieu_nhap_list = self.db.fetch_all(query)
        
        if phieu_nhap_list:
            for pn in phieu_nhap_list:
                # --- XỬ LÝ HIỂN THỊ TRẠNG THÁI TIẾNG VIỆT ---
                raw_status = pn['TrangThai']
                display_status = raw_status # Mặc định
                
                if raw_status == 'DaXacNhan':
                    display_status = "Đã xác nhận"
                elif raw_status == 'ChoXacNhan':
                    display_status = "Chờ xử lý" # Theo yêu cầu của bạn
                elif raw_status == 'Huy':
                    display_status = "Đã hủy"

                # Chèn dữ liệu vào Treeview
                self.view.phieu_nhap_tree.insert("", tk.END, values=(
                    pn['MaPhieuNhap'],
                    pn['TenNhaCungCap'] or "N/A", 
                    pn['NguoiNhap'],
                    pn['NgayNhap'],
                    f"{pn['TongTien']:,.0f}", 
                    display_status  # <-- Hiển thị tiếng Việt
                ))

    def add_phieu_nhap(self):
        """Mở cửa sổ popup để tạo phiếu nhập kho mới (chỉ tạo Header)"""
        
        dialog = tk.Toplevel(self.view.window)
        dialog.title("Tạo Phiếu Nhập Kho")
        dialog.geometry("400x250")
        dialog.resizable(False, False)
        
        tk.Label(dialog, text="Chọn Nhà Cung Cấp:", font=("Arial", 11)).pack(pady=10)
        
        # Tải danh sách nhà cung cấp để đưa vào Combobox
        try:
            suppliers = self.db.fetch_all("SELECT MaNhaCungCap, TenNhaCungCap FROM NhaCungCap WHERE TrangThai = 'HoatDong'")
            supplier_names = [s['TenNhaCungCap'] for s in suppliers]
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách nhà cung cấp: {e}")
            dialog.destroy()
            return

        if not suppliers:
            messagebox.showwarning("Cảnh báo", "Không có nhà cung cấp nào đang 'HoatDong'.\nVui lòng thêm nhà cung cấp trước.")
            dialog.destroy()
            return

        supplier_var = tk.StringVar()
        supplier_combo = ttk.Combobox(dialog, textvariable=supplier_var, values=supplier_names, state="readonly", width=40)
        supplier_combo.pack(pady=5, padx=20)
        supplier_combo.current(0) 

        tk.Label(dialog, text="Ghi chú (nếu có):", font=("Arial", 11)).pack(pady=10)
        ghi_chu_entry = tk.Entry(dialog, font=("Arial", 11), width=42)
        ghi_chu_entry.pack(pady=5, padx=20)

        def save_phieu_nhap():
            selected_name = supplier_var.get()
            selected_supplier_id = None
            
            for s in suppliers:
                if s['TenNhaCungCap'] == selected_name:
                    selected_supplier_id = s['MaNhaCungCap']
                    break
            
            if not selected_supplier_id:
                messagebox.showwarning("Lỗi", "Vui lòng chọn nhà cung cấp hợp lệ.")
                return
            
            ghi_chu = ghi_chu_entry.get().strip()
            admin_id = self.view.user_info['MaNguoiDung'] 

            # Lưu ý: Trong CSDL vẫn lưu là 'ChoXacNhan' (tiếng Anh) để chuẩn hóa
            query = """
                INSERT INTO PhieuNhapKho (MaNhaCungCap, MaNguoiDung, TrangThai, GhiChu)
                VALUES (%s, %s, 'ChoXacNhan', %s)
            """
            
            ma_phieu_nhap = self.db.execute_query(query, (selected_supplier_id, admin_id, ghi_chu))
            
            if ma_phieu_nhap:
                self.load_phieu_nhap()
                dialog.destroy()
                messagebox.showinfo("Thành công", f"Đã tạo Phiếu nhập kho #{ma_phieu_nhap}.\nVui lòng thêm chi tiết sản phẩm/phụ tùng.")
                self._show_detail_window(ma_phieu_nhap, is_view_only=False)
            else:
                messagebox.showerror("Lỗi", "Không thể tạo phiếu nhập kho.")

        tk.Button(dialog, text="💾 Tạo Phiếu Nhập", command=save_phieu_nhap, 
                  font=("Arial", 11, "bold"), bg="#28a745", fg="white").pack(pady=20)

    def view_chi_tiet(self):
        """Mở cửa sổ Xem Chi Tiết Phiếu Nhập"""
        selected = self.view.phieu_nhap_tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một phiếu nhập.")
            return
        
        item = self.view.phieu_nhap_tree.item(selected[0])
        pn_id = item['values'][0]

        self._show_detail_window(pn_id, is_view_only=True)

    def _show_detail_window(self, pn_id, is_view_only=False):
        """Hàm nội bộ: Hiển thị cửa sổ chi tiết"""
        
        dialog = tk.Toplevel(self.view.window)
        dialog.title(f"Chi tiết Phiếu Nhập #{pn_id}")
        dialog.geometry("900x600" if not is_view_only else "500x600")
        
        # --- Input Frame ---
        input_frame = tk.Frame(dialog, width=400, bd=2, relief=tk.RIDGE)

        tk.Label(input_frame, text="THÊM HÀNG VÀO PHIẾU", font=("Arial", 14, "bold")).pack(pady=10)

        tab_control = ttk.Notebook(input_frame)
        tab_products = ttk.Frame(tab_control)
        tab_parts = ttk.Frame(tab_control)
        tab_control.add(tab_products, text='   🏍️ Sản Phẩm (Xe)   ')
        tab_control.add(tab_parts, text='   🔧 Phụ Tùng   ')
        tab_control.pack(fill=tk.BOTH, expand=True, pady=5, padx=5)

        cols_sp = ("Mã SP", "Tên Sản Phẩm", "Hãng")
        tree_sp = ttk.Treeview(tab_products, columns=cols_sp, show="headings", height=15)
        for col in cols_sp: tree_sp.heading(col, text=col)
        tree_sp.column("Mã SP", width=50)
        tree_sp.column("Tên Sản Phẩm", width=200)
        tree_sp.pack(fill=tk.BOTH, expand=True)

        cols_pt = ("Mã PT", "Tên Phụ Tùng", "Loại")
        tree_pt = ttk.Treeview(tab_parts, columns=cols_pt, show="headings", height=15)
        for col in cols_pt: tree_pt.heading(col, text=col)
        tree_pt.column("Mã PT", width=50)
        tree_pt.column("Tên Phụ Tùng", width=200)
        tree_pt.pack(fill=tk.BOTH, expand=True)
        
        entry_frame = tk.Frame(input_frame)
        entry_frame.pack(pady=10)

        tk.Label(entry_frame, text="Số Lượng:", font=("Arial", 11)).grid(row=0, column=0, padx=5, pady=5)
        dialog.entry_so_luong = tk.Entry(entry_frame, font=("Arial", 11), width=15)
        dialog.entry_so_luong.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(entry_frame, text="Đơn Giá Nhập:", font=("Arial", 11)).grid(row=1, column=0, padx=5, pady=5)
        dialog.entry_don_gia = tk.Entry(entry_frame, font=("Arial", 11), width=15)
        dialog.entry_don_gia.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(input_frame, text="➕ Thêm vào Phiếu Nhập", font=("Arial", 11, "bold"), 
                  bg="#007bff", fg="white", 
                  command=lambda: self._add_item_to_phieu(dialog, pn_id, tab_control, tree_sp, tree_pt)).pack(pady=10)

        self._load_all_products(tree_sp)
        self._load_all_parts(tree_pt)
        
        # --- Display Frame ---
        display_frame = tk.Frame(dialog)
        
        if is_view_only:
            display_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        else:
            input_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
            display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(display_frame, text="CHI TIẾT ĐÃ NHẬP", font=("Arial", 14, "bold")).pack(pady=10)

        sp_detail_frame = tk.LabelFrame(display_frame, text="Sản phẩm (Xe) đã nhập", font=("Arial", 11), padx=5, pady=5)
        sp_detail_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        cols_sp_detail = ("MaChiTiet", "Tên Sản Phẩm", "Số Lượng", "Đơn Giá", "Thành Tiền")
        dialog.tree_sp_detail = ttk.Treeview(sp_detail_frame, columns=cols_sp_detail, show="headings", height=8)
        for col in cols_sp_detail: dialog.tree_sp_detail.heading(col, text=col)
        dialog.tree_sp_detail.column("MaChiTiet", width=0, stretch=tk.NO) 
        dialog.tree_sp_detail.pack(fill=tk.BOTH, expand=True)

        pt_detail_frame = tk.LabelFrame(display_frame, text="Phụ tùng đã nhập", font=("Arial", 11), padx=5, pady=5)
        pt_detail_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        cols_pt_detail = ("MaChiTiet", "Tên Phụ Tùng", "Số Lượng", "Đơn Giá", "Thành Tiền")
        dialog.tree_pt_detail = ttk.Treeview(pt_detail_frame, columns=cols_pt_detail, show="headings", height=8)
        for col in cols_pt_detail: dialog.tree_pt_detail.heading(col, text=col)
        dialog.tree_pt_detail.column("MaChiTiet", width=0, stretch=tk.NO)
        dialog.tree_pt_detail.pack(fill=tk.BOTH, expand=True)

        if not is_view_only:
            tk.Button(display_frame, text="🗑️ Xóa mục đã chọn", font=("Arial", 11, "bold"), 
                      bg="#dc3545", fg="white", 
                      command=lambda: self._delete_item_from_phieu(dialog, pn_id)).pack(pady=10)
        
        if is_view_only:
            tk.Button(display_frame, text="Đóng", font=("Arial", 11, "bold"), 
                      bg="#6c757d", fg="white", 
                      command=dialog.destroy).pack(pady=10)

        self._load_existing_details(dialog, pn_id)

    def _load_existing_details(self, dialog, pn_id):
        for item in dialog.tree_sp_detail.get_children(): dialog.tree_sp_detail.delete(item)
        for item in dialog.tree_pt_detail.get_children(): dialog.tree_pt_detail.delete(item)
        try:
            query_sp = """
                SELECT ct.MaChiTiet, sp.TenSanPham, ct.SoLuong, ct.DonGia, (ct.SoLuong * ct.DonGia) AS ThanhTien
                FROM ChiTietPhieuNhapSanPham ct JOIN SanPham sp ON ct.MaSanPham = sp.MaSanPham WHERE ct.MaPhieuNhap = %s
            """
            products = self.db.fetch_all(query_sp, (pn_id,))
            if products:
                for p in products:
                    dialog.tree_sp_detail.insert("", tk.END, values=(p['MaChiTiet'], p['TenSanPham'], p['SoLuong'], f"{p['DonGia']:,.0f}", f"{p['ThanhTien']:,.0f}"))
            
            query_pt = """
                SELECT ct.MaChiTiet, pt.TenPhuTung, ct.SoLuong, ct.DonGia, (ct.SoLuong * ct.DonGia) AS ThanhTien
                FROM ChiTietPhieuNhapPhuTung ct JOIN PhuTung pt ON ct.MaPhuTung = pt.MaPhuTung WHERE ct.MaPhieuNhap = %s
            """
            parts = self.db.fetch_all(query_pt, (pn_id,))
            if parts:
                for p in parts:
                    dialog.tree_pt_detail.insert("", tk.END, values=(p['MaChiTiet'], p['TenPhuTung'], p['SoLuong'], f"{p['DonGia']:,.0f}", f"{p['ThanhTien']:,.0f}"))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải chi tiết phiếu nhập: {e}", parent=dialog)

    def _delete_item_from_phieu(self, dialog, pn_id):
        ma_chi_tiet = None
        table_name = None
        item_name = None
        
        selected_sp = dialog.tree_sp_detail.selection()
        if selected_sp:
            item = dialog.tree_sp_detail.item(selected_sp[0])
            ma_chi_tiet = item['values'][0]; item_name = item['values'][1]; table_name = "ChiTietPhieuNhapSanPham"
        else:
            selected_pt = dialog.tree_pt_detail.selection()
            if selected_pt:
                item = dialog.tree_pt_detail.item(selected_pt[0])
                ma_chi_tiet = item['values'][0]; item_name = item['values'][1]; table_name = "ChiTietPhieuNhapPhuTung"
        
        if not ma_chi_tiet:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một mục ở bảng bên phải để xóa.", parent=dialog)
            return

        if messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc muốn xóa '{item_name}'?", parent=dialog):
            try:
                self.db.execute_query(f"DELETE FROM {table_name} WHERE MaChiTiet = %s", (ma_chi_tiet,))
                update_query = """
                    UPDATE PhieuNhapKho SET TongTien = (
                        SELECT ISNULL(SUM(ThanhTien), 0) FROM ChiTietPhieuNhapSanPham WHERE MaPhieuNhap = %s
                    ) + (
                        SELECT ISNULL(SUM(ThanhTien), 0) FROM ChiTietPhieuNhapPhuTung WHERE MaPhieuNhap = %s
                    ) WHERE MaPhieuNhap = %s
                """
                self.db.execute_query(update_query, (pn_id, pn_id, pn_id))
                messagebox.showinfo("Thành công", f"Đã xóa '{item_name}'.", parent=dialog)
                self._load_existing_details(dialog, pn_id)
                self.load_phieu_nhap() 
            except Exception as e:
                messagebox.showerror("Lỗi CSDL", f"Không thể xóa: {e}", parent=dialog)

    def _load_all_products(self, tree_sp):
        for item in tree_sp.get_children(): tree_sp.delete(item)
        products = self.db.fetch_all("SELECT sp.MaSanPham, sp.TenSanPham, hx.TenHangXe FROM SanPham sp LEFT JOIN HangXe hx ON sp.MaHangXe = hx.MaHangXe ORDER BY sp.TenSanPham")
        if products:
            for p in products: tree_sp.insert("", tk.END, values=(p['MaSanPham'], p['TenSanPham'], p['TenHangXe'] or "N/A"))

    def _load_all_parts(self, tree_pt):
        for item in tree_pt.get_children(): tree_pt.delete(item)
        parts = self.db.fetch_all("SELECT pt.MaPhuTung, pt.TenPhuTung, lpt.TenLoaiPhuTung FROM PhuTung pt LEFT JOIN LoaiPhuTung lpt ON pt.MaLoaiPhuTung = lpt.MaLoaiPhuTung ORDER BY pt.TenPhuTung")
        if parts:
            for p in parts: tree_pt.insert("", tk.END, values=(p['MaPhuTung'], p['TenPhuTung'], p['TenLoaiPhuTung'] or "N/A"))

    def _add_item_to_phieu(self, dialog, pn_id, tab_control, tree_sp, tree_pt):
        try:
            current_tab = tab_control.index(tab_control.select())
            if current_tab == 0:
                selected = tree_sp.selection()
                if not selected: return messagebox.showwarning("Cảnh báo", "Vui lòng chọn SẢN PHẨM!", parent=dialog)
                item_id = tree_sp.item(selected[0])['values'][0]; item_name = tree_sp.item(selected[0])['values'][1]
                table_name = "ChiTietPhieuNhapSanPham"; id_col = "MaSanPham"
            elif current_tab == 1:
                selected = tree_pt.selection()
                if not selected: return messagebox.showwarning("Cảnh báo", "Vui lòng chọn PHỤ TÙNG!", parent=dialog)
                item_id = tree_pt.item(selected[0])['values'][0]; item_name = tree_pt.item(selected[0])['values'][1]
                table_name = "ChiTietPhieuNhapPhuTung"; id_col = "MaPhuTung"
            
            so_luong = int(dialog.entry_so_luong.get().strip())
            don_gia = float(dialog.entry_don_gia.get().strip())
            if so_luong <= 0 or don_gia < 0: return messagebox.showerror("Lỗi", "Số lượng > 0 và Đơn giá >= 0", parent=dialog)

            query = f"INSERT INTO {table_name} (MaPhieuNhap, {id_col}, SoLuong, DonGia) VALUES (%s, %s, %s, %s)"
            if self.db.execute_query(query, (pn_id, item_id, so_luong, don_gia)):
                messagebox.showinfo("Thành công", f"Đã thêm {so_luong} x {item_name}", parent=dialog)
                self.load_phieu_nhap()
                self._load_existing_details(dialog, pn_id)
                dialog.entry_so_luong.delete(0, tk.END); dialog.entry_don_gia.delete(0, tk.END)
            else:
                messagebox.showerror("Lỗi", "Thất bại.", parent=dialog)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi: {e}", parent=dialog)

    # --- CÁC HÀM XỬ LÝ LOGIC VỚI TRẠNG THÁI TIẾNG VIỆT ---

    def confirm_phieu_nhap(self):
        """Xác nhận phiếu: Cập nhật trạng thái VÀ CỘNG HÀNG VÀO KHO."""
        selected = self.view.phieu_nhap_tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn phiếu nhập để xác nhận.")
            return

        item = self.view.phieu_nhap_tree.item(selected[0])
        pn_id = item['values'][0]
        trang_thai_text = item['values'][5] # Lấy chữ tiếng Việt

        # --- SỬA ĐIỀU KIỆN CHECK SANG TIẾNG VIỆT ---
        if trang_thai_text != 'Chờ xử lý':
            messagebox.showerror("Lỗi", f"Chỉ có thể xác nhận phiếu đang 'Chờ xử lý'.\nTrạng thái hiện tại: '{trang_thai_text}'.")
            return
        
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xác nhận Phiếu Nhập #{pn_id}?\nHÀNG HÓA SẼ ĐƯỢC CỘNG VÀO KHO."):
            try:
                # Logic cộng kho giữ nguyên
                query_sp = "SELECT MaSanPham, SoLuong FROM ChiTietPhieuNhapSanPham WHERE MaPhieuNhap = %s"
                items_sp = self.db.fetch_all(query_sp, (pn_id,))
                if items_sp:
                    for item_sp in items_sp:
                        self.db.execute_query("UPDATE SanPham SET SoLuongTon = SoLuongTon + %s WHERE MaSanPham = %s", (item_sp['SoLuong'], item_sp['MaSanPham']))

                query_pt = "SELECT MaPhuTung, SoLuong FROM ChiTietPhieuNhapPhuTung WHERE MaPhieuNhap = %s"
                items_pt = self.db.fetch_all(query_pt, (pn_id,))
                if items_pt:
                    for item_pt in items_pt:
                        self.db.execute_query("UPDATE PhuTung SET SoLuongTon = SoLuongTon + %s WHERE MaPhuTung = %s", (item_pt['SoLuong'], item_pt['MaPhuTung']))

                # Cập nhật trạng thái trong DB thành 'DaXacNhan' (Tiếng Anh)
                query = "UPDATE PhieuNhapKho SET TrangThai = 'DaXacNhan' WHERE MaPhieuNhap = %s"
                result = self.db.execute_query(query, (pn_id,))
                
                if result:
                    messagebox.showinfo("Thành công", f"Đã xác nhận Phiếu Nhập #{pn_id}.")
                    self.load_phieu_nhap() 
                else:
                    messagebox.showerror("Lỗi", "Lỗi cập nhật trạng thái.")
            except Exception as e:
                messagebox.showerror("Lỗi CSDL", f"Lỗi: {e}")

    def cancel_phieu_nhap(self):
        """Hủy phiếu: Chỉ đổi trạng thái."""
        selected = self.view.phieu_nhap_tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn phiếu nhập để hủy.")
            return

        item = self.view.phieu_nhap_tree.item(selected[0])
        pn_id = item['values'][0]
        trang_thai_text = item['values'][5]

        # --- SỬA ĐIỀU KIỆN CHECK SANG TIẾNG VIỆT ---
        if trang_thai_text != 'Chờ xử lý':
            messagebox.showerror("Lỗi", f"Chỉ có thể hủy phiếu đang 'Chờ xử lý'.\nTrạng thái hiện tại: '{trang_thai_text}'.")
            return
        
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn HỦY Phiếu Nhập #{pn_id}?"):
            try:
                query = "UPDATE PhieuNhapKho SET TrangThai = 'Huy' WHERE MaPhieuNhap = %s"
                result = self.db.execute_query(query, (pn_id,))
                
                if result:
                    messagebox.showinfo("Thành công", f"Đã hủy Phiếu Nhập #{pn_id}.")
                    self.load_phieu_nhap() 
                else:
                    messagebox.showerror("Lỗi", "Không thể cập nhật trạng thái.")
            except Exception as e:
                messagebox.showerror("Lỗi CSDL", f"Lỗi: {e}")

    def delete_phieu_nhap(self):
        """Xóa phiếu nhập VĨNH VIỄN."""
        selected = self.view.phieu_nhap_tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn phiếu nhập để xóa.")
            return

        item = self.view.phieu_nhap_tree.item(selected[0])
        pn_id = item['values'][0]
        trang_thai_text = item['values'][5]

        # --- SỬA CẢNH BÁO DỰA TRÊN TIẾNG VIỆT ---
        confirm_message = ""
        if trang_thai_text == 'Đã xác nhận':
            confirm_message = (
                f"Bạn có chắc muốn XÓA VĨNH VIỄN Phiếu Nhập #{pn_id}?\n\n"
                f"CẢNH BÁO: Phiếu này đã '{trang_thai_text}'.\n"
                f"Việc xóa sẽ KHÔNG HOÀN TÁC KHO.\n"
                f"==> Dữ liệu kho có thể bị SAI LỆCH."
            )
        else: 
            confirm_message = f"Bạn có chắc muốn XÓA VĨNH VIỄN Phiếu Nhập #{pn_id}?"

        if not messagebox.askyesno("Xác nhận xóa", confirm_message, icon='warning'):
            return

        try:
            self.db.execute_query("DELETE FROM ChiTietPhieuNhapSanPham WHERE MaPhieuNhap = %s", (pn_id,))
            self.db.execute_query("DELETE FROM ChiTietPhieuNhapPhuTung WHERE MaPhieuNhap = %s", (pn_id,))
            result = self.db.execute_query("DELETE FROM PhieuNhapKho WHERE MaPhieuNhap = %s", (pn_id,))
            
            if result:
                messagebox.showinfo("Thành công", f"Đã xóa Phiếu Nhập #{pn_id}.")
                self.load_phieu_nhap() 
            else:
                messagebox.showerror("Lỗi", "Không thể xóa phiếu nhập chính.")
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Lỗi: {e}")