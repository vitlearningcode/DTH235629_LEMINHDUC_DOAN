# =================================================================
# FILE: admin_window.py
# MÔ TẢ: Class Admin - Giao diện quản trị (ĐÃ DỌN DẸP)
# =================================================================

import tkinter as tk
from tkinter import messagebox, ttk
from database_connection import DatabaseConnection
from datetime import datetime

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



    def manage_customers(self):
        """Hiển thị UI Quản lý khách hàng"""
        self.clear_content()
        tk.Label(self.content_frame, text="QUẢN LÝ KHÁCH HÀNG", font=("Arial", 18, "bold"), bg=self.bg_color).pack(pady=10)
        
        search_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        search_frame.pack(pady=10)
        tk.Label(search_frame, text="Tìm kiếm:", bg=self.bg_color).pack(side=tk.LEFT, padx=5)
        search_entry = tk.Entry(search_frame, font=("Arial", 11), width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="🔍 Tìm", bg=self.btn_color, fg="white", command=lambda: self.cust_logic.search_customers(search_entry.get())).pack(side=tk.LEFT, padx=5)
        
        columns = ("Mã", "Họ tên", "SĐT", "Email", "Địa chỉ", "Loại KH", "Ngày tạo")
        self.customer_tree = ttk.Treeview(self.content_frame, columns=columns, show="headings", height=22)
        for col in columns: self.customer_tree.heading(col, text=col)
        self.customer_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.cust_logic.load_customers()

    def manage_invoices(self):
        """Hiển thị UI Quản lý hóa đơn"""
        self.clear_content()
        tk.Label(self.content_frame, text="QUẢN LÝ HÓA ĐƠN", font=("Arial", 18, "bold"), bg=self.bg_color).pack(pady=10)
        
        columns = ("Mã HĐ", "Khách hàng", "Nhân viên", "Ngày lập", "Tổng tiền", "Thanh toán", "Còn nợ", "Trạng thái")
        self.invoice_tree = ttk.Treeview(self.content_frame, columns=columns, show="headings", height=20)
        for col in columns: self.invoice_tree.heading(col, text=col)
        self.invoice_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
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

    def manage_attendance(self):
        """Hiển thị UI Quản lý chấm công (Placeholder)"""
        self.clear_content()
        tk.Label(self.content_frame, text="QUẢN LÝ CHẤM CÔNG (Đang phát triển)", font=("Arial", 18, "bold"), bg=self.bg_color).pack(pady=20)

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