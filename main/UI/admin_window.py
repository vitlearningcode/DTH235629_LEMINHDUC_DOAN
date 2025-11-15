# =================================================================
# FILE: admin_window.py
# MÔ TẢ: Class Admin - Giao diện quản trị (ĐÃ DỌN DẸP)
# =================================================================

import tkinter as tk
from tkinter import messagebox, ttk
from database_connection import DatabaseConnection
from datetime import datetime, date

# --- IMPORT TẤT CẢ CÁC LỚP LOGIC ---
from Function.function_Admin.admin_dashboard_logic import AdminDashboardLogic
from Function.function_Admin.admin_employee_logic import AdminEmployeeLogic
from Function.function_Admin.admin_product_logic import AdminProductLogic
from Function.function_Admin.admin_part_logic import AdminPartLogic
from Function.function_Admin.admin_customer_logic import AdminCustomerLogic
from Function.function_Admin.admin_invoice_logic import AdminInvoiceLogic
from Function.function_Admin.admin_promotion_logic import AdminPromotionLogic
from Function.function_Admin.admin_reports_logic import AdminReportsLogic
from Function.function_Admin.admin_system_logic import AdminSystemLogic
#-------------------------------------------------------------------------
# imoport mới đưa vào ở đây hieu
from Function.function_Admin.admin_warehouse_logic import AdminWarehouseLogic
#-------------------------------------------------------------------------
from Function.function_Admin.admin_attendance_logic import AdminAttendanceLogic
#-------------------------------------------------------------------------
from Function.function_Admin.admin_warranty_logic import AdminWarrantyLogic
# --- KHÔNG CẦN IMPORT LOGIN TẠI ĐÂY ---

class Admin:
    def __init__(self, user_info):
        """Khởi tạo cửa sổ Admin"""
        self.window = tk.Tk()
        self.window.title(f"ADMIN - {user_info['HoTen']}")
        self.window.geometry("1200x700")
        self.window.state('zoomed')
        
        self.user_info = user_info
        
        # Màu sắc
        self.bg_color = "#E6F2FF"
        self.menu_color = "#4682B4"
        self.btn_color = "#5F9EA0"
        self.text_color = "#FFFFFF"
        
        # Database
        self.db = DatabaseConnection()
        self.db.connect()
        
        # --- KHỞI TẠO TẤT CẢ LOGIC HELPER ---
        self.dashboard_logic = AdminDashboardLogic(self)
        self.emp_logic = AdminEmployeeLogic(self)
        self.prod_logic = AdminProductLogic(self)
        self.part_logic = AdminPartLogic(self)
        self.cust_logic = AdminCustomerLogic(self)
        self.invoice_logic = AdminInvoiceLogic(self)
        self.promo_logic = AdminPromotionLogic(self)
        self.report_logic = AdminReportsLogic(self)
        self.system_logic = AdminSystemLogic(self)
        #-------------------------------------------------------------------------
        # dòng mới đc hieu thêm vào
        self.warehouse_logic = AdminWarehouseLogic(self)
        #-------------------------------------------------------------------------
        self.attend_logic = AdminAttendanceLogic(self)
        #-------------------------------------------------------------------------
        self.warranty_logic = AdminWarrantyLogic(self)

        self.setup_ui()
        self.window.protocol("WM_DELETE_WINDOW", self.system_logic.on_closing)
        self.window.mainloop()
    
    def setup_ui(self):
        """Thiết lập giao diện chính (Chỉ UI)"""
        # Header
        header_frame = tk.Frame(self.window, bg=self.menu_color, height=60)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        
        tk.Label(
            header_frame,
            text="HỆ THỐNG QUẢN LÝ CỬA HÀNG XE MÁY - CHỦ CỬA HÀNG",
            font=("Arial", 18, "bold"),
            bg=self.menu_color,
            fg=self.text_color
        ).pack(side=tk.LEFT, padx=20, pady=10)
        
        tk.Label(
            header_frame,
            text=f"Xin chào: {self.user_info['HoTen']}",
            font=("Arial", 12),
            bg=self.menu_color,
            fg=self.text_color
        ).pack(side=tk.RIGHT, padx=20, pady=10)
        
        tk.Button(
            header_frame,
            text="Đăng xuất",
            font=("Arial", 10, "bold"),
            bg="#DC143C",
            fg=self.text_color,
            command=self.system_logic.logout
        ).pack(side=tk.RIGHT, padx=10)
        
        # Menu
        menu_frame = tk.Frame(self.window, bg=self.menu_color, width=250)
        menu_frame.pack(fill=tk.Y, side=tk.LEFT)
        
        # Nội dung
        self.content_frame = tk.Frame(self.window, bg=self.bg_color)
        self.content_frame.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)
        
        self.create_menu(menu_frame)
        self.show_dashboard()
    
    def create_menu(self, parent):
        """Tạo menu điều hướng (Chỉ UI)"""
        menu_items = [
            ("🏠 Trang chủ", self.show_dashboard),
            ("👥 Quản lý nhân viên", self.manage_employees),
            ("🏍️ Quản lý sản phẩm", self.manage_products),
            ("🔧 Quản lý phụ tùng", self.manage_parts),
            ("📦 Quản lý kho", self.manage_warehouse),
            ("🎁 Quản lý khuyến mãi", self.manage_promotions),
            ("👤 Quản lý khách hàng", self.manage_customers),
            ("📄 Quản lý hóa đơn", self.manage_invoices),
            ("⏰ Quản lý chấm công", self.manage_attendance),
            ("🛡️ Quản lý Bảo hành", self.manage_warranty),
            ("📊 Báo cáo thống kê", self.show_reports)
        ]
        
        tk.Label(
            parent,
            text="MENU CHÍNH",
            font=("Arial", 14, "bold"),
            bg=self.menu_color,
            fg=self.text_color
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
        """Xóa nội dung frame chính"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    # =================================================================
    # CÁC HÀM VẼ GIAO DIỆN (UI-DRAWING METHODS)
    # =================================================================
    
    def show_dashboard(self):
        """Hiển thị trang chủ (Chỉ UI)"""
        self.clear_content()
        
        tk.Label(
            self.content_frame,
            text="TRANG CHỦ ADMIN",
            font=("Arial", 20, "bold"),
            bg=self.bg_color,
            fg="#003366"
        ).pack(pady=20)
        
        stats_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        stats_frame.pack(pady=20)
        
        stats = self.dashboard_logic.get_dashboard_stats()
        
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A"]
        for i, (label, value) in enumerate(stats.items()):
            card = tk.Frame(stats_frame, bg=colors[i % len(colors)], width=250, height=150)
            card.grid(row=i//2, column=i%2, padx=20, pady=20)
            card.pack_propagate(False)
            
            tk.Label(card, text=label, font=("Arial", 12, "bold"), bg=colors[i % len(colors)], fg="white").pack(pady=10)
            tk.Label(card, text=str(value), font=("Arial", 24, "bold"), bg=colors[i % len(colors)], fg="white").pack()
    
    def manage_employees(self):
        """Hiển thị UI Quản lý nhân viên"""
        self.clear_content()
        tk.Label(self.content_frame, text="QUẢN LÝ NHÂN VIÊN", font=("Arial", 18, "bold"), bg=self.bg_color, fg="#003366").pack(pady=10)
        
        btn_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        btn_frame.pack(pady=10)
        
        # Sửa lỗi 'ValueError: not enough values to unpack'
        buttons = [
            ("➕ Thêm nhân viên", "#28a745", self.emp_logic.add_employee),
            ("✏️ Sửa thông tin", "#ffc107", self.emp_logic.edit_employee),
            ("🗑️ Xóa nhân viên", "#dc3545", self.emp_logic.delete_employee),
            ("🔄 Làm mới", "#17a2b8", self.manage_employees) # Thêm màu cho nút này
        ]
        for text, bg, cmd in buttons:
            tk.Button(btn_frame, text=text, font=("Arial", 11), bg=bg, fg="white", command=cmd).pack(side=tk.LEFT, padx=5)
        
        table_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        columns = ("ID", "Tên đăng nhập", "Họ tên", "SĐT", "Email", "Vai trò", "Trạng thái")
        self.employee_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)
        for col in columns: self.employee_tree.heading(col, text=col)
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.employee_tree.yview)
        self.employee_tree.configure(yscrollcommand=scrollbar.set)
        self.employee_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.emp_logic.load_employees()
    
    def manage_products(self):
        """Hiển thị UI Quản lý sản phẩm"""
        self.clear_content()
        tk.Label(self.content_frame, text="QUẢN LÝ SẢN PHẨM", font=("Arial", 18, "bold"), bg=self.bg_color).pack(pady=10)
        
        btn_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="➕ Thêm SP", bg="#28a745", fg="white", command=self.prod_logic.add_product).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="✏️ Sửa SP", bg="#ffc107", fg="white", command=self.prod_logic.edit_product).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🗑️ Xóa SP", bg="#dc3545", fg="white", command=self.prod_logic.delete_product).pack(side=tk.LEFT, padx=5)
        
        columns = ("Mã", "Tên SP", "Hãng", "Loại", "Màu", "Giá bán", "Tồn kho", "Trạng thái")
        self.product_tree = ttk.Treeview(self.content_frame, columns=columns, show="headings")
        for col in columns: self.product_tree.heading(col, text=col)
        self.product_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.prod_logic.load_products()

    def manage_parts(self):
        """Hiển thị UI Quản lý phụ tùng"""
        self.clear_content()
        tk.Label(self.content_frame, text="QUẢN LÝ PHỤ TÙNG", font=("Arial", 18, "bold"), bg=self.bg_color).pack(pady=10)
        
        btn_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="➕ Thêm", bg="#28a745", fg="white", command=self.part_logic.add_part).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="✏️ Sửa", bg="#ffc107", fg="white", command=self.part_logic.edit_part).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🗑️ Xóa", bg="#dc3545", fg="white", command=self.part_logic.delete_part).pack(side=tk.LEFT, padx=5)
        
        columns = ("Mã", "Tên phụ tùng", "Loại", "Đơn vị", "Giá nhập", "Giá bán", "Tồn kho")
        self.part_tree = ttk.Treeview(self.content_frame, columns=columns, show="headings", height=25)
        for col in columns: self.part_tree.heading(col, text=col)
        self.part_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.part_logic.load_parts()



    def manage_warehouse(self):
        """Hiển thị UI Quản lý Kho (Phiếu Nhập)"""
        self.clear_content()
        tk.Label(self.content_frame, text="QUẢN LÝ KHO - PHIẾU NHẬP", 
                 font=("Arial", 18, "bold"), bg=self.bg_color, fg="#003366").pack(pady=10)
        
        btn_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        btn_frame.pack(pady=10)
        
        # Sử dụng self.warehouse_logic (đã khởi tạo trong __init__)
        buttons = [
            ("➕ Tạo Phiếu Nhập Mới", "#28a745", self.warehouse_logic.add_phieu_nhap),
            ("🔍 Xem Chi Tiết", "#007bff", self.warehouse_logic.view_chi_tiet),
            ("✅ Xác Nhận Phiếu", "#218838", self.warehouse_logic.confirm_phieu_nhap), 
            
            # NÚT MỚI: HỦY PHIẾU
            ("⚠️ Hủy Phiếu", "#ffc107", self.warehouse_logic.cancel_phieu_nhap),
            ("🗑️ Xóa Phiếu Nhập", "#dc3545", self.warehouse_logic.delete_phieu_nhap),
            ("🔄 Tải lại", "#17a2b8", self.manage_warehouse) 
        ]
        
        for text, bg, cmd in buttons:
            tk.Button(btn_frame, text=text, font=("Arial", 11), bg=bg, fg="white", command=cmd, width=20).pack(side=tk.LEFT, padx=5)
        
        table_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        columns = ("Mã Phiếu", "Nhà Cung Cấp", "Người Nhập", "Ngày Nhập", "Tổng Tiền", "Trạng Thái")
        
        # Tạo Treeview và gán vào self.view (chính là self của admin_window)
        # Bằng cách này, file logic có thể truy cập qua self.view.phieu_nhap_tree
        self.phieu_nhap_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=25)
        
        widths = {"Mã Phiếu": 80, "Nhà Cung Cấp": 250, "Người Nhập": 200, "Ngày Nhập": 150, "Tổng Tiền": 120, "Trạng Thái": 100}
        
        for col in columns: 
            self.phieu_nhap_tree.heading(col, text=col)
            self.phieu_nhap_tree.column(col, width=widths[col], anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.phieu_nhap_tree.yview)
        self.phieu_nhap_tree.configure(yscrollcommand=scrollbar.set)
        
        self.phieu_nhap_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Tải dữ liệu ban đầu
        self.warehouse_logic.load_phieu_nhap()



    # Mở file: main/UI/admin_window.py
# THAY THẾ toàn bộ hàm manage_customers CŨ bằng hàm MỚI này:

    def manage_customers(self):
        """Hiển thị UI Quản lý khách hàng"""
        self.clear_content()
        tk.Label(self.content_frame, text="QUẢN LÝ KHÁCH HÀNG", font=("Arial", 18, "bold"), bg=self.bg_color, fg="#003366").pack(pady=10)
        
        # --- KHUNG CHỨC NĂNG (TÌM KIẾM + NÚT BẤM) ---
        func_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        func_frame.pack(pady=10, fill=tk.X, padx=20)
        
        tk.Label(func_frame, text="Tìm kiếm (theo Tên hoặc SĐT):", bg=self.bg_color, font=("Arial", 11)).pack(side=tk.LEFT, padx=(0, 5))
        
        search_entry = tk.Entry(func_frame, font=("Arial", 11), width=25)
        search_entry.pack(side=tk.LEFT, padx=5, ipady=4)
        
        # Nút Tìm kiếm (gọi load_customers với từ khóa)
        tk.Button(
            func_frame, text="🔍 Tìm", font=("Arial", 10, "bold"), bg=self.btn_color, fg="white", 
            command=lambda: self.cust_logic.load_customers(search_entry.get())
        ).pack(side=tk.LEFT, padx=5, ipady=4)
        
        # Nút Làm mới (gọi load_customers không có từ khóa)
        tk.Button(
            func_frame, text="🔄 Làm mới", font=("Arial", 10, "bold"), bg="#17a2b8", fg="white",
            command=lambda: (search_entry.delete(0, tk.END), self.cust_logic.load_customers())
        ).pack(side=tk.LEFT, padx=5, ipady=4)
        
        # Các nút nghiệp vụ
        tk.Button(
            func_frame, text="➕ Thêm Khách Hàng", font=("Arial", 10, "bold"), bg="#28a745", fg="white", 
            command=self.cust_logic.add_customer
        ).pack(side=tk.LEFT, padx=(20, 5), ipady=4)
        
        tk.Button(
            func_frame, text="✏️ Sửa Thông Tin", font=("Arial", 10, "bold"), bg="#ffc107", fg="white",
            command=self.cust_logic.edit_customer
        ).pack(side=tk.LEFT, padx=5, ipady=4)
        
        tk.Button(
            func_frame, text="🗑️ Xóa Khách Hàng", font=("Arial", 10, "bold"), bg="#dc3545", fg="white",
            command=self.cust_logic.delete_customer
        ).pack(side=tk.LEFT, padx=5, ipady=4)

        # --- KHUNG HIỂN THỊ DANH SÁCH ---
        table_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        columns = ("Mã", "Họ tên", "SĐT", "Email", "Địa chỉ", "Loại KH", "Ngày tạo")
        self.customer_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=22)
        
        self.customer_tree.heading("Mã", text="Mã")
        self.customer_tree.column("Mã", width=50, anchor="center")
        self.customer_tree.heading("Họ tên", text="Họ tên")
        self.customer_tree.column("Họ tên", width=200)
        self.customer_tree.heading("SĐT", text="SĐT")
        self.customer_tree.column("SĐT", width=120, anchor="center")
        self.customer_tree.heading("Email", text="Email")
        self.customer_tree.column("Email", width=200)
        self.customer_tree.heading("Địa chỉ", text="Địa chỉ")
        self.customer_tree.column("Địa chỉ", width=250)
        self.customer_tree.heading("Loại KH", text="Loại KH")
        self.customer_tree.column("Loại KH", width=100, anchor="center")
        self.customer_tree.heading("Ngày tạo", text="Ngày tạo")
        self.customer_tree.column("Ngày tạo", width=120, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.customer_tree.yview)
        self.customer_tree.configure(yscrollcommand=scrollbar.set)
        
        self.customer_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.cust_logic.load_customers() # Tải dữ liệu ban đầu

    def manage_invoices(self):
        """Hiển thị UI Quản lý hóa đơn"""
        self.clear_content()
        tk.Label(self.content_frame, text="QUẢN LÝ HÓA ĐƠN", font=("Arial", 18, "bold"), bg=self.bg_color, fg="#003366").pack(pady=10)

        # --- KHUNG NÚT BẤM ---
        btn_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        btn_frame.pack(pady=10, fill=tk.X, padx=20)
        
        tk.Button(
            btn_frame, text="🔍 Xem Chi Tiết", font=("Arial", 11, "bold"), bg="#007bff", fg="white", 
            command=self.invoice_logic.show_invoice_details, # <-- Logic mới sẽ được thêm
            width=20, height=2
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            btn_frame, text="🔄 Tải lại", font=("Arial", 11, "bold"), bg="#17a2b8", fg="white",
            command=self.manage_invoices, # Tải lại chính nó
            width=20, height=2
        ).pack(side=tk.LEFT, padx=10)

        # --- KHUNG HIỂN THỊ DANH SÁCH ---
        table_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        columns = ("Mã HĐ", "Khách hàng", "Nhân viên", "Ngày lập", "Tổng tiền", "Thanh toán", "Còn nợ", "Trạng thái")
        self.invoice_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)
        
        # Định dạng cột
        self.invoice_tree.heading("Mã HĐ", text="Mã HĐ")
        self.invoice_tree.column("Mã HĐ", width=60, anchor="center")
        self.invoice_tree.heading("Khách hàng", text="Khách hàng")
        self.invoice_tree.column("Khách hàng", width=200)
        self.invoice_tree.heading("Nhân viên", text="Nhân viên")
        self.invoice_tree.column("Nhân viên", width=200)
        self.invoice_tree.heading("Ngày lập", text="Ngày lập")
        self.invoice_tree.column("Ngày lập", width=130, anchor="center")
        self.invoice_tree.heading("Tổng tiền", text="Tổng tiền")
        self.invoice_tree.column("Tổng tiền", width=120, anchor="e")
        self.invoice_tree.heading("Thanh toán", text="Thanh toán")
        self.invoice_tree.column("Thanh toán", width=120, anchor="e")
        self.invoice_tree.heading("Còn nợ", text="Còn nợ")
        self.invoice_tree.column("Còn nợ", width=100, anchor="e")
        self.invoice_tree.heading("Trạng thái", text="Trạng thái")
        self.invoice_tree.column("Trạng thái", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.invoice_tree.yview)
        self.invoice_tree.configure(yscrollcommand=scrollbar.set)
        
        self.invoice_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Thêm sự kiện double-click
        self.invoice_tree.bind("<Double-1>", lambda e: self.invoice_logic.show_invoice_details())
        
        self.invoice_logic.load_invoices()

    def manage_promotions(self):
        """Hiển thị UI Quản lý khuyến mãi"""
        self.clear_content()
        tk.Label(self.content_frame, text="QUẢN LÝ KHUYẾN MÃI", font=("Arial", 18, "bold"), bg=self.bg_color, fg="#003366").pack(pady=10)
        
        # --- THÊM KHUNG NÚT BẤM ---
        btn_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        btn_frame.pack(pady=10)
        
        buttons = [
            ("➕ Thêm khuyến mãi", "#28a745", self.promo_logic.add_promotion),
            ("✏️ Sửa khuyến mãi", "#ffc107", self.promo_logic.edit_promotion),
            ("🗑️ Xóa khuyến mãi", "#dc3545", self.promo_logic.delete_promotion)
        ]
        
        for text, bg, cmd in buttons:
            tk.Button(btn_frame, text=text, font=("Arial", 11), bg=bg, fg="white", command=cmd, width=20).pack(side=tk.LEFT, padx=10)
        
        # --- KHUNG HIỂN THỊ DANH SÁCH ---
        table_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        columns = ("Mã", "Tên chương trình", "Loại", "Giá trị", "Từ ngày", "Đến ngày", "Trạng thái")
        self.promo_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=22)
        
        # Định dạng các cột
        self.promo_tree.heading("Mã", text="Mã")
        self.promo_tree.column("Mã", width=50, anchor="center")
        
        self.promo_tree.heading("Tên chương trình", text="Tên chương trình")
        self.promo_tree.column("Tên chương trình", width=300)
        
        self.promo_tree.heading("Loại", text="Loại")
        self.promo_tree.column("Loại", width=100, anchor="center")
        
        self.promo_tree.heading("Giá trị", text="Giá trị")
        self.promo_tree.column("Giá trị", width=120, anchor="e")
        
        self.promo_tree.heading("Từ ngày", text="Từ ngày")
        self.promo_tree.column("Từ ngày", width=100, anchor="center")
        
        self.promo_tree.heading("Đến ngày", text="Đến ngày")
        self.promo_tree.column("Đến ngày", width=100, anchor="center")
        
        self.promo_tree.heading("Trạng thái", text="Trạng thái")
        self.promo_tree.column("Trạng thái", width=100, anchor="center")

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.promo_tree.yview)
        self.promo_tree.configure(yscrollcommand=scrollbar.set)
        
        self.promo_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.promo_logic.load_promotions() # Tải dữ liệu

    # Mở file: main/UI/admin_window.py
# THAY THẾ toàn bộ hàm manage_attendance CŨ bằng hàm MỚI này:

    def manage_attendance(self):
        """Vẽ UI Chấm công nhân viên (Chức năng logic chính)"""
        self.clear_content()
        
        tk.Label(
            self.content_frame,
            text="CHẤM CÔNG NHÂN VIÊN",
            font=("Arial", 18, "bold"), 
            bg=self.bg_color, 
            fg="#003366"
        ).pack(pady=(0, 10))
        
        date_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        date_frame.pack(pady=10, fill=tk.X, padx=20)
        
        tk.Label(
            date_frame,
            text="Ngày chấm công (YYYY-MM-DD):",
            font=("Arial", 11),
            bg=self.bg_color
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.date_var = tk.StringVar(value=date.today().strftime('%Y-%m-%d'))
        date_entry = tk.Entry(
            date_frame, 
            textvariable=self.date_var, 
            font=("Arial", 11), 
            width=15
        )
        date_entry.pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            date_frame,
            text="Tải dữ liệu",
            font=("Arial", 10, "bold"),
            bg=self.btn_color,
            fg="white",
            command=self.attend_logic.load_attendance, # <-- Đã đổi
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=10, ipady=4)
        
        table_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(10,0), padx=20)
        
        columns = ("ID", "Họ tên", "Giờ vào", "Giờ ra", "Số giờ làm", "Trạng thái")
        self.attendance_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)
        
        tree = self.attendance_tree
        for col in columns:
            tree.heading(col, text=col)
            width = 150 if col == "Họ tên" else 100
            tree.column(col, width=width, anchor="center")
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        btn_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        btn_frame.pack(pady=10)
        
        tk.Button(
            btn_frame,
            text="✓ Chấm công (Thêm/Sửa)",
            font=("Arial", 11, "bold"),
            bg="#28a745",
            fg="white",
            command=self.attend_logic.add_attendance, # <-- Đã đổi
            relief="flat",
            padx=10,
            pady=5,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=5)
        
        self.attend_logic.load_attendance() # Tải dữ liệu ban đầu

    # Mở file: main/UI/admin_window.py
# BỔ SUNG HÀM MỚI NÀY vào gần cuối file (ví dụ: bên trên hàm manage_reports)

    def manage_warranty(self):
        """Vẽ Màn hình Quản lý Bảo hành & Sửa chữa (Admin)"""
        self.clear_content()
        
        tk.Label(
            self.content_frame,
            text="QUẢN LÝ BẢO HÀNH VÀ SỬA CHỮA",
            font=("Arial", 18, "bold"),
            bg=self.bg_color,
            fg="#003366"
        ).pack(pady=10)
        
        # --- KHUNG TÌM KIẾM ---
        search_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        search_frame.pack(pady=10, fill=tk.X, padx=20)
        
        tk.Label(search_frame, text="Tìm (Tên KH, SĐT, Tên Xe):", bg=self.bg_color, font=("Arial", 11)).pack(side=tk.LEFT, padx=(0, 5))
        search_entry = tk.Entry(search_frame, font=("Arial", 11), width=30)
        search_entry.pack(side=tk.LEFT, padx=5, ipady=4)
        
        tk.Button(
            search_frame, text="🔍 Tìm", font=("Arial", 10, "bold"), bg=self.btn_color, fg="white", 
            command=lambda: self.warranty_logic.load_all_warranties(search_entry.get())
        ).pack(side=tk.LEFT, padx=5, ipady=4)
        
        tk.Button(
            search_frame, text="🔄 Tải lại", font=("Arial", 10, "bold"), bg="#17a2b8", fg="white",
            command=lambda: (search_entry.delete(0, tk.END), self.warranty_logic.load_all_warranties())
        ).pack(side=tk.LEFT, padx=5, ipady=4)

        # --- KHUNG NỘI DUNG CHIA ĐÔI ---
        main_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # --- CỘT TRÁI: DANH SÁCH PHIẾU BẢO HÀNH ---
        left_frame = tk.Frame(main_frame, bg=self.bg_color)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        warranty_frame = tk.LabelFrame(left_frame, text="Tất cả Phiếu Bảo Hành", 
                                       font=("Arial", 12, "bold"), bg="white", padx=10, pady=10)
        warranty_frame.pack(fill=tk.BOTH, expand=True)
        
        cols_warranty = ("ID", "Khách Hàng", "SĐT", "Tên Xe", "Từ Ngày", "Đến Ngày", "Trạng Thái")
        self.warranty_tree = ttk.Treeview(warranty_frame, columns=cols_warranty, show="headings", height=15)
        for col in cols_warranty: self.warranty_tree.heading(col, text=col)
        
        self.warranty_tree.column("ID", width=40, anchor="center")
        self.warranty_tree.column("Khách Hàng", width=150)
        self.warranty_tree.column("SĐT", width=100, anchor="center")
        self.warranty_tree.column("Tên Xe", width=150)
        self.warranty_tree.column("Từ Ngày", width=90, anchor="center")
        self.warranty_tree.column("Đến Ngày", width=90, anchor="center")
        self.warranty_tree.column("Trạng Thái", width=90, anchor="center")
        
        self.warranty_tree.bind("<<TreeviewSelect>>", self.warranty_logic.on_warranty_select)
        
        self.warranty_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_left = ttk.Scrollbar(warranty_frame, orient="vertical", command=self.warranty_tree.yview)
        self.warranty_tree.configure(yscrollcommand=scrollbar_left.set)
        scrollbar_left.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Nút xóa Phiếu Bảo Hành
        tk.Button(
            left_frame, text="🗑️ Xóa Phiếu Bảo Hành (Bên trái)", font=("Arial", 10, "bold"), bg="#dc3545", fg="white",
            command=self.warranty_logic.delete_warranty_entry
        ).pack(pady=10)

        # --- CỘT PHẢI: LỊCH SỬ SỬA CHỮA ---
        right_frame = tk.Frame(main_frame, bg=self.bg_color)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        history_frame = tk.LabelFrame(right_frame, text="Lịch Sử Sửa Chữa (của phiếu đã chọn)", 
                                   font=("Arial", 12, "bold"), bg="white", padx=10, pady=10)
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        cols_history = ("ID LS", "Ngày Sửa", "Mô Tả Lỗi", "Người Xử Lý", "Chi Phí", "Trạng Thái")
        self.history_tree = ttk.Treeview(history_frame, columns=cols_history, show="headings", height=15)
        
        self.history_tree.heading("ID LS", text="ID")
        self.history_tree.column("ID LS", width=40, anchor="center")
        self.history_tree.heading("Ngày Sửa", text="Ngày Sửa")
        self.history_tree.column("Ngày Sửa", width=90, anchor="center")
        self.history_tree.heading("Mô Tả Lỗi", text="Mô Tả Lỗi")
        self.history_tree.column("Mô Tả Lỗi", width=200)
        self.history_tree.heading("Người Xử Lý", text="Người Xử Lý")
        self.history_tree.column("Người Xử Lý", width=120)
        self.history_tree.heading("Chi Phí", text="Chi Phí")
        self.history_tree.column("Chi Phí", width=90, anchor="e")
        self.history_tree.heading("Trạng Thái", text="Trạng Thái")
        self.history_tree.column("Trạng Thái", width=90, anchor="center")
        
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_right = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar_right.set)
        scrollbar_right.pack(side=tk.RIGHT, fill=tk.Y)

        # Nút xóa Lịch Sử Sửa Chữa
        tk.Button(
            right_frame, text="🗑️ Xóa Lịch Sử Sửa Chữa (Bên phải)", font=("Arial", 10, "bold"), bg="#ffc107", fg="black",
            command=self.warranty_logic.delete_history_entry
        ).pack(pady=10)
        
        # Tải dữ liệu ban đầu
        self.warranty_logic.load_all_warranties()

    def show_reports(self):
        """Hiển thị UI Báo cáo thống kê"""
        self.clear_content()
        tk.Label(self.content_frame, text="BÁO CÁO THỐNG KÊ", font=("Arial", 18, "bold"), bg=self.bg_color).pack(pady=10)
        
        report_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        report_frame.pack(pady=20)
        
        reports = [
            ("📊 Doanh thu theo tháng", self.report_logic.report_revenue),
            ("📦 Tồn kho sản phẩm", self.report_logic.report_inventory),
            ("👥 Hiệu suất nhân viên", self.report_logic.report_employee_performance),
            ("🏆 Top sản phẩm bán chạy", self.report_logic.report_top_products),
            ("👤 Khách hàng thân thiết", self.report_logic.report_loyal_customers),
            ("💰 Công nợ khách hàng", self.report_logic.report_debt)
        ]
        row, col = 0, 0
        for text, command in reports:
            btn = tk.Button(report_frame, text=text, font=("Arial", 12), bg=self.btn_color, fg="white", width=30, height=3, command=command)
            btn.grid(row=row, column=col, padx=15, pady=15)
            col += 1
            if col > 1: col, row = 0, row + 1