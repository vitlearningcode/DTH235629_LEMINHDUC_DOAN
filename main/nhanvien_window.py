# =================================================================
# FILE: nhanvien_window.py
# MÔ TẢ: Class NhanVien - Giao diện nhân viên (lập hóa đơn, bán hàng)
# =================================================================

import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from database_connection import DatabaseConnection
from datetime import datetime

class NhanVien:
    def __init__(self, user_info):
        """Khởi tạo cửa sổ Nhân viên"""
        self.window = tk.Tk()
        self.window.title(f"NHÂN VIÊN - {user_info['HoTen']}")
        self.window.geometry("1200x700")
        self.window.state('zoomed')
        
        self.user_info = user_info
        
        # Màu sắc
        self.bg_color = "#F0F8FF"
        self.menu_color = "#87CEEB"
        self.btn_color = "#4682B4"
        self.text_color = "#FFFFFF"
        
        # Database
        self.db = DatabaseConnection()
        self.db.connect()
        
        # Giỏ hàng tạm
        self.cart_items = []
        
        self.setup_ui()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()
    
    def setup_ui(self):
        """Thiết lập giao diện"""
        # Header
        header_frame = tk.Frame(self.window, bg=self.menu_color, height=60)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        
        tk.Label(
            header_frame,
            text="HỆ THỐNG BÁN HÀNG - NHÂN VIÊN",
            font=("Arial", 18, "bold"),
            bg=self.menu_color,
            fg="#003366"
        ).pack(side=tk.LEFT, padx=20, pady=10)
        
        tk.Label(
            header_frame,
            text=f"Nhân viên: {self.user_info['HoTen']}",
            font=("Arial", 12),
            bg=self.menu_color,
            fg="#003366"
        ).pack(side=tk.RIGHT, padx=20, pady=10)
        
        tk.Button(
            header_frame,
            text="Đăng xuất",
            font=("Arial", 10, "bold"),
            bg="#DC143C",
            fg=self.text_color,
            command=self.logout
        ).pack(side=tk.RIGHT, padx=10)
        
        # Menu
        menu_frame = tk.Frame(self.window, bg=self.menu_color, width=250)
        menu_frame.pack(fill=tk.Y, side=tk.LEFT)
        
        # Nội dung
        self.content_frame = tk.Frame(self.window, bg=self.bg_color)
        self.content_frame.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)
        
        self.create_menu(menu_frame)
        self.show_sales_screen()
    
    def create_menu(self, parent):
        """Tạo menu"""
        menu_items = [
            ("🛒 Bán hàng", self.show_sales_screen),
            ("🔧 Dịch vụ sửa chữa", self.show_service_screen),
            ("🏍️ Xem sản phẩm", self.view_products),
            ("👤 Tìm khách hàng", self.search_customer),
            ("📄 Lịch sử hóa đơn", self.view_invoice_history)
        ]
        
        tk.Label(
            parent,
            text="MENU",
            font=("Arial", 14, "bold"),
            bg=self.menu_color,
            fg="#003366"
        ).pack(pady=20)
        
        for text, command in menu_items:
            btn = tk.Button(
                parent,
                text=text,
                font=("Arial", 11),
                bg=self.btn_color,
                fg=self.text_color,
                width=25,
                height=2,
                cursor="hand2",
                command=command,
                anchor="w",
                padx=10
            )
            btn.pack(pady=5, padx=10)
    
    def clear_content(self):
        """Xóa nội dung"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_sales_screen(self):
        """Màn hình bán hàng"""
        self.clear_content()
        self.cart_items = []
        
        # Title
        tk.Label(
            self.content_frame,
            text="TẠO HÓA ĐƠN BÁN HÀNG & DỊCH VỤ",
            font=("Arial", 18, "bold"),
            bg=self.bg_color,
            fg="#003366"
        ).pack(pady=10)
        
        # Frame chính chia 2 cột
        main_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Cột trái - Thông tin khách hàng và sản phẩm
        left_frame = tk.Frame(main_frame, bg=self.bg_color)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        # Thông tin khách hàng (Giữ nguyên)
        customer_frame = tk.LabelFrame(left_frame, text="Thông tin khách hàng", 
                                       font=("Arial", 12, "bold"), bg="white", padx=10, pady=10)
        customer_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(customer_frame, text="Số điện thoại:", font=("Arial", 11), bg="white").grid(row=0, column=0, sticky="w", pady=5)
        self.phone_entry = tk.Entry(customer_frame, font=("Arial", 11), width=20)
        self.phone_entry.grid(row=0, column=1, pady=5, padx=5)
        
        tk.Button(
            customer_frame,
            text="🔍 Tìm",
            font=("Arial", 10),
            bg=self.btn_color,
            fg="white",
            command=self.search_customer_by_phone
        ).grid(row=0, column=2, pady=5, padx=5)
        
        tk.Button(
            customer_frame,
            text="➕ Thêm mới",
            font=("Arial", 10),
            bg="#28a745",
            fg="white",
            command=self.add_new_customer
        ).grid(row=0, column=3, pady=5, padx=5)
        
        tk.Label(customer_frame, text="Họ tên:", font=("Arial", 11), bg="white").grid(row=1, column=0, sticky="w", pady=5)
        self.customer_name_var = tk.StringVar()
        tk.Entry(customer_frame, textvariable=self.customer_name_var, font=("Arial", 11), width=40, state="readonly").grid(row=1, column=1, columnspan=3, pady=5, padx=5, sticky="w")
        
        # --- NÂNG CẤP: SỬ DỤNG TAB CONTROL ---
        product_frame = tk.LabelFrame(left_frame, text="Chọn sản phẩm / Phụ tùng", 
                                      font=("Arial", 12, "bold"), bg="white", padx=10, pady=10)
        product_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.tab_control = ttk.Notebook(product_frame)
        
        self.tab_products = ttk.Frame(self.tab_control)
        self.tab_parts = ttk.Frame(self.tab_control)
        
        self.tab_control.add(self.tab_products, text='   🏍️ Xe máy (Sản phẩm)   ')
        self.tab_control.add(self.tab_parts, text='   🔧 Phụ tùng & Dịch vụ   ')
        
        self.tab_control.pack(fill=tk.BOTH, expand=True)

        # Tab 1: Danh sách sản phẩm (Xe máy)
        columns_sp = ("Mã", "Tên sản phẩm", "Hãng", "Giá bán", "Tồn kho")
        self.product_tree = ttk.Treeview(self.tab_products, columns=columns_sp, show="headings", height=15)
        for col in columns_sp:
            self.product_tree.heading(col, text=col)
            w = 250 if col == "Tên sản phẩm" else 100
            self.product_tree.column(col, width=w, anchor="center" if col != "Tên sản phẩm" else "w")
        
        scrollbar_sp = ttk.Scrollbar(self.tab_products, orient="vertical", command=self.product_tree.yview)
        self.product_tree.configure(yscrollcommand=scrollbar_sp.set)
        self.product_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_sp.pack(side=tk.RIGHT, fill=tk.Y)

        # Tab 2: Danh sách phụ tùng
        columns_pt = ("Mã", "Tên phụ tùng", "Loại", "Giá bán", "Tồn kho")
        self.part_tree = ttk.Treeview(self.tab_parts, columns=columns_pt, show="headings", height=15)
        for col in columns_pt:
            self.part_tree.heading(col, text=col)
            w = 250 if col == "Tên phụ tùng" else 100
            self.part_tree.column(col, width=w, anchor="center" if col != "Tên phụ tùng" else "w")

        scrollbar_pt = ttk.Scrollbar(self.tab_parts, orient="vertical", command=self.part_tree.yview)
        self.part_tree.configure(yscrollcommand=scrollbar_pt.set)
        self.part_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_pt.pack(side=tk.RIGHT, fill=tk.Y)
        
        # --- KẾT THÚC NÂNG CẤP ---

        # Nút thêm vào giỏ
        tk.Button(
            left_frame,
            text="➕ Thêm vào giỏ hàng",
            font=("Arial", 12, "bold"),
            bg="#28a745",
            fg="white",
            command=self.add_to_cart
        ).pack(pady=10)
        
        # Load sản phẩm và phụ tùng
        self.load_products()
        self.load_parts()
        
        # Cột phải - Giỏ hàng (Giữ nguyên)
        right_frame = tk.Frame(main_frame, bg=self.bg_color, width=450)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10)
        right_frame.pack_propagate(False)
        
        cart_frame = tk.LabelFrame(right_frame, text="Giỏ hàng", 
                                   font=("Arial", 12, "bold"), bg="white", padx=10, pady=10)
        cart_frame.pack(fill=tk.BOTH, expand=True)
        
        cart_columns = ("Tên", "SL", "Đơn giá", "Thành tiền")
        self.cart_tree = ttk.Treeview(cart_frame, columns=cart_columns, show="headings", height=12)
        
        widths = {"Tên": 180, "SL": 50, "Đơn giá": 100, "Thành tiền": 100}
        for col in cart_columns:
            self.cart_tree.heading(col, text=col)
            self.cart_tree.column(col, width=widths[col], anchor="center" if col != "Tên" else "w")
        
        self.cart_tree.pack(fill=tk.BOTH, expand=True)
        
        tk.Button(
            cart_frame,
            text="🗑️ Xóa khỏi giỏ",
            font=("Arial", 10),
            bg="#dc3545",
            fg="white",
            command=self.remove_from_cart
        ).pack(pady=5)
        
        total_frame = tk.Frame(right_frame, bg="white", bd=2, relief=tk.RAISED)
        total_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(total_frame, text="TỔNG TIỀN:", font=("Arial", 14, "bold"), bg="white").pack(pady=10)
        self.total_label = tk.Label(total_frame, text="0 VNĐ", font=("Arial", 18, "bold"), bg="white", fg="red")
        self.total_label.pack(pady=5)
        
        tk.Button(
            right_frame,
            text="💳 THANH TOÁN",
            font=("Arial", 14, "bold"),
            bg="#007bff",
            fg="white",
            command=self.process_payment,
            height=2
        ).pack(fill=tk.X, pady=10)
    
    def load_products(self):
        """Tải danh sách sản phẩm còn hàng"""
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
        
        query = """
            SELECT sp.MaSanPham, sp.TenSanPham, hx.TenHangXe, sp.GiaBan, sp.SoLuongTon
            FROM SanPham sp
            JOIN HangXe hx ON sp.MaHangXe = hx.MaHangXe
            WHERE sp.TrangThai = 'ConHang' AND sp.SoLuongTon > 0
            ORDER BY sp.TenSanPham
        """
        products = self.db.fetch_all(query)
        
        for p in products:
            self.product_tree.insert("", tk.END, values=(
                p['MaSanPham'],
                p['TenSanPham'],
                p['TenHangXe'],
                f"{p['GiaBan']:,.0f}",
                p['SoLuongTon']
            ))
    
    def load_parts(self):
        """Tải danh sách phụ tùng còn hàng"""
        for item in self.part_tree.get_children():
            self.part_tree.delete(item)
        
        query = """
            SELECT pt.MaPhuTung, pt.TenPhuTung, lpt.TenLoaiPhuTung, pt.GiaBan, pt.SoLuongTon
            FROM PhuTung pt
            LEFT JOIN LoaiPhuTung lpt ON pt.MaLoaiPhuTung = lpt.MaLoaiPhuTung
            WHERE pt.TrangThai = 'ConHang' AND pt.SoLuongTon > 0
            ORDER BY pt.TenPhuTung
        """
        parts = self.db.fetch_all(query)
        
        if parts:
            for p in parts:
                self.part_tree.insert("", tk.END, values=(
                    p['MaPhuTung'],
                    p['TenPhuTung'],
                    p['TenLoaiPhuTung'] or "N/A",
                    f"{p['GiaBan']:,.0f}",
                    p['SoLuongTon']
                ))


    def search_customer_by_phone(self):
        """Tìm khách hàng theo SĐT"""
        phone = self.phone_entry.get().strip()
        if not phone:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập số điện thoại!")
            return
        
        query = "SELECT * FROM KhachHang WHERE SoDienThoai = %s"
        customer = self.db.fetch_one(query, (phone,))
        
        if customer:
            self.current_customer = customer
            self.customer_name_var.set(customer['HoTen'])
            messagebox.showinfo("Thành công", f"Tìm thấy khách hàng: {customer['HoTen']}")
        else:
            self.customer_name_var.set("")
            if messagebox.askyesno("Không tìm thấy", "Khách hàng chưa có trong hệ thống.\nBạn có muốn thêm mới?"):
                self.add_new_customer()
    
    def add_new_customer(self):
        """Thêm khách hàng mới"""
        dialog = tk.Toplevel(self.window)
        dialog.title("Thêm khách hàng")
        dialog.geometry("450x400")
        dialog.resizable(False, False)
        
        fields = [
            ("Họ tên:", "fullname"),
            ("Số điện thoại:", "phone"),
            ("Email:", "email"),
            ("Địa chỉ:", "address"),
            ("CMND:", "cmnd")
        ]
        
        entries = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(dialog, text=label, font=("Arial", 11)).grid(row=i, column=0, padx=20, pady=10, sticky="w")
            entry = tk.Entry(dialog, font=("Arial", 11), width=30)
            entry.grid(row=i, column=1, padx=20, pady=10)
            entries[key] = entry
        
        # Giới tính
        tk.Label(dialog, text="Giới tính:", font=("Arial", 11)).grid(row=len(fields), column=0, padx=20, pady=10, sticky="w")
        gender_var = tk.StringVar(value="Nam")
        gender_combo = ttk.Combobox(dialog, textvariable=gender_var, values=["Nam", "Nu", "Khac"], 
                                    font=("Arial", 11), state="readonly", width=28)
        gender_combo.grid(row=len(fields), column=1, padx=20, pady=10)
        
        def save():
            fullname = entries["fullname"].get().strip()
            phone = entries["phone"].get().strip()
            email = entries["email"].get().strip()
            address = entries["address"].get().strip()
            cmnd = entries["cmnd"].get().strip()
            
            if not fullname or not phone:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập họ tên và số điện thoại!")
                return
            
            query = """
                INSERT INTO KhachHang (HoTen, SoDienThoai, Email, DiaChi, CMND, GioiTinh)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            result = self.db.execute_query(query, (fullname, phone, email, address, cmnd, gender_var.get()))
            
            if result:
                messagebox.showinfo("Thành công", "Thêm khách hàng thành công!")
                self.phone_entry.delete(0, tk.END)
                self.phone_entry.insert(0, phone)
                dialog.destroy()
                self.search_customer_by_phone()
            else:
                messagebox.showerror("Lỗi", "Không thể thêm khách hàng!")
        
        tk.Button(
            dialog,
            text="💾 Lưu",
            font=("Arial", 12, "bold"),
            bg="#28a745",
            fg="white",
            command=save,
            width=15
        ).grid(row=len(fields)+1, column=0, columnspan=2, pady=20)
    
    def add_to_cart(self):
        """Thêm sản phẩm hoặc phụ tùng vào giỏ"""
        try:
            current_tab = self.tab_control.index(self.tab_control.select())
            
            # current_tab == 0 là tab Xe máy
            # current_tab == 1 là tab Phụ tùng
            
            if current_tab == 0:
                tree = self.product_tree
                item_type = 'SanPham'
                selected = tree.selection()
                if not selected:
                    messagebox.showwarning("Cảnh báo", "Vui lòng chọn một SẢN PHẨM (XE MÁY)!")
                    return
            elif current_tab == 1:
                tree = self.part_tree
                item_type = 'PhuTung'
                selected = tree.selection()
                if not selected:
                    messagebox.showwarning("Cảnh báo", "Vui lòng chọn một PHỤ TÙNG!")
                    return
            else:
                return

            item = tree.item(selected[0])
            values = item['values']
            
            item_id = values[0]
            name = values[1]
            price = float(values[3].replace(',', ''))
            stock = int(values[4])
            
            # Kiểm tra xem đã có trong giỏ chưa
            for cart_item in self.cart_items:
                if cart_item['id'] == item_id and cart_item['type'] == item_type:
                    messagebox.showwarning("Thông báo", f"'{name}' đã có trong giỏ hàng.")
                    return

            # Hỏi số lượng
            quantity = tk.simpledialog.askinteger(
                "Số lượng", 
                f"Nhập số lượng cho:\n{name}\n(Tồn kho: {stock})", 
                minvalue=1, 
                maxvalue=stock
            )
            
            if quantity:
                # Kiểm tra tồn kho (đã được xử lý bởi maxvalue, nhưng cẩn thận vẫn hơn)
                if quantity > stock:
                    messagebox.showwarning("Cảnh báo", "Số lượng vượt quá tồn kho!")
                    return
                
                total = price * quantity
                
                # Thêm vào giỏ
                self.cart_items.append({
                    'id': item_id,
                    'name': name,
                    'quantity': quantity,
                    'price': price,
                    'total': total,
                    'type': item_type  # << Rất quan trọng
                })
                
                self.update_cart_display()
        
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra khi thêm vào giỏ: {e}")
    

    def remove_from_cart(self):
        """Xóa sản phẩm khỏi giỏ"""
        selected = self.cart_tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sản phẩm cần xóa!")
            return
        
        index = self.cart_tree.index(selected[0])
        del self.cart_items[index]
        self.update_cart_display()
    
    def update_cart_display(self):
        """Cập nhật hiển thị giỏ hàng"""
        # Xóa hiển thị cũ
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
        
        # Hiển thị lại
        total = 0
        for item in self.cart_items:
            self.cart_tree.insert("", tk.END, values=(
                item['name'],
                item['quantity'],
                f"{item['price']:,.0f}",
                f"{item['total']:,.0f}"
            ))
            total += item['total']
        
        # Cập nhật tổng tiền
        self.total_label.config(text=f"{total:,.0f} VNĐ")
    
   
    def process_payment(self):
        """Xử lý thanh toán (Hỗ trợ cả Sản phẩm và Phụ tùng)"""
        if not self.cart_items:
            messagebox.showwarning("Cảnh báo", "Giỏ hàng trống!")
            return
        
        if not hasattr(self, 'current_customer'):
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn khách hàng!")
            return
        
        # Tính tổng tiền
        total = sum(item['total'] for item in self.cart_items)
        
        # --- Tạo hóa đơn ---
        # (Giả sử thanh toán đủ, nếu cần trả góp/ghi nợ, bạn cần thêm logic ở đây)
        query = """
            INSERT INTO HoaDon (MaKhachHang, MaNguoiDung, TongTien, TongThanhToan, TienDaTra, PhuongThucThanhToan, TrangThai)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        try:
            invoice_id = self.db.execute_query(
                query,
                (self.current_customer['MaKhachHang'], self.user_info['MaNguoiDung'], 
                 total, total, total, 'TienMat', 'DaThanhToan')
            )
            
            if not invoice_id:
                messagebox.showerror("Lỗi", "Không thể tạo hóa đơn! (ID trả về null)")
                return

            # --- Thêm chi tiết hóa đơn (Phần nâng cấp) ---
            for item in self.cart_items:
                if item['type'] == 'SanPham':
                    detail_query = """
                        INSERT INTO ChiTietHoaDonSanPham (MaHoaDon, MaSanPham, SoLuong, DonGia)
                        VALUES (%s, %s, %s, %s)
                    """
                    params = (invoice_id, item['id'], item['quantity'], item['price'])
                
                elif item['type'] == 'PhuTung':
                    detail_query = """
                        INSERT INTO ChiTietHoaDonPhuTung (MaHoaDon, MaPhuTung, SoLuong, DonGia)
                        VALUES (%s, %s, %s, %s)
                    """
                    params = (invoice_id, item['id'], item['quantity'], item['price'])
                
                # Thực thi trigger (trừ tồn kho) sẽ diễn ra ở đây
                self.db.execute_query(detail_query, params)
            
            messagebox.showinfo("Thành công", f"Tạo hóa đơn thành công!\nMã hóa đơn: {invoice_id}")
            
            # Reset
            self.cart_items = []
            self.update_cart_display()
            self.customer_name_var.set("")
            self.phone_entry.delete(0, tk.END)
            delattr(self, 'current_customer')
            
            # Tải lại cả sản phẩm và phụ tùng (vì tồn kho đã thay đổi)
            self.load_products()
            self.load_parts()
        
        except Exception as e:
            # Nếu có lỗi (ví dụ trigger báo hết hàng), ta cần báo lỗi
            # Lưu ý: Cần có cơ chế Rollback nếu 1 chi tiết bị lỗi
            messagebox.showerror("Lỗi", f"Không thể tạo hóa đơn! \n{e}")
    

    def show_service_screen(self):
        """Màn hình dịch vụ sửa chữa"""
        self.clear_content()
        tk.Label(
            self.content_frame,
            text="DỊCH VỤ SỬA CHỮA - BẢO DƯỠNG",
            font=("Arial", 18, "bold"),
            bg=self.bg_color
        ).pack(pady=20)
        tk.Label(
            self.content_frame,
            text="Chức năng tương tự bán hàng\nNhưng sử dụng bảng PhuTung thay vì SanPham",
            font=("Arial", 12),
            bg=self.bg_color
        ).pack(pady=20)
    
    
    def view_products(self):
        """Xem danh sách sản phẩm"""
        self.clear_content()
        tk.Label(
            self.content_frame,
            text="DANH SÁCH SẢN PHẨM",
            font=("Arial", 18, "bold"),
            bg=self.bg_color
        ).pack(pady=20)
    
    def search_customer(self):
        """Tìm kiếm khách hàng"""
        self.clear_content()
        tk.Label(
            self.content_frame,
            text="TÌM KIẾM KHÁCH HÀNG",
            font=("Arial", 18, "bold"),
            bg=self.bg_color
        ).pack(pady=20)
    
    def view_invoice_history(self):
        """Xem lịch sử hóa đơn"""
        self.clear_content()
        tk.Label(
            self.content_frame,
            text="LỊCH SỬ HÓA ĐƠN",
            font=("Arial", 18, "bold"),
            bg=self.bg_color
        ).pack(pady=20)
    
    def logout(self):
        """Đăng xuất"""
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn đăng xuất?"):
            self.db.disconnect()
            self.window.destroy()
            from login import Login
            Login().run()
    
    def on_closing(self):
        """Xử lý đóng cửa sổ"""
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn thoát?"):
            self.db.disconnect()
            self.window.destroy()

    
    
    # Phần còn lại code tương tự show_sales_screen
    # Nhưng thay vì load sản phẩm thì load phụ tùng
    # Và thêm phần nhập công sửa chữa
    