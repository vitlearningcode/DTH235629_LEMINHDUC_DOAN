import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
#------------------------------------------------------------
# MÔ TẢ: Logic cho Quản lý Kho (Admin)
# FILE NÀY ĐÃ ĐƯỢC SỬA LỖI THỤT LỀ VÀ LỖI TRÙNG HÀM
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
            ORDER BY p.MaPhieuNhap DESC
        """
        phieu_nhap_list = self.db.fetch_all(query)
        
        if phieu_nhap_list:
            for pn in phieu_nhap_list:
                # Chèn dữ liệu vào Treeview
                self.view.phieu_nhap_tree.insert("", tk.END, values=(
                    pn['MaPhieuNhap'],
                    pn['TenNhaCungCap'] or "N/A", # Hiển thị N/A nếu NCC đã bị xóa
                    pn['NguoiNhap'],
                    pn['NgayNhap'],
                    f"{pn['TongTien']:,.0f}", # Format tiền
                    pn['TrangThai']
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
        supplier_combo.current(0) # Chọn mặc định là nhà cung cấp đầu tiên

        tk.Label(dialog, text="Ghi chú (nếu có):", font=("Arial", 11)).pack(pady=10)
        ghi_chu_entry = tk.Entry(dialog, font=("Arial", 11), width=42)
        ghi_chu_entry.pack(pady=5, padx=20)

        def save_phieu_nhap():
            selected_name = supplier_var.get()
            selected_supplier_id = None
            
            # Tìm ID dựa trên tên đã chọn
            for s in suppliers:
                if s['TenNhaCungCap'] == selected_name:
                    selected_supplier_id = s['MaNhaCungCap']
                    break
            
            if not selected_supplier_id:
                messagebox.showwarning("Lỗi", "Vui lòng chọn nhà cung cấp hợp lệ.")
                return
            
            ghi_chu = ghi_chu_entry.get().strip()
            admin_id = self.view.user_info['MaNguoiDung'] # Lấy ID admin đang đăng nhập

            query = """
                INSERT INTO PhieuNhapKho (MaNhaCungCap, MaNguoiDung, TrangThai, GhiChu)
                VALUES (%s, %s, 'ChoXacNhan', %s)
            """
            
            # Thực thi query
            ma_phieu_nhap = self.db.execute_query(query, (selected_supplier_id, admin_id, ghi_chu))
            
            if ma_phieu_nhap:
                # 1. Tải lại danh sách phiếu nhập
                self.load_phieu_nhap()
                # 2. Đóng cửa sổ tạo header
                dialog.destroy()
                # 3. Mở ngay cửa sổ chi tiết ở chế độ Thêm/Sửa
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

        # Mở cửa sổ chi tiết ở chế độ CHỈ XEM
        self._show_detail_window(pn_id, is_view_only=True)

    def _show_detail_window(self, pn_id, is_view_only=False):
        """Hàm nội bộ: Hiển thị cửa sổ chi tiết"""
        
        dialog = tk.Toplevel(self.view.window)
        dialog.title(f"Chi tiết Phiếu Nhập #{pn_id}")
        dialog.geometry("900x600" if not is_view_only else "500x600")
        
        # --- 2. Tạo Frame Input (Bên trái) ---
        input_frame = tk.Frame(dialog, width=400, bd=2, relief=tk.RIDGE)
        # (Sẽ pack ở dưới)

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

        # Tải dữ liệu cho cây bên trái
        self._load_all_products(tree_sp)
        self._load_all_parts(tree_pt)
        
        # --- 3. Tạo Frame Hiển thị (Bên phải) - LUÔN HIỂN THỊ ---
        display_frame = tk.Frame(dialog)
        
        if is_view_only:
            display_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        else:
            input_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
            display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(display_frame, text="CHI TIẾT ĐÃ NHẬP", font=("Arial", 14, "bold")).pack(pady=10)

        # Frame cho chi tiết SP đã nhập
        sp_detail_frame = tk.LabelFrame(display_frame, text="Sản phẩm (Xe) đã nhập", 
                                        font=("Arial", 11), padx=5, pady=5)
        sp_detail_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        cols_sp_detail = ("MaChiTiet", "Tên Sản Phẩm", "Số Lượng", "Đơn Giá", "Thành Tiền")
        dialog.tree_sp_detail = ttk.Treeview(sp_detail_frame, columns=cols_sp_detail, show="headings", height=8)
        dialog.tree_sp_detail.heading("MaChiTiet", text="ID")
        dialog.tree_sp_detail.heading("Tên Sản Phẩm", text="Tên Sản Phẩm")
        dialog.tree_sp_detail.heading("Số Lượng", text="SL")
        dialog.tree_sp_detail.heading("Đơn Giá", text="Đơn Giá")
        dialog.tree_sp_detail.heading("Thành Tiền", text="Thành Tiền")
        dialog.tree_sp_detail.column("MaChiTiet", width=0, stretch=tk.NO) 
        dialog.tree_sp_detail.column("Tên Sản Phẩm", width=200)
        dialog.tree_sp_detail.column("Số Lượng", width=50, anchor="center")
        dialog.tree_sp_detail.column("Đơn Giá", width=100, anchor="e")
        dialog.tree_sp_detail.column("Thành Tiền", width=100, anchor="e")
        dialog.tree_sp_detail.pack(fill=tk.BOTH, expand=True)

        # Frame cho chi tiết PT đã nhập
        pt_detail_frame = tk.LabelFrame(display_frame, text="Phụ tùng đã nhập", 
                                        font=("Arial", 11), padx=5, pady=5)
        pt_detail_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        cols_pt_detail = ("MaChiTiet", "Tên Phụ Tùng", "Số Lượng", "Đơn Giá", "Thành Tiền")
        dialog.tree_pt_detail = ttk.Treeview(pt_detail_frame, columns=cols_pt_detail, show="headings", height=8)
        dialog.tree_pt_detail.heading("MaChiTiet", text="ID")
        dialog.tree_pt_detail.heading("Tên Phụ Tùng", text="Tên Phụ Tùng")
        dialog.tree_pt_detail.heading("Số Lượng", text="SL")
        dialog.tree_pt_detail.heading("Đơn Giá", text="Đơn Giá")
        dialog.tree_pt_detail.heading("Thành Tiền", text="Thành Tiền")
        dialog.tree_pt_detail.column("MaChiTiet", width=0, stretch=tk.NO)
        dialog.tree_pt_detail.column("Tên Phụ Tùng", width=200)
        dialog.tree_pt_detail.column("Số Lượng", width=50, anchor="center") 
        dialog.tree_pt_detail.column("Đơn Giá", width=100, anchor="e")
        dialog.tree_pt_detail.column("Thành Tiền", width=100, anchor="e")
        dialog.tree_pt_detail.pack(fill=tk.BOTH, expand=True)

        # Nút Xóa (Chỉ hiển thị khi is_view_only=False)
        if not is_view_only:
            tk.Button(display_frame, text="🗑️ Xóa mục đã chọn", font=("Arial", 11, "bold"), 
                      bg="#dc3545", fg="white", 
                      command=lambda: self._delete_item_from_phieu(dialog, pn_id)).pack(pady=10)
        
        # Nút Đóng (Nếu là 'chỉ xem' thì thêm nút Đóng)
        if is_view_only:
            tk.Button(display_frame, text="Đóng", font=("Arial", 11, "bold"), 
                      bg="#6c757d", fg="white", 
                      command=dialog.destroy).pack(pady=10)

        # Tải chi tiết đã có của phiếu nhập (luôn luôn)
        self._load_existing_details(dialog, pn_id)

    def _load_existing_details(self, dialog, pn_id):
        """Hàm nội bộ: Tải các chi tiết đã có của phiếu nhập (bên phải)"""
        
        # Xóa dữ liệu cũ trên cây
        for item in dialog.tree_sp_detail.get_children():
            dialog.tree_sp_detail.delete(item)
        for item in dialog.tree_pt_detail.get_children():
            dialog.tree_pt_detail.delete(item)

        try:
            # Tải chi tiết sản phẩm
            query_sp = """
                SELECT ct.MaChiTiet, sp.TenSanPham, ct.SoLuong, ct.DonGia, (ct.SoLuong * ct.DonGia) AS ThanhTien
                FROM ChiTietPhieuNhapSanPham ct
                JOIN SanPham sp ON ct.MaSanPham = sp.MaSanPham
                WHERE ct.MaPhieuNhap = %s
            """
            products = self.db.fetch_all(query_sp, (pn_id,))
            if products:
                for p in products:
                    dialog.tree_sp_detail.insert("", tk.END, values=(
                        p['MaChiTiet'],
                        p['TenSanPham'],
                        p['SoLuong'],
                        f"{p['DonGia']:,.0f}",
                        f"{p['ThanhTien']:,.0f}"
                    ))
            
            # Tải chi tiết phụ tùng
            query_pt = """
                SELECT ct.MaChiTiet, pt.TenPhuTung, ct.SoLuong, ct.DonGia, (ct.SoLuong * ct.DonGia) AS ThanhTien
                FROM ChiTietPhieuNhapPhuTung ct
                JOIN PhuTung pt ON ct.MaPhuTung = pt.MaPhuTung
                WHERE ct.MaPhieuNhap = %s
            """
            parts = self.db.fetch_all(query_pt, (pn_id,))
            if parts:
                for p in parts:
                    dialog.tree_pt_detail.insert("", tk.END, values=(
                        p['MaChiTiet'],
                        p['TenPhuTung'],
                        p['SoLuong'],
                        f"{p['DonGia']:,.0f}",
                        f"{p['ThanhTien']:,.0f}"
                    ))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải chi tiết phiếu nhập: {e}", parent=dialog)

    def _delete_item_from_phieu(self, dialog, pn_id):
        """Hàm nội bộ: Xóa một chi tiết khỏi phiếu nhập"""
        
        ma_chi_tiet = None
        table_name = None
        item_name = None
        
        # Kiểm tra cây sản phẩm chi tiết
        selected_sp = dialog.tree_sp_detail.selection()
        if selected_sp:
            item = dialog.tree_sp_detail.item(selected_sp[0])
            ma_chi_tiet = item['values'][0]
            item_name = item['values'][1]
            table_name = "ChiTietPhieuNhapSanPham"
        else:
            # Nếu không, kiểm tra cây phụ tùng chi tiết
            selected_pt = dialog.tree_pt_detail.selection()
            if selected_pt:
                item = dialog.tree_pt_detail.item(selected_pt[0])
                ma_chi_tiet = item['values'][0]
                item_name = item['values'][1]
                table_name = "ChiTietPhieuNhapPhuTung"
        
        if not ma_chi_tiet:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một mục ở bảng bên phải để xóa.", parent=dialog)
            return

        if messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc muốn xóa '{item_name}'\nkhỏi phiếu nhập này?", parent=dialog):
            try:
                # Xóa chi tiết
                query = f"DELETE FROM {table_name} WHERE MaChiTiet = %s"
                result = self.db.execute_query(query, (ma_chi_tiet,))
                
                # Cập nhật tổng tiền (Trigger của bạn chỉ chạy khi INSERT, không chạy khi DELETE)
                update_query = """
                    UPDATE PhieuNhapKho
                    SET TongTien = (
                        SELECT ISNULL(SUM(ThanhTien), 0) 
                        FROM ChiTietPhieuNhapSanPham 
                        WHERE MaPhieuNhap = %s
                    ) + (
                        SELECT ISNULL(SUM(ThanhTien), 0) 
                        FROM ChiTietPhieuNhapPhuTung 
                        WHERE MaPhieuNhap = %s
                    )
                    WHERE MaPhieuNhap = %s
                """
                self.db.execute_query(update_query, (pn_id, pn_id, pn_id))

                if result:
                    messagebox.showinfo("Thành công", f"Đã xóa '{item_name}'.", parent=dialog)
                    # Tải lại danh sách chi tiết (bên phải)
                    self._load_existing_details(dialog, pn_id)
                    # Tải lại danh sách phiếu nhập (màn hình chính) để cập nhật Tổng Tiền
                    self.load_phieu_nhap() 
                else:
                    messagebox.showerror("Lỗi", "Không thể xóa chi tiết.", parent=dialog)
            except Exception as e:
                messagebox.showerror("Lỗi CSDL", f"Không thể xóa: {e}", parent=dialog)

    def _load_all_products(self, tree_sp):
        """Hàm nội bộ: Tải tất cả sản phẩm (bất kể tồn kho)"""
        try:
            # Xóa dữ liệu cũ (phòng trường hợp)
            for item in tree_sp.get_children():
                tree_sp.delete(item)
                
            query = """
                SELECT sp.MaSanPham, sp.TenSanPham, hx.TenHangXe 
                FROM SanPham sp
                LEFT JOIN HangXe hx ON sp.MaHangXe = hx.MaHangXe
                ORDER BY sp.TenSanPham
            """
            products = self.db.fetch_all(query)
            if products:
                for p in products:
                    tree_sp.insert("", tk.END, values=(
                        p['MaSanPham'], 
                        p['TenSanPham'], 
                        p['TenHangXe'] or "N/A"
                    ))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách sản phẩm: {e}")

    def _load_all_parts(self, tree_pt):
        """Hàm nội bộ: Tải tất cả phụ tùng (bất kể tồn kho)"""
        try:
            # Xóa dữ liệu cũ
            for item in tree_pt.get_children():
                tree_pt.delete(item)
                
            query = """
                SELECT pt.MaPhuTung, pt.TenPhuTung, lpt.TenLoaiPhuTung
                FROM PhuTung pt
                LEFT JOIN LoaiPhuTung lpt ON pt.MaLoaiPhuTung = lpt.MaLoaiPhuTung
                ORDER BY pt.TenPhuTung
            """
            parts = self.db.fetch_all(query)
            if parts:
                for p in parts:
                    tree_pt.insert("", tk.END, values=(
                        p['MaPhuTung'], 
                        p['TenPhuTung'], 
                        p['TenLoaiPhuTung'] or "N/A"
                    ))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách phụ tùng: {e}")

    def _add_item_to_phieu(self, dialog, pn_id, tab_control, tree_sp, tree_pt):
        """Hàm nội bộ: Xử lý logic thêm item vào CSDL"""
        
        try:
            current_tab = tab_control.index(tab_control.select()) # 0 = Sản phẩm, 1 = Phụ tùng
            
            if current_tab == 0:
                selected_item_tree = tree_sp
                selected = selected_item_tree.selection()
                if not selected:
                    messagebox.showwarning("Cảnh báo", "Vui lòng chọn một SẢN PHẨM (XE MÁY)!", parent=dialog)
                    return
                item_id = selected_item_tree.item(selected[0])['values'][0]
                item_name = selected_item_tree.item(selected[0])['values'][1]
                table_name = "ChiTietPhieuNhapSanPham"
                id_col = "MaSanPham"
                
            elif current_tab == 1:
                selected_item_tree = tree_pt
                selected = selected_item_tree.selection()
                if not selected:
                    messagebox.showwarning("Cảnh báo", "Vui lòng chọn một PHỤ TÙNG!", parent=dialog)
                    return
                item_id = selected_item_tree.item(selected[0])['values'][0]
                item_name = selected_item_tree.item(selected[0])['values'][1]
                table_name = "ChiTietPhieuNhapPhuTung"
                id_col = "MaPhuTung"
            
            # --- Đọc dữ liệu từ 2 ô Entry ---
            so_luong_str = dialog.entry_so_luong.get().strip()
            don_gia_str = dialog.entry_don_gia.get().strip()

            if not so_luong_str or not don_gia_str:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập Số Lượng và Đơn Giá Nhập.", parent=dialog)
                return

            try:
                so_luong = int(so_luong_str)
                don_gia = float(don_gia_str)
            except ValueError:
                messagebox.showerror("Lỗi", "Số lượng hoặc Đơn giá không hợp lệ.\nVui lòng chỉ nhập số.", parent=dialog)
                return

            if so_luong <= 0 or don_gia < 0:
                messagebox.showerror("Lỗi", "Số lượng phải lớn hơn 0 và Đơn giá không được âm.", parent=dialog)
                return
            # --- KẾT THÚC ĐỌC DỮ LIỆU ---

            # --- Thực thi Query ---
            query = f"""
                INSERT INTO {table_name} (MaPhieuNhap, {id_col}, SoLuong, DonGia)
                VALUES (%s, %s, %s, %s)
            """
            
            result = self.db.execute_query(query, (pn_id, item_id, so_luong, don_gia))

            if result:
                messagebox.showinfo("Thành công", f"Đã thêm {so_luong} x {item_name} vào phiếu nhập.", parent=dialog)
                
                # Tải lại danh sách phiếu nhập ở màn hình chính (Admin)
                self.load_phieu_nhap()
                
                # Tải lại chi tiết ở bảng bên phải
                self._load_existing_details(dialog, pn_id)

                # Xóa nội dung 2 ô entry sau khi thêm thành công
                dialog.entry_so_luong.delete(0, tk.END)
                dialog.entry_don_gia.delete(0, tk.END)
            else:
                messagebox.showerror("Lỗi", "Không thể thêm chi tiết vào phiếu nhập.", parent=dialog)

        except Exception as e:
            messagebox.showerror("Lỗi nghiêm trọng", f"Có lỗi xảy ra: {e}", parent=dialog)

    def delete_phieu_nhap(self):
        """Xóa phiếu nhập (chỉ khi ở trạng thái 'ChoXacNhan')"""
        selected = self.view.phieu_nhap_tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn phiếu nhập để xóa.")
            return

        item = self.view.phieu_nhap_tree.item(selected[0])
        pn_id = item['values'][0]
        trang_thai = item['values'][5]

        if trang_thai != 'ChoXacNhan':
            messagebox.showerror("Lỗi", "Chỉ có thể xóa phiếu nhập ở trạng thái 'Chờ Xác Nhận'.")
            return
        
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa Phiếu Nhập #{pn_id}?\nMọi chi tiết (nếu có) cũng sẽ bị xóa."):
            try:
                # Phải xóa chi tiết trước (theo ràng buộc khóa ngoại)
                self.db.execute_query("DELETE FROM ChiTietPhieuNhapSanPham WHERE MaPhieuNhap = %s", (pn_id,))
                self.db.execute_query("DELETE FROM ChiTietPhieuNhapPhuTung WHERE MaPhieuNhap = %s", (pn_id,))
                
                # Xóa phiếu nhập
                result = self.db.execute_query("DELETE FROM PhieuNhapKho WHERE MaPhieuNhap = %s", (pn_id,))
                
                if result:
                    messagebox.showinfo("Thành công", f"Đã xóa Phiếu Nhập #{pn_id}.")
                    self.load_phieu_nhap()
                else:
                    messagebox.showerror("Lỗi", "Không thể xóa phiếu nhập.")
            except Exception as e:
                messagebox.showerror("Lỗi CSDL", f"Không thể xóa: {e}")