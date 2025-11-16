# =================================================================
# FILE: nhanvien_window.py
# MÔ TẢ: Class NhanVien - Giao diện nhân viên (CHỈ CÓ UI, ĐÃ DỌN DẸP)
# =================================================================

import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from database_connection import DatabaseConnection
from datetime import datetime

# --- 1. IMPORT CÁC LỚP LOGIC ĐÃ TÁCH NHỎ ---
from Function.function_NhanVien.nhanvien_sales_logic import NhanVienSalesLogic
from Function.function_NhanVien.nhanvien_customer_logic import NhanVienCustomerLogic
from Function.function_NhanVien.nhanvien_invoice_logic import NhanVienInvoiceLogic
from Function.function_NhanVien.nhanvien_system_logic import NhanVienSystemLogic
#-------------------------------------------------------------------------
#hieu them vao 
from Function.function_NhanVien.nhanvien_service_logic import NhanVienServiceLogic

# --- KHÔNG CẦN IMPORT LOGIN TẠI ĐÂY ---

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
        
        # Giỏ hàng tạm (Các lớp Logic sẽ truy cập qua self.view.cart_items)
        self.cart_items = []
        
        # --- 2. KHỞI TẠO TẤT CẢ CÁC LỚP LOGIC ---
        self.sales_logic = NhanVienSalesLogic(self)
        self.cust_logic = NhanVienCustomerLogic(self)
        self.invoice_logic = NhanVienInvoiceLogic(self)
        self.system_logic = NhanVienSystemLogic(self)
        self.service_logic = NhanVienServiceLogic(self)
        
        self.setup_ui()
        self.window.protocol("WM_DELETE_WINDOW", self.system_logic.on_closing)
        self.window.mainloop()
    
    def setup_ui(self):
        """Thiết lập giao diện (Chỉ UI)"""
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
            command=self.system_logic.logout # GỌI LOGIC HỆ THỐNG
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
        """Tạo menu (Chỉ UI)"""
        menu_items = [
            ("🛒 Bán hàng", self.show_sales_screen),
            ("🔧 Dịch vụ sửa chữa", self.show_service_screen),
            ("🏍️ Xem sản phẩm", self.view_products),
            ("💰 Quản lý Công nợ", self.show_debt_screen), # <-- THÊM DÒNG MỚI NÀY
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
    
    # =================================================================
    # CÁC HÀM VẼ GIAO DIỆN (UI-DRAWING METHODS)
    # =================================================================

    def show_sales_screen(self):
        """Vẽ Màn hình bán hàng"""
        self.clear_content()
        self.cart_items = [] # Reset giỏ hàng
        
        tk.Label(
            self.content_frame,
            text="TẠO HÓA ĐƠN BÁN HÀNG & DỊCH VỤ",
            font=("Arial", 18, "bold"),
            bg=self.bg_color,
            fg="#003366"
        ).pack(pady=10)
        
        main_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        left_frame = tk.Frame(main_frame, bg=self.bg_color)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        # --- FRAME KHÁCH HÀNG ---
        customer_frame = tk.LabelFrame(left_frame, text="Thông tin khách hàng", 
                                       font=("Arial", 12, "bold"), bg="white", padx=10, pady=10)
        customer_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(customer_frame, text="Số điện thoại:", font=("Arial", 11), bg="white").grid(row=0, column=0, sticky="w", pady=5)
        self.phone_entry = tk.Entry(customer_frame, font=("Arial", 11), width=20)
        self.phone_entry.grid(row=0, column=1, pady=5, padx=5)
        
        # (Lưu ý: chúng ta cần truyền 'event' nên dùng lambda)
        self.phone_entry.bind("<KeyRelease>", lambda event: self.cust_logic.on_phone_entry_release(event))
        # --- KẾT THÚC PHẦN THÊM MỚI ---
        
        #tk.Button(
        #    customer_frame,
        #    text="🔍 Tìm",
        #    font=("Arial", 10),
        #    bg=self.btn_color,
        #    fg="white",
        #    command=self.cust_logic.search_customer_by_phone
         #).grid(row=0, column=2, pady=5, padx=5)
        
        tk.Button(
            customer_frame,
            text="➕ Thêm mới",
            font=("Arial", 10),
            bg="#28a745",
            fg="white",
            command=self.cust_logic.add_new_customer
        ).grid(row=0, column=3, pady=5, padx=5)
        
        tk.Label(customer_frame, text="Họ tên:", font=("Arial", 11), bg="white").grid(row=1, column=0, sticky="w", pady=5)
        self.customer_name_var = tk.StringVar()
        tk.Entry(customer_frame, textvariable=self.customer_name_var, font=("Arial", 11), width=40, state="readonly").grid(row=1, column=1, columnspan=3, pady=5, padx=5, sticky="w")
        
        # --- FRAME SẢN PHẨM / PHỤ TÙNG ---
        product_frame = tk.LabelFrame(left_frame, text="Chọn sản phẩm / Phụ tùng", 
                                      font=("Arial", 12, "bold"), bg="white", padx=10, pady=10)
        product_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.tab_control = ttk.Notebook(product_frame)
        self.tab_products = ttk.Frame(self.tab_control)
        self.tab_parts = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_products, text='   🏍️ Xe máy (Sản phẩm)   ')
        self.tab_control.add(self.tab_parts, text='   🔧 Phụ tùng & Dịch vụ   ')
        self.tab_control.pack(fill=tk.BOTH, expand=True)

        # Cây Sản phẩm (Xe máy)
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

        # Cây Phụ tùng
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
        
        tk.Button(
            left_frame,
            text="➕ Thêm vào giỏ hàng",
            font=("Arial", 12, "bold"),
            bg="#28a745",
            fg="white",
            command=self.sales_logic.add_to_cart
        ).pack(pady=10)
        
        # Tải dữ liệu ban đầu
        self.sales_logic.load_products()
        self.sales_logic.load_parts()
        
        # --- FRAME GIỎ HÀNG (CỘT PHẢI) ---
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
            command=self.sales_logic.remove_from_cart
        ).pack(pady=5)
        
        # --- KHUNG NHẬP TIỀN KHÁCH TRẢ (ĐÃ THÊM) ---
        payment_frame = tk.Frame(right_frame, bg="white", bd=2, relief=tk.RAISED)
        payment_frame.pack(fill=tk.X, pady=(10, 5)) # Pack nó ngay trên total_frame
        
        tk.Label(
            payment_frame, 
            text="Tiền khách trả:", 
            font=("Arial", 12, "bold"), 
            bg="white"
        ).pack(side=tk.LEFT, padx=10, pady=10)
        
        self.payment_entry = tk.Entry(
            payment_frame, 
            font=("Arial", 14, "bold"), 
            width=20, 
            justify="right", 
            fg="#006400" # Màu xanh cho tiền
        )
        self.payment_entry.pack(side=tk.RIGHT, padx=10, pady=10)
        # --- KẾT THÚC KHUNG MỚI ---

        total_frame = tk.Frame(right_frame, bg="white", bd=2, relief=tk.RAISED)
        total_frame.pack(fill=tk.X, pady=(5, 10)) # Sửa lại padding
        
        tk.Label(total_frame, text="TỔNG TIỀN:", font=("Arial", 14, "bold"), bg="white").pack(pady=10)
        self.total_label = tk.Label(total_frame, text="0 VNĐ", font=("Arial", 18, "bold"), bg="white", fg="red")
        self.total_label.pack(pady=5)
        
        tk.Button(
            right_frame,
            text="💳 THANH TOÁN",
            font=("Arial", 14, "bold"),
            bg="#007bff",
            fg="white",
            command=self.sales_logic.process_payment,
            height=2
        ).pack(fill=tk.X, pady=10)
    
    # Mở file: main/UI/nhanvien_window.py
# THAY THẾ toàn bộ hàm show_service_screen CŨ bằng hàm MỚI này:

    def show_service_screen(self):
        """Vẽ Màn hình dịch vụ sửa chữa"""
        self.clear_content()
        
        tk.Label(
            self.content_frame,
            text="TIẾP NHẬN DỊCH VỤ - BẢO HÀNH",
            font=("Arial", 18, "bold"),
            bg=self.bg_color,
            fg="#003366"
        ).pack(pady=10)
        
        main_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # --- CỘT TRÁI: TÌM KIẾM VÀ DANH SÁCH BẢO HÀNH ---
        left_frame = tk.Frame(main_frame, bg=self.bg_color)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        # 1. Khung tìm khách hàng
        customer_frame = tk.LabelFrame(left_frame, text="Tìm Khách Hàng", 
                                       font=("Arial", 12, "bold"), bg="white", padx=10, pady=10)
        customer_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(customer_frame, text="SĐT Khách hàng:", font=("Arial", 11), bg="white").grid(row=0, column=0, sticky="w", pady=5)
        # Gán Entry vào self.view (tức là self) để logic có thể truy cập
        self.service_phone_entry = tk.Entry(customer_frame, font=("Arial", 11), width=20)
        self.service_phone_entry.grid(row=0, column=1, pady=5, padx=5)
        
        tk.Button(
            customer_frame, text="🔍 Tìm", font=("Arial", 10), bg=self.btn_color, fg="white",
            command=self.service_logic.search_customer_by_phone
        ).grid(row=0, column=2, pady=5, padx=5)
        
        tk.Label(customer_frame, text="Họ tên:", font=("Arial", 11), bg="white").grid(row=1, column=0, sticky="w", pady=5)
        self.service_customer_name_var = tk.StringVar(value="Vui lòng tìm SĐT...")
        tk.Entry(customer_frame, textvariable=self.service_customer_name_var, font=("Arial", 11), width=40, state="readonly").grid(row=1, column=1, columnspan=2, pady=5, padx=5, sticky="w")

        # 2. Khung danh sách phiếu bảo hành
        warranty_frame = tk.LabelFrame(left_frame, text="Danh sách Phiếu Bảo Hành (Xe đã mua)", 
                                       font=("Arial", 12, "bold"), bg="white", padx=10, pady=10)
        warranty_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        cols_warranty = ("ID", "Tên Xe", "Từ Ngày", "Đến Ngày", "Trạng Thái")
        self.warranty_tree = ttk.Treeview(warranty_frame, columns=cols_warranty, show="headings", height=15)
        for col in cols_warranty: self.warranty_tree.heading(col, text=col)
        
        self.warranty_tree.column("ID", width=40, anchor="center")
        self.warranty_tree.column("Tên Xe", width=200)
        self.warranty_tree.column("Từ Ngày", width=100, anchor="center")
        self.warranty_tree.column("Đến Ngày", width=100, anchor="center")
        self.warranty_tree.column("Trạng Thái", width=100, anchor="center")
        
        # Gán sự kiện click (chọn) vào hàm logic
        self.warranty_tree.bind("<<TreeviewSelect>>", self.service_logic.on_warranty_select)
        
        self.warranty_tree.pack(fill=tk.BOTH, expand=True)

        # --- CỘT PHẢI: LỊCH SỬ SỬA CHỮA ---
        right_frame = tk.Frame(main_frame, bg=self.bg_color, width=500)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10)
        right_frame.pack_propagate(False)
        
        history_frame = tk.LabelFrame(right_frame, text="Lịch Sử Sửa Chữa (của phiếu đã chọn)", 
                                   font=("Arial", 12, "bold"), bg="white", padx=10, pady=10)
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        cols_history = ("Ngày Sửa", "Mô Tả Lỗi", "Người Xử Lý", "Chi Phí", "Trạng Thái")
        self.history_tree = ttk.Treeview(history_frame, columns=cols_history, show="headings", height=12)
        
        self.history_tree.heading("Ngày Sửa", text="Ngày Sửa")
        self.history_tree.column("Ngày Sửa", width=100, anchor="center")
        self.history_tree.heading("Mô Tả Lỗi", text="Mô Tả Lỗi")
        self.history_tree.column("Mô Tả Lỗi", width=250)
        self.history_tree.heading("Người Xử Lý", text="Người Xử Lý")
        self.history_tree.column("Người Xử Lý", width=150)
        self.history_tree.heading("Chi Phí", text="Chi Phí")
        self.history_tree.column("Chi Phí", width=100, anchor="e")
        self.history_tree.heading("Trạng Thái", text="Trạng Thái")
        self.history_tree.column("Trạng Thái", width=100, anchor="center")
        
        self.history_tree.pack(fill=tk.BOTH, expand=True)

        tk.Button(
            right_frame,
            text="➕ Thêm Lịch Sử Sửa Chữa",
            font=("Arial", 12, "bold"),
            bg="#28a745",
            fg="white",
            command=self.service_logic.add_warranty_history_entry,
            height=2
        ).pack(fill=tk.X, pady=20)
    
    def view_products(self):
        """Vẽ Màn hình xem sản phẩm"""
        self.clear_content()
        tk.Label(
            self.content_frame,
            text="DANH SÁCH SẢN PHẨM",
            font=("Arial", 18, "bold"),
            bg=self.bg_color
        ).pack(pady=20)
    
    
    def view_invoice_history(self):
        """Vẽ Màn hình lịch sử hóa đơn"""
        self.clear_content()
        
        tk.Label(
            self.content_frame,
            text="LỊCH SỬ HÓA ĐƠN (DO BẠN LẬP)",
            font=("Arial", 18, "bold"),
            bg=self.bg_color,
            fg="#003366"
        ).pack(pady=10)
        
        btn_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        btn_frame.pack(pady=10)
        
        tk.Button(
            btn_frame,
            text="🔍 Xem chi tiết",
            font=("Arial", 11),
            bg=self.btn_color,
            fg="white",
            command=self.invoice_logic.show_invoice_details
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            btn_frame,
            text="🔄 Tải lại",
            font=("Arial", 11),
            bg="#17a2b8",
            fg="white",
            command=self.invoice_logic.load_invoice_history
        ).pack(side=tk.LEFT, padx=10)
        
        table_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        columns = ("Mã HĐ", "Khách hàng", "Ngày lập", "Tổng tiền", "Trạng thái")
        self.invoice_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=25)
        
        widths = {"Mã HĐ": 80, "Khách hàng": 250, "Ngày lập": 150, "Tổng tiền": 150, "Trạng thái": 100}
        for col in columns:
            self.invoice_tree.heading(col, text=col)
            self.invoice_tree.column(col, width=widths[col], anchor="center")
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.invoice_tree.yview)
        self.invoice_tree.configure(yscrollcommand=scrollbar.set)
        
        self.invoice_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Tải dữ liệu ban đầu
        self.invoice_logic.load_invoice_history()

    def _validate_payment_input(self, P):
            """Chỉ cho phép nhập số vào ô thanh toán công nợ"""
            if P == "" or P.isdigit():
                return True
            return False

    def show_debt_screen(self):
        """Vẽ Màn hình Quản lý Công Nợ"""
        self.clear_content()
        
        tk.Label(
            self.content_frame,
            text="ĐƠN HÀNG GHI NỢ",
            font=("Arial", 18, "bold"),
            bg=self.bg_color,
            fg="#003366"
        ).pack(pady=10)
        
        # --- KHUNG TÌM KIẾM ---
        search_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        search_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(search_frame, text="Tìm kiếm (Tên hoặc SĐT):", font=("Arial", 11), bg=self.bg_color).pack(side=tk.LEFT, padx=5)
        self.debt_search_entry = tk.Entry(search_frame, font=("Arial", 11), width=30)
        self.debt_search_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            search_frame,
            text="🔍 Tìm / Tải lại",
            font=("Arial", 10, "bold"),
            bg=self.btn_color,
            fg="white",
            command=self.invoice_logic.load_debt_list # Gọi logic đã có
        ).pack(side=tk.LEFT, padx=10)
        
        # --- KHUNG DANH SÁCH NỢ ---
        list_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        cols = ("Mã HĐ", "Khách hàng", "SĐT", "Ngày lập", "Tổng tiền", "Đã trả", "Còn nợ")
        self.debt_tree = ttk.Treeview(list_frame, columns=cols, show="headings", height=10)
        
        widths = {"Mã HĐ": 60, "Khách hàng": 200, "SĐT": 100, "Ngày lập": 120, "Tổng tiền": 120, "Đã trả": 120, "Còn nợ": 120}
        for col in cols:
            self.debt_tree.heading(col, text=col)
            self.debt_tree.column(col, width=widths[col], anchor="center")
            
        # Gán sự kiện Double-click vào hàm logic (sẽ tạo ở bước 2)
        self.debt_tree.bind("<Double-1>", self.invoice_logic.on_debt_select)
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.debt_tree.yview)
        self.debt_tree.configure(yscrollcommand=scrollbar.set)
        self.debt_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # --- KHUNG CHI TIẾT VÀ THANH TOÁN ---
        detail_frame = tk.LabelFrame(
            self.content_frame, 
            text="Chi tiết thanh toán (Double-click một đơn hàng để chọn)", 
            font=("Arial", 12, "bold"), 
            bg="white", 
            padx=10, pady=10
        )
        detail_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Lưu các entry vào self.view để logic truy cập
        self.debt_entries = {}
        
        fields = [
            ("Mã Hóa Đơn:", "ma_hd"), 
            ("Khách Hàng:", "khach_hang"),
            ("Tổng Tiền:", "tong_tien"), 
            ("Đã Trả:", "da_tra"), 
            ("Còn Nợ:", "con_no")
        ]
        
        # Tạo các entry readonly
        for i, (text, key) in enumerate(fields):
            tk.Label(detail_frame, text=text, font=("Arial", 11), bg="white").grid(row=i, column=0, sticky="w", padx=10, pady=5)
            entry = tk.Entry(detail_frame, font=("Arial", 11, "bold"), width=30, state="readonly", readonlybackground="#eee")
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.debt_entries[key] = entry
            
        # --- KHUNG THANH TOÁN (BÊN PHẢI KHUNG CHI TIẾT) ---
        pay_frame = tk.Frame(detail_frame, bg="white")
        pay_frame.grid(row=0, column=2, rowspan=5, sticky="ns", padx=20)
        
        tk.Label(pay_frame, text="Nhập số tiền trả:", font=("Arial", 11, "bold"), bg="white").pack(pady=(5,0))
        
        # Đăng ký hàm validate
        vcmd = (self.window.register(self._validate_payment_input), '%P')
        
        self.debt_payment_entry = tk.Entry(
            pay_frame, 
            font=("Arial", 14, "bold"), 
            width=20, 
            justify="right", 
            fg="#006400",
            validate='key', # Bật validate
            validatecommand=vcmd # Gọi hàm validate
        )
        self.debt_payment_entry.pack(pady=5)
        
        tk.Button(
            pay_frame,
            text="💳 THANH TOÁN NỢ",
            font=("Arial", 11, "bold"),
            bg="#007bff",
            fg="white",
            command=self.invoice_logic.process_debt_payment # Sẽ tạo ở bước 2
        ).pack(pady=10, fill=tk.X)
        
        tk.Button(
            pay_frame,
            text="🔄 Làm mới",
            font=("Arial", 11),
            bg="#6c757d",
            fg="white",
            command=self.invoice_logic.clear_debt_details # Sẽ tạo ở bước 2
        ).pack(fill=tk.X)

        # Tải dữ liệu ban đầu
        self.invoice_logic.load_debt_list()
        self.invoice_logic.clear_debt_details() # Xóa trắng khung chi tiết
# --- TOÀN BỘ LOGIC ĐÃ BỊ XÓA KHỎI FILE NÀY ---