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
        
        # --- BỘ FONT CHỮ (ĐÃ BỔ SUNG ĐỂ SỬA LỖI) ---
        self.font_title = ("Segoe UI", 18, "bold")
        self.font_header = ("Segoe UI", 16, "bold")
        self.font_menu_title = ("Segoe UI", 14, "bold")
        self.font_menu_btn = ("Segoe UI", 11, "bold") 
        self.font_label = ("Segoe UI", 12) 
        self.font_info = ("Segoe UI", 12)
        self.font_button = ("Segoe UI", 10, "bold") # <-- Đây là font bị thiếu
        self.font_card_label = ("Segoe UI", 12, "bold")
        self.font_card_value = ("Segoe UI", 24, "bold")

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
        #-------------------------------------------------------------------------
        self.setup_styles()
        self.setup_ui()
        self.window.protocol("WM_DELETE_WINDOW", self.system_logic.on_closing)
        self.window.mainloop()
    
    def setup_styles(self):
        """Định nghĩa style cho các widget TTK"""
        s = ttk.Style()
        try:
            s.theme_use('vista')
        except tk.TclError:
            pass 

        # Đặt tên style dựa trên màu nền của Admin
        s.configure('Content.TFrame', background=self.bg_color)
        s.configure('Content.TLabel', background=self.bg_color, foreground="#003366", font=("Segoe UI", 16, "bold"))
        s.configure('Menu.TFrame', background=self.menu_color)
        s.configure('Menu.TLabel', background=self.menu_color, foreground=self.text_color, font=("Segoe UI", 14, "bold"))
        
        s.configure('Std.TLabel', background=self.bg_color, font=("Segoe UI", 12))
        s.configure('Card.TFrame', background="white", relief="raised", borderwidth=2)
        s.configure('Func.TButton', font=("Segoe UI", 10, "bold"), padding=5)
        
        # Style cho LabelFrame nền trắng (dùng cho Detail Pane)
        s.configure('Details.TLabelframe', background="white", padding=10)
        s.configure('Details.TLabelframe.Label', background="white", font=("Segoe UI", 12), foreground="#003366")
        
        # Style cho Label bên trong LabelFrame (nền trắng)
        s.configure('Details.TLabel', background="white", font=("Segoe UI", 12))
        
        s.configure("Treeview", 
                    rowheight=28, 
                    font=("Segoe UI", 10),
                    background="white",
                    fieldbackground="white")
        s.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        s.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})]) # Bỏ viền
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
            
    def create_search_bar(self, parent_frame, search_command):
        """Tạo một frame chứa ô tìm kiếm (LIVE SEARCH)"""
        search_frame = ttk.Frame(parent_frame, style='Content.TFrame')
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(
            search_frame, 
            text="Tìm kiếm:", 
            style='Std.TLabel'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        search_entry = ttk.Entry(
            search_frame, 
            font=("Segoe UI", 12), # Sử dụng font chuẩn
            width=40
        )
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Gán sự kiện <KeyRelease> để tìm kiếm live
        search_entry.bind("<KeyRelease>", lambda e: search_command(search_entry.get()))
        return search_entry
            
    
    
    # =================================================================
    # CÁC HÀM VẼ GIAO DIỆN (UI-DRAWING METHODS)
    # =================================================================
    
    def create_search_bar(self, parent_frame, search_command):
        """Tạo một frame chứa ô tìm kiếm (LIVE SEARCH)"""
        search_frame = ttk.Frame(parent_frame, style='Content.TFrame')
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(
            search_frame, 
            text="Tìm kiếm:", 
            style='Std.TLabel'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        search_entry = ttk.Entry(
            search_frame, 
            font=("Segoe UI", 12), # Sử dụng font chuẩn
            width=40
        )
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Gán sự kiện <KeyRelease> để tìm kiếm live
        search_entry.bind("<KeyRelease>", lambda e: search_command(search_entry.get()))
        return search_entry
    
    def show_dashboard(self):
        """Hiển thị trang chủ (Cập nhật: 4 thẻ kích thước bằng nhau tuyệt đối)"""
        self.clear_content()
        
        # 1. Tiêu đề
        tk.Label(
            self.content_frame,
            text="TRANG CHỦ ADMIN",
            font=("Arial", 20, "bold"),
            bg=self.bg_color,
            fg="#003366"
        ).pack(pady=(0, 20))
        
        # 2. Khung chứa thống kê
        stats_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        stats = self.dashboard_logic.get_dashboard_stats()
        
        # 3. Cấu hình lưới (QUAN TRỌNG: Thêm uniform="group_name")
        # uniform="cols": Ép tất cả các cột có cùng tag "cols" phải rộng bằng nhau
        stats_frame.grid_columnconfigure(0, weight=1, uniform="cols")
        stats_frame.grid_columnconfigure(1, weight=1, uniform="cols")
        
        # uniform="rows": Ép tất cả các hàng có cùng tag "rows" phải cao bằng nhau
        stats_frame.grid_rowconfigure(0, weight=1, uniform="rows")
        stats_frame.grid_rowconfigure(1, weight=1, uniform="rows")
        
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A"]
        
        for i, (label, value) in enumerate(stats.items()):
            # Tạo thẻ (Card)
            card = tk.Frame(stats_frame, bg=colors[i % len(colors)], relief="raised", bd=2)
            
            # Đặt vào lưới
            card.grid(row=i//2, column=i%2, padx=20, pady=20, sticky="nsew")
            
            # --- FRAME CON ĐỂ CĂN GIỮA NỘI DUNG ---
            # Frame này chứa chữ và luôn nằm giữa tâm thẻ
            content_frame = tk.Frame(card, bg=colors[i % len(colors)])
            content_frame.place(relx=0.5, rely=0.5, anchor="center")
            
            # Label tiêu đề
            tk.Label(
                content_frame, 
                text=label, 
                font=("Arial", 16, "bold"), 
                bg=colors[i % len(colors)], 
                fg="white"
            ).pack(pady=5)
            
            # Label giá trị
            tk.Label(
                content_frame, 
                text=str(value), 
                font=("Arial", 30, "bold"), 
                bg=colors[i % len(colors)], 
                fg="white"
            ).pack(pady=5)
    
    def manage_employees(self):
        """Hiển thị UI Quản lý nhân viên (ĐÃ NÂNG CẤP VỚI PANEL CHI TIẾT)"""
        self.clear_content()
        
        # --- SỬA LỖI: Dùng tk.Label (thay vì ttk.Label) để nhận 'bg' và 'fg' ---
        tk.Label(
            self.content_frame,
            text="QUẢN LÝ THÔNG TIN NHÂN VIÊN",
            font=("Arial", 18, "bold"), 
            bg=self.bg_color, 
            fg="#003366"
        ).pack(pady=(0, 10))
        
        # --- 1. KHUNG NÚT BẤM CHỨC NĂNG (Thêm, Xóa) ---
        btn_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        btn_frame.pack(pady=5, fill=tk.X, padx=20) # Thêm padx
        
        tk.Button(
            btn_frame, text="➕ Thêm nhân viên", font=("Arial", 11), bg="#28a745", fg="white", 
            command=self.emp_logic.add_employee, cursor="hand2"
        ).pack(side=tk.LEFT, padx=5, ipady=4)
        
        tk.Button(
            btn_frame, text="🗑️ Xóa nhân viên", font=("Arial", 11), bg="#dc3545", fg="white", 
            command=self.emp_logic.delete_employee, cursor="hand2"
        ).pack(side=tk.LEFT, padx=5, ipady=4)
        
        # --- 2. THANH TÌM KIẾM (Live Search) ---
        # Đặt thanh tìm kiếm trong content_frame, có padding
        search_bar_container = tk.Frame(self.content_frame, bg=self.bg_color)
        search_bar_container.pack(fill=tk.X, padx=20)
        self.search_entry = self.create_search_bar(
            search_bar_container, 
            lambda keyword: self.emp_logic.load_view(self.employee_tree, keyword)
        )
        
        # --- 3. KHUNG BẢNG (Treeview) ---
        table_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 10), padx=20) 
        
        columns = ("ID", "Họ tên", "SĐT", "Email", "Vai trò", "Trạng thái")
        self.employee_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        
        tree = self.employee_tree
        tree.heading("ID", text="ID")
        tree.column("ID", width=50, anchor="center")
        tree.heading("Họ tên", text="Họ tên")
        tree.column("Họ tên", width=200, anchor="w")
        tree.heading("SĐT", text="SĐT")
        tree.column("SĐT", width=120, anchor="center")
        tree.heading("Email", text="Email")
        tree.column("Email", width=200, anchor="w")
        tree.heading("Vai trò", text="Vai trò")
        tree.column("Vai trò", width=100, anchor="center")
        tree.heading("Trạng thái", text="Trạng thái")
        tree.column("Trạng thái", width=100, anchor="center")
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree.bind("<<TreeviewSelect>>", self.emp_logic.on_employee_select)

        # --- 4. KHUNG CHI TIẾT (Panel) ---
        details_frame = ttk.LabelFrame(self.content_frame, text="Chi tiết Nhân viên", style='Details.TLabelframe')
        details_frame.pack(fill=tk.X, expand=False, pady=(10, 0), padx=20)

        # 4.1. Cột Ảnh (Bên trái)
        image_frame = ttk.Frame(details_frame, style='Card.TFrame', width=160, height=200)
        image_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 20), pady=10)
        image_frame.pack_propagate(False) 

        upload_button = ttk.Button(
            image_frame, 
            text="Tải ảnh lên", 
            style='Func.TButton', 
            command=self.emp_logic.upload_image, # Gọi logic
            cursor="hand2"
        )
        upload_button.pack(side=tk.BOTTOM, pady=10)
        
        self.image_label = ttk.Label(image_frame, text="Chọn NV", anchor="center", background="lightgrey", relief="groove")
        self.image_label.pack(fill=tk.BOTH, expand=True, side=tk.TOP, pady=5, padx=5)

        # 4.2. Cột Thông tin (Bên phải)
        info_frame = ttk.Frame(details_frame, style='Card.TFrame')
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10, padx=(0, 20))

        self.details_emp_id = ttk.Label(info_frame, text="ID: (Chưa chọn)", style='Details.TLabel', font=("Segoe UI", 12))
        self.details_emp_id.grid(row=0, column=0, columnspan=2, pady=10, sticky="w", padx=10)

        # Cột 1 thông tin
        ttk.Label(info_frame, text="Họ tên:", style='Details.TLabel').grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.details_hoten = ttk.Entry(info_frame, font=("Segoe UI", 12), width=30)
        self.details_hoten.grid(row=1, column=1, pady=5, sticky="ew")
        
        ttk.Label(info_frame, text="SĐT:", style='Details.TLabel').grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.details_sdt = ttk.Entry(info_frame, font=("Segoe UI", 12), width=30)
        self.details_sdt.grid(row=2, column=1, pady=5, sticky="ew")

        ttk.Label(info_frame, text="Email:", style='Details.TLabel').grid(row=3, column=0, sticky="e", padx=10, pady=5)
        self.details_email = ttk.Entry(info_frame, font=("Segoe UI", 12), width=30)
        self.details_email.grid(row=3, column=1, pady=5, sticky="ew")

        # Cột 2 thông tin
        ttk.Label(info_frame, text="Vai trò:", style='Details.TLabel').grid(row=1, column=2, sticky="e", padx=10, pady=5)
        self.details_vaitro = ttk.Combobox(info_frame, values=["Admin", "QuanLy", "NhanVien"], state="readonly", font=("Segoe UI", 12), width=20)
        self.details_vaitro.grid(row=1, column=3, pady=5, padx=10, sticky="ew")
        
        ttk.Label(info_frame, text="Trạng thái:", style='Details.TLabel').grid(row=2, column=2, sticky="e", padx=10, pady=5)
        self.details_trangthai = ttk.Combobox(info_frame, values=["HoatDong", "KhongHoatDong"], state="readonly", font=("Segoe UI", 12), width=20)
        self.details_trangthai.grid(row=2, column=3, pady=5, padx=10, sticky="ew")

        # Nút Cập nhật
        self.update_button = tk.Button(
            info_frame,
            text="CẬP NHẬT",
            font=("Arial", 10, "bold"),
            bg="#007bff",
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            command=self.emp_logic.update_employee, # Gọi logic
            state="disabled",
            cursor=""
        )
        self.update_button.grid(row=3, column=3, pady=10, padx=10, sticky="se")

        # Cấu hình grid co dãn
        info_frame.grid_columnconfigure(1, weight=1)
        info_frame.grid_columnconfigure(3, weight=1)

        # Gán sự kiện thay đổi
        self.details_hoten.bind("<KeyRelease>", self.emp_logic.check_for_changes)
        self.details_sdt.bind("<KeyRelease>", self.emp_logic.check_for_changes)
        self.details_email.bind("<KeyRelease>", self.emp_logic.check_for_changes)
        self.details_vaitro.bind("<<ComboboxSelected>>", self.emp_logic.check_for_changes)
        self.details_trangthai.bind("<<ComboboxSelected>>", self.emp_logic.check_for_changes)
        
        # Tải dữ liệu lần đầu
        self.emp_logic.load_view(self.employee_tree)
    
    def manage_products(self):
        """Hiển thị UI Quản lý sản phẩm (NÂNG CẤP VỚI PANEL CHI TIẾT)"""
        self.clear_content()
        
        ttk.Label(
            self.content_frame,
            text="QUẢN LÝ THÔNG TIN SẢN PHẨM",
            style='Content.TLabel'
        ).pack(pady=(0, 10))
        
        # --- 1. KHUNG NÚT BẤM CHỨC NĂNG (Giữ lại của Admin) ---
        btn_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
        btn_frame.pack(pady=5, fill=tk.X)
        
        tk.Button(
            btn_frame, text="➕ Thêm SP", font=self.font_button, bg="#28a745", fg="white", 
            command=self.prod_logic.add_product, cursor="hand2"
        ).pack(side=tk.LEFT, padx=5, ipady=4)
        
        # Nút "Sửa" bị loại bỏ, vì đã có nút "CẬP NHẬT" trong panel
        
        tk.Button(
            btn_frame, text="🗑️ Xóa SP", font=self.font_button, bg="#dc3545", fg="white", 
            command=self.prod_logic.delete_product, cursor="hand2"
        ).pack(side=tk.LEFT, padx=5, ipady=4)
        
        # --- 2. THANH TÌM KIẾM (Lấy từ quanly_window) ---
        self.search_entry = self.create_search_bar(
            self.content_frame,
            lambda keyword: self.prod_logic.load_products(self.product_tree, keyword) # Sửa tên hàm logic
        )

        # --- 3. KHUNG BẢNG (Treeview) ---
        table_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 10))
        
        # Cập nhật cột để giống hệt file quanly_window
        columns = ("Mã SP", "Tên SP", "Hãng", "Loại", "Giá bán", "Tồn kho")
        self.product_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        
        tree = self.product_tree
        tree.heading("Mã SP", text="Mã SP")
        tree.column("Mã SP", width=50, anchor="center")
        tree.heading("Tên SP", text="Tên SP")
        tree.column("Tên SP", width=250, anchor="w") # Tăng chiều rộng
        tree.heading("Hãng", text="Hãng")
        tree.column("Hãng", width=100, anchor="center")
        tree.heading("Loại", text="Loại")
        tree.column("Loại", width=100, anchor="center")
        tree.heading("Giá bán", text="Giá bán")
        tree.column("Giá bán", width=120, anchor="e")
        tree.heading("Tồn kho", text="Tồn kho")
        tree.column("Tồn kho", width=80, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Sửa sự kiện bind thành <ButtonRelease-1> và gọi logic của Admin
        tree.bind("<ButtonRelease-1>", self.prod_logic.on_product_select)
        
        # --- 4. KHUNG CHI TIẾT (Panel) ---
        details_frame = ttk.LabelFrame(self.content_frame, text="Chi tiết Sản phẩm", style='Details.TLabelframe')
        details_frame.pack(fill=tk.X, expand=False, pady=(10, 0))

        # Cột trái: ảnh sản phẩm
        image_frame = ttk.Frame(details_frame, style='Card.TFrame', width=160, height=200)
        image_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 20), pady=10)
        image_frame.pack_propagate(False)
        upload_button = ttk.Button(
            image_frame, text="Tải ảnh lên", style='Func.TButton',
            command=self.prod_logic.upload_image, cursor="hand2"
        )
        upload_button.pack(side=tk.BOTTOM, pady=10)
        self.product_image_label = ttk.Label(
            image_frame, text="Chọn SP", anchor="center", background="lightgrey", relief="groove")
        self.product_image_label.pack(fill=tk.BOTH, expand=True, side=tk.TOP, pady=5, padx=5)

        # Cột phải: các trường thông tin
        info_frame = ttk.Frame(details_frame, style='Card.TFrame')
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10, padx=(0, 20))

        self.details_product_id = ttk.Label(info_frame, text="Mã: (Chưa chọn)", style='Details.TLabel', font=self.font_label)
        self.details_product_id.grid(row=0, column=0, pady=10, sticky="w", padx=10)

        # Tên sản phẩm
        ttk.Label(info_frame, text="Tên SP:", style='Details.TLabel').grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.details_name = ttk.Entry(info_frame, font=self.font_label, width=30)
        self.details_name.grid(row=1, column=1, pady=5, sticky="ew")

        # Giá bán
        ttk.Label(info_frame, text="Giá bán:", style='Details.TLabel').grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.details_price = ttk.Entry(info_frame, font=self.font_label, width=30)
        self.details_price.grid(row=2, column=1, pady=5, sticky="ew")

        # Tồn kho
        ttk.Label(info_frame, text="Tồn kho:", style='Details.TLabel').grid(row=3, column=0, sticky="e", padx=10, pady=5)
        self.details_stock = ttk.Entry(info_frame, font=self.font_label, width=30)
        self.details_stock.grid(row=3, column=1, pady=5, sticky="ew")

        # Hãng xe (Cần logic load_products để lấy danh sách hãng)
        ttk.Label(info_frame, text="Hãng:", style='Details.TLabel').grid(row=1, column=2, sticky="e", padx=10, pady=5)
        self.details_hang = ttk.Combobox(info_frame, values=[], state="readonly", font=self.font_label, width=20)
        self.details_hang.grid(row=1, column=3, pady=5, padx=10, sticky="ew")

        # Loại xe (Cần logic load_products để lấy danh sách loại)
        ttk.Label(info_frame, text="Loại:", style='Details.TLabel').grid(row=2, column=2, sticky="e", padx=10, pady=5)
        self.details_loai = ttk.Combobox(info_frame, values=[], state="readonly", font=self.font_label, width=20)
        self.details_loai.grid(row=2, column=3, pady=5, padx=10, sticky="ew")

        # Nút cập nhật
        self.update_button = tk.Button(
            info_frame, text="CẬP NHẬT", font=self.font_button, bg="#007bff", fg="white",
            relief="flat", padx=20, pady=10, command=self.prod_logic.update_product, state="disabled", cursor=""
        )
        self.update_button.grid(row=3, column=3, pady=10, padx=10, sticky="e")

        info_frame.grid_columnconfigure(1, weight=1)
        info_frame.grid_columnconfigure(3, weight=1)

        # Bind sự kiện
        self.details_name.bind("<KeyRelease>", self.prod_logic.check_for_changes)
        self.details_price.bind("<KeyRelease>", self.prod_logic.check_for_changes)
        self.details_stock.bind("<KeyRelease>", self.prod_logic.check_for_changes)
        self.details_hang.bind("<<ComboboxSelected>>", self.prod_logic.check_for_changes)
        self.details_loai.bind("<<ComboboxSelected>>", self.prod_logic.check_for_changes)

        # Tải dữ liệu ban đầu
        self.prod_logic.load_products(tree)
        
    def manage_parts(self):
        """Hiển thị UI Quản lý phụ tùng (NÂNG CẤP VỚI PANEL CHI TIẾT)"""
        self.clear_content()
        
        ttk.Label(
            self.content_frame,
            text="QUẢN LÝ THÔNG TIN PHỤ TÙNG",
            style='Content.TLabel'
        ).pack(pady=(0, 10))

        # --- 1. KHUNG NÚT BẤM CHỨC NĂNG (Giữ lại của Admin) ---
        btn_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
        btn_frame.pack(pady=5, fill=tk.X)
        
        tk.Button(
            btn_frame, text="➕ Thêm PT", font=self.font_button, bg="#28a745", fg="white", 
            command=self.part_logic.add_part, cursor="hand2"
        ).pack(side=tk.LEFT, padx=5, ipady=4)
        
        tk.Button(
            btn_frame, text="🗑️ Xóa PT", font=self.font_button, bg="#dc3545", fg="white", 
            command=self.part_logic.delete_part, cursor="hand2"
        ).pack(side=tk.LEFT, padx=5, ipady=4)
        
        # --- 2. THANH TÌM KIẾM (Lấy từ quanly_window) ---
        self.search_entry = self.create_search_bar(
            self.content_frame,
            lambda keyword: self.part_logic.load_parts(self.part_tree, keyword) # Sửa tên hàm logic
        )

        # --- 3. KHUNG BẢNG (Treeview) ---
        table_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 10))
        
        # Cập nhật cột để giống hệt file quanly_window
        columns = ("Mã PT", "Tên PT", "Loại", "Giá bán", "Tồn kho")
        self.part_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        
        tree = self.part_tree
        tree.heading("Mã PT", text="Mã PT")
        tree.column("Mã PT", width=50, anchor="center")
        tree.heading("Tên PT", text="Tên PT")
        tree.column("Tên PT", width=250, anchor="w")
        tree.heading("Loại", text="Loại")
        tree.column("Loại", width=120, anchor="center")
        tree.heading("Giá bán", text="Giá bán")
        tree.column("Giá bán", width=120, anchor="e")
        tree.heading("Tồn kho", text="Tồn kho")
        tree.column("Tồn kho", width=80, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree.bind("<ButtonRelease-1>", self.part_logic.on_part_select)
        
        # --- 4. KHUNG CHI TIẾT (Panel) ---
        details_frame = ttk.LabelFrame(self.content_frame, text="Chi tiết Phụ tùng", style='Details.TLabelframe')
        details_frame.pack(fill=tk.X, expand=False, pady=(10, 0))

        # Cột trái: ảnh
        image_frame = ttk.Frame(details_frame, style='Card.TFrame', width=160, height=200)
        image_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 20), pady=10)
        image_frame.pack_propagate(False)
        upload_button = ttk.Button(
            image_frame, text="Tải ảnh lên", style='Func.TButton',
            command=self.part_logic.upload_image, cursor="hand2"
        )
        upload_button.pack(side=tk.BOTTOM, pady=10)
        self.part_image_label = ttk.Label(
            image_frame, text="Chọn PT", anchor="center", background="lightgrey", relief="groove")
        self.part_image_label.pack(fill=tk.BOTH, expand=True, side=tk.TOP, pady=5, padx=5)

        # Cột phải: thông tin
        info_frame = ttk.Frame(details_frame, style='Card.TFrame')
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10, padx=(0, 20))

        self.details_part_id = ttk.Label(info_frame, text="Mã: (Chưa chọn)", style='Details.TLabel', font=self.font_label)
        self.details_part_id.grid(row=0, column=0, pady=10, sticky="w", padx=10)

        # Tên PT
        ttk.Label(info_frame, text="Tên PT:", style='Details.TLabel').grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.details_name = ttk.Entry(info_frame, font=self.font_label, width=30)
        self.details_name.grid(row=1, column=1, pady=5, sticky="ew")

        # Giá bán
        ttk.Label(info_frame, text="Giá bán:", style='Details.TLabel').grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.details_price = ttk.Entry(info_frame, font=self.font_label, width=30)
        self.details_price.grid(row=2, column=1, pady=5, sticky="ew")

        # Tồn kho
        ttk.Label(info_frame, text="Tồn kho:", style='Details.TLabel').grid(row=3, column=0, sticky="e", padx=10, pady=5)
        self.details_stock = ttk.Entry(info_frame, font=self.font_label, width=30)
        self.details_stock.grid(row=3, column=1, pady=5, sticky="ew")

        # Loại phụ tùng
        ttk.Label(info_frame, text="Loại:", style='Details.TLabel').grid(row=1, column=2, sticky="e", padx=10, pady=5)
        self.details_loai = ttk.Combobox(
            info_frame, values=[], state="readonly", font=self.font_label, width=20)
        self.details_loai.grid(row=1, column=3, pady=5, padx=10, sticky="ew")

        # Nút cập nhật
        self.update_button = tk.Button(
            info_frame, text="CẬP NHẬT", font=self.font_button, bg="#007bff", fg="white",
            relief="flat", padx=20, pady=10, command=self.part_logic.update_part, state="disabled", cursor=""
        )
        self.update_button.grid(row=3, column=3, pady=10, padx=10, sticky="e")

        info_frame.grid_columnconfigure(1, weight=1)
        info_frame.grid_columnconfigure(3, weight=1)

        # Bind sự kiện
        self.details_name.bind("<KeyRelease>", self.part_logic.check_for_changes)
        self.details_price.bind("<KeyRelease>", self.part_logic.check_for_changes)
        self.details_stock.bind("<KeyRelease>", self.part_logic.check_for_changes)
        self.details_loai.bind("<<ComboboxSelected>>", self.part_logic.check_for_changes)

        # Tải dữ liệu ban đầu
        self.part_logic.load_parts(tree)



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

   # FILE: main/UI/admin_window.py

    def manage_invoices(self):
        """Hiển thị UI Quản lý hóa đơn"""
        self.clear_content()
        tk.Label(self.content_frame, text="QUẢN LÝ HÓA ĐƠN", font=("Arial", 18, "bold"), bg=self.bg_color, fg="#003366").pack(pady=10)

        # --- KHUNG CHỨC NĂNG (TÌM KIẾM & NÚT) ---
        func_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        func_frame.pack(pady=10, fill=tk.X, padx=20)

        # Ô tìm kiếm
        tk.Label(func_frame, text="Tìm kiếm (Tên KH hoặc Mã HĐ):", bg=self.bg_color, font=("Arial", 11)).pack(side=tk.LEFT, padx=(0, 5))
        search_entry = tk.Entry(func_frame, font=("Arial", 11), width=30)
        search_entry.pack(side=tk.LEFT, padx=5, ipady=4)

        # Nút Tìm kiếm [MỚI]
        tk.Button(
            func_frame, text="🔍 Tìm", font=("Arial", 10, "bold"), bg=self.btn_color, fg="white", 
            command=lambda: self.invoice_logic.load_invoices(search_entry.get())
        ).pack(side=tk.LEFT, padx=5, ipady=4)

        # Nút Làm mới [CẬP NHẬT]
        tk.Button(
            func_frame, text="🔄 Tải lại", font=("Arial", 10, "bold"), bg="#17a2b8", fg="white",
            command=lambda: (search_entry.delete(0, tk.END), self.invoice_logic.load_invoices())
        ).pack(side=tk.LEFT, padx=5, ipady=4)
        
        # Nút Xem chi tiết
        tk.Button(
            func_frame, text="👁️ Xem Chi Tiết", font=("Arial", 10, "bold"), bg="#007bff", fg="white", 
            command=self.invoice_logic.show_invoice_details
        ).pack(side=tk.LEFT, padx=5, ipady=4)

        # Nút Xóa hóa đơn [MỚI]
        tk.Button(
            func_frame, text="🗑️ Xóa Hóa Đơn", font=("Arial", 10, "bold"), bg="#dc3545", fg="white", 
            command=self.invoice_logic.delete_invoice
        ).pack(side=tk.LEFT, padx=5, ipady=4)

        # --- KHUNG HIỂN THỊ DANH SÁCH ---
        table_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        columns = ("Mã HĐ", "Khách hàng", "Nhân viên", "Ngày lập", "Tổng tiền", "Thanh toán", "Còn nợ", "Trạng thái")
        self.invoice_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)
        
        # ... (Phần định dạng cột Treeview giữ nguyên như cũ) ...
        self.invoice_tree.heading("Mã HĐ", text="Mã HĐ")
        self.invoice_tree.column("Mã HĐ", width=60, anchor="center")
        self.invoice_tree.heading("Khách hàng", text="Khách hàng")
        self.invoice_tree.column("Khách hàng", width=200)
        self.invoice_tree.heading("Nhân viên", text="Nhân viên")
        self.invoice_tree.column("Nhân viên", width=150)
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
        
        # Bind sự kiện enter để tìm kiếm
        search_entry.bind("<Return>", lambda e: self.invoice_logic.load_invoices(search_entry.get()))
        
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
            
            ("💰 Công nợ khách hàng", self.report_logic.report_debt)
        ]
        row, col = 0, 0
        for text, command in reports:
            btn = tk.Button(report_frame, text=text, font=("Arial", 12), bg=self.btn_color, fg="white", width=30, height=3, command=command)
            btn.grid(row=row, column=col, padx=15, pady=15)
            col += 1
            if col > 1: col, row = 0, row + 1