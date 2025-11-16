# =================================================================
# FILE: quanly_window.py
# MÔ TẢ: Class QuanLy - Giao diện quản lý (ĐÃ SỬA LỖI LAYOUT PANEL CHI TIẾT)
# =================================================================

import tkinter as tk
from tkinter import messagebox, ttk
from database_connection import DatabaseConnection
from datetime import datetime, date

# --- 1. IMPORT TẤT CẢ 10 LỚP LOGIC ---
from Function.function_QuanLy.quanly_attendance_logic import QuanLyAttendanceLogic
from Function.function_QuanLy.quanly_system_logic import QuanLySystemLogic
from Function.function_QuanLy.quanly_employee_view_logic import QuanLyEmployeeViewLogic
from Function.function_QuanLy.quanly_product_view_logic import QuanLyProductViewLogic
from Function.function_QuanLy.quanly_part_view_logic import QuanLyPartViewLogic
from Function.function_QuanLy.quanly_warehouse_view_logic import QuanLyWarehouseViewLogic
from Function.function_QuanLy.quanly_customer_view_logic import QuanLyCustomerViewLogic
from Function.function_QuanLy.quanly_invoice_view_logic import QuanLyInvoiceViewLogic
from Function.function_QuanLy.quanly_report_view_logic import QuanLyReportViewLogic
from Function.function_QuanLy.quanly_dashboard_logic import QuanLyDashboardLogic


class QuanLy:
    def __init__(self, user_info):
        """Khởi tạo cửa sổ Quản lý"""
        self.window = tk.Tk()
        self.window.title(f"QUẢN LÝ - {user_info['HoTen']}")
        self.window.geometry("1200x700")
        self.window.state('zoomed')
        
        self.user_info = user_info
        
        # --- BỘ FONT CHỮ ---
        self.font_title = ("Segoe UI", 18, "bold")
        self.font_header = ("Segoe UI", 16, "bold")
        self.font_menu_title = ("Segoe UI", 14, "bold")
        self.font_menu_btn = ("Segoe UI", 11, "bold")
        self.font_label = ("Segoe UI", 12)
        self.font_info = ("Segoe UI", 12)
        self.font_button = ("Segoe UI", 10, "bold")
        self.font_card_label = ("Segoe UI", 12, "bold")
        self.font_card_value = ("Segoe UI", 24, "bold")

        # Màu sắc
        self.bg_color = "#E6F2FF"
        self.menu_color = "#5F9EA0"
        self.btn_color = "#4682B4"
        self.text_color = "#FFFFFF"
        self.header_fg = "#003366"
        
        # Database
        self.db = DatabaseConnection()
        self.db.connect()
        
        # --- 2. KHỞI TẠO TẤT CẢ 10 LỚP LOGIC ---
        self.logic_attendance = QuanLyAttendanceLogic(self)
        self.logic_system = QuanLySystemLogic(self)
        self.view_employee = QuanLyEmployeeViewLogic(self)
        self.view_product = QuanLyProductViewLogic(self)
        self.view_part = QuanLyPartViewLogic(self)
        self.view_warehouse = QuanLyWarehouseViewLogic(self) # Đây là BIẾN LOGIC
        self.view_customer = QuanLyCustomerViewLogic(self)
        self.view_invoice = QuanLyInvoiceViewLogic(self)
        self.view_report = QuanLyReportViewLogic(self)
        self.logic_dashboard = QuanLyDashboardLogic(self)
        
        self.setup_styles()
        self.setup_ui()
        self.window.protocol("WM_DELETE_WINDOW", self.logic_system.on_closing)
        self.window.mainloop()

    def setup_styles(self):
        """Định nghĩa style cho các widget TTK"""
        s = ttk.Style()
        try:
            s.theme_use('vista')
        except tk.TclError:
            pass 

        s.configure('Content.TFrame', background=self.bg_color)
        s.configure('Content.TLabel', background=self.bg_color, foreground=self.header_fg, font=self.font_header)
        s.configure('Menu.TFrame', background=self.menu_color)
        s.configure('Menu.TLabel', background=self.menu_color, foreground=self.text_color, font=self.font_menu_title)
        
        s.configure('Std.TLabel', background=self.bg_color, font=self.font_label)
        s.configure('Card.TFrame', background="white", relief="raised", borderwidth=2)
        s.configure('Func.TButton', font=self.font_button, padding=5)
        
        # Style cho LabelFrame nền trắng (dùng cho Detail Pane)
        s.configure('Details.TLabelframe', background="white", padding=10)
        s.configure('Details.TLabelframe.Label', background="white", font=self.font_label, foreground="#003366")
        
        # Style cho Label bên trong LabelFrame (nền trắng)
        s.configure('Details.TLabel', background="white", font=self.font_label)
        
        s.configure("Treeview", 
                    rowheight=28, 
                    font=("Segoe UI", 10),
                    background="white",
                    fieldbackground="white")
        s.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        s.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})]) # Bỏ viền

    def setup_ui(self):
        """Thiết lập giao diện (Sử dụng TTK)"""
        # Header (tk.Frame)
        header_frame = tk.Frame(self.window, bg=self.menu_color, height=60)
        header_frame.pack(fill=tk.X, side=tk.TOP, ipady=5)
        
        tk.Label(
            header_frame,
            text="HỆ THỐNG QUẢN LÝ CỬA HÀNG XE MÁY - QUẢN LÝ",
            font=self.font_title,
            bg=self.menu_color,
            fg=self.text_color
        ).pack(side=tk.LEFT, padx=20)
        
        tk.Label(
            header_frame,
            text=f"Xin chào: {self.user_info['HoTen']}",
            font=self.font_label,
            bg=self.menu_color,
            fg=self.text_color
        ).pack(side=tk.RIGHT, padx=20)
        
        tk.Button(
            header_frame,
            text="Đăng xuất",
            font=self.font_button,
            bg="#DC143C",
            fg=self.text_color,
            command=self.logic_system.logout,
            relief="flat",
            padx=10,
            pady=5,
            cursor="hand2"
        ).pack(side=tk.RIGHT, padx=10)
        
        # Menu (ttk.Frame)
        menu_frame = ttk.Frame(self.window, style='Menu.TFrame', width=250)
        menu_frame.pack(fill=tk.Y, side=tk.LEFT)
        menu_frame.pack_propagate(False)
        
        # Nội dung (ttk.Frame)
        self.content_frame = ttk.Frame(self.window, style='Content.TFrame', padding=20)
        self.content_frame.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)
        
        self.create_menu(menu_frame)
        self.show_dashboard()
    
    def create_menu(self, parent):
        """Tạo menu điều hướng (Dùng tk.Button để giữ màu)"""
        menu_items = [
            ("🏠 Trang chủ", self.show_dashboard),
            ("👥 Xem nhân viên", self.view_employees),
            ("🏍️ Xem sản phẩm", self.view_products),
            ("🔧 Xem phụ tùng", self.view_parts),
            ("📦 Xem kho", self.show_warehouse_view), # <--- SỬA LỖI 1: Đổi lệnh gọi hàm
            ("👤 Xem khách hàng", self.view_customers),
            ("📄 Xem hóa đơn", self.view_invoices),
            ("⏰ Chấm công", self.manage_attendance),
            ("📊 Xem báo cáo", self.view_reports)
        ]
        
        ttk.Label(
            parent,
            text="MENU CHÍNH",
            style='Menu.TLabel'
        ).pack(pady=20)
        
        for text, command in menu_items:
            btn = tk.Button(
                parent,
                text=text,
                font=self.font_menu_btn,
                bg=self.btn_color,
                fg=self.text_color,
                command=command,
                cursor="hand2",
                anchor="w",
                width=25,
                relief="flat",
                padx=10,
                pady=8
            )
            hover_color = "#5A9BD8"
            btn.bind("<Enter>", lambda e, b=btn, c=hover_color: b.config(bg=c))
            btn.bind("<Leave>", lambda e, b=btn, c=self.btn_color: b.config(bg=c))
            btn.pack(pady=4, padx=15, fill=tk.X)
    
    def clear_content(self):
        """Xóa nội dung frame"""
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
            font=self.font_label, 
            width=40
        )
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        search_entry.bind("<KeyRelease>", lambda e: search_command(search_entry.get()))
        return search_entry

    # =================================================================
    # CÁC HÀM VẼ GIAO DIỆN (UI-DRAWING METHODS)
    # =================================================================

    def show_dashboard(self):
        """Hiển thị trang chủ (ĐÃ NÂNG CẤP VỚI CÁC THẺ)"""
        self.clear_content()
        
        ttk.Label(
            self.content_frame,
            text="TRANG CHỦ QUẢN LÝ",
            style='Content.TLabel'
        ).pack(pady=(0, 20), anchor="center")
        
        stats_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
        stats_frame.pack(fill=tk.BOTH, expand=True)
        
        stats = self.logic_dashboard.get_dashboard_stats()
        colors = ["#17A2B8", "#28A745", "#FFC107", "#DC3545"]
        
        card1 = tk.Frame(stats_frame, bg=colors[0], width=250, height=150, relief="raised", bd=2)
        card1.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        card2 = tk.Frame(stats_frame, bg=colors[1], width=250, height=150, relief="raised", bd=2)
        card2.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        card3 = tk.Frame(stats_frame, bg=colors[2], width=250, height=150, relief="raised", bd=2)
        card3.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        card4 = tk.Frame(stats_frame, bg=colors[3], width=250, height=150, relief="raised", bd=2)
        card4.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")
        
        stats_frame.grid_columnconfigure(0, weight=1)
        stats_frame.grid_columnconfigure(1, weight=1)
        stats_frame.grid_rowconfigure(0, weight=1)
        stats_frame.grid_rowconfigure(1, weight=1)

        tk.Label(card1, text="Tổng nhân viên", font=self.font_card_label, bg=colors[0], fg="white").pack(pady=(20, 5))
        tk.Label(card1, text=stats.get("Tổng nhân viên", 0), font=self.font_card_value, bg=colors[0], fg="white").pack(pady=5)
        card1.pack_propagate(False)

        tk.Label(card2, text="Tổng khách hàng", font=self.font_card_label, bg=colors[1], fg="white").pack(pady=(20, 5))
        tk.Label(card2, text=stats.get("Tổng khách hàng", 0), font=self.font_card_value, bg=colors[1], fg="white").pack(pady=5)
        card2.pack_propagate(False)

        tk.Label(card3, text="Nhân viên có mặt", font=self.font_card_label, bg=colors[2], fg="#343A40").pack(pady=(20, 5))
        tk.Label(card3, text=stats.get("Nhân viên có mặt", 0), font=self.font_card_value, bg=colors[2], fg="#343A40").pack(pady=5)
        card3.pack_propagate(False)

        tk.Label(card4, text="Doanh thu hôm nay", font=self.font_card_label, bg=colors[3], fg="white").pack(pady=(20, 5))
        tk.Label(card4, text=stats.get("Doanh thu hôm nay", "0 VNĐ"), font=self.font_card_value, bg=colors[3], fg="white").pack(pady=5)
        card4.pack_propagate(False)

    
    # =================================================================
    # HÀM XEM NHÂN VIÊN (ĐÃ SỬA LỖI LAYOUT)
    # =================================================================
    def view_employees(self):
        """Xem danh sách nhân viên (NÂNG CẤP: Live Search + Panel Chi Tiết)"""
        self.clear_content()
        
        ttk.Label(
            self.content_frame,
            text="QUẢN LÝ THÔNG TIN NHÂN VIÊN",
            style='Content.TLabel'
        ).pack(pady=(0, 10))
        
        # --- 1. THANH TÌM KIẾM (Live Search) ---
        self.search_entry = self.create_search_bar(
            self.content_frame, 
            lambda keyword: self.view_employee.load_view(self.employee_tree, keyword)
        )
        
        # --- 2. KHUNG BẢNG (Treeview) ---
        table_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 10)) 
        
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
        
        tree.bind("<<TreeviewSelect>>", self.view_employee.on_employee_select)
        self.view_employee.load_view(tree)

        # --- 3. KHUNG CHI TIẾT (Panel) ---
        details_frame = ttk.LabelFrame(self.content_frame, text="Chi tiết Nhân viên", style='Details.TLabelframe')
        details_frame.pack(fill=tk.X, expand=False, pady=(10, 0))

        # --- SỬA LỖI LAYOUT BẮT ĐẦU TỪ ĐÂY ---

        # 3.1. Cột Ảnh (Bên trái)
        image_frame = ttk.Frame(details_frame, style='Card.TFrame', width=160, height=200)
        image_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 20), pady=10)
        image_frame.pack_propagate(False) 

        # Nút Tải ảnh lên (PACK TRƯỚC VÀ ĐẶT Ở DƯỚI CÙNG)
        upload_button = ttk.Button(
            image_frame, 
            text="Tải ảnh lên", 
            style='Func.TButton', 
            command=self.view_employee.upload_image,
            cursor="hand2"
        )
        upload_button.pack(side=tk.BOTTOM, pady=10)
        
        # Label để giữ ảnh (PACK SAU, NÓ SẼ CHIẾM PHẦN CÒN LẠI)
        self.image_label = ttk.Label(image_frame, text="Chọn NV", anchor="center", background="lightgrey", relief="groove")
        self.image_label.pack(fill=tk.BOTH, expand=True, side=tk.TOP, pady=5, padx=5)

        # 3.2. Cột Thông tin (Ở giữa) - (PACK CUỐI CÙNG ĐỂ NÓ TỰ GIÃN RA)
        info_frame = ttk.Frame(details_frame, style='Card.TFrame')
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10, padx=(0, 20)) # Thêm padding bên phải

        # ID (Chỉ hiển thị)
        self.details_emp_id = ttk.Label(info_frame, text="ID: (Chưa chọn)", style='Details.TLabel', font=self.font_label)
        self.details_emp_id.grid(row=0, column=0, columnspan=2, pady=10, sticky="w", padx=10)

        # --- CỘT 1 THÔNG TIN ---
        ttk.Label(info_frame, text="Họ tên:", style='Details.TLabel').grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.details_hoten = ttk.Entry(info_frame, font=self.font_label, width=30)
        self.details_hoten.grid(row=1, column=1, pady=5, sticky="ew") # Thêm sticky="ew"
        
        ttk.Label(info_frame, text="SĐT:", style='Details.TLabel').grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.details_sdt = ttk.Entry(info_frame, font=self.font_label, width=30)
        self.details_sdt.grid(row=2, column=1, pady=5, sticky="ew")

        ttk.Label(info_frame, text="Email:", style='Details.TLabel').grid(row=3, column=0, sticky="e", padx=10, pady=5)
        self.details_email = ttk.Entry(info_frame, font=self.font_label, width=30)
        self.details_email.grid(row=3, column=1, pady=5, sticky="ew")

        # --- CỘT 2 THÔNG TIN ---
        ttk.Label(info_frame, text="Vai trò:", style='Details.TLabel').grid(row=1, column=2, sticky="e", padx=10, pady=5)
        self.details_vaitro = ttk.Combobox(info_frame, values=["NhanVien", "QuanLy"], state="readonly", font=self.font_label, width=20)
        self.details_vaitro.grid(row=1, column=3, pady=5, padx=10, sticky="ew")
        
        ttk.Label(info_frame, text="Trạng thái:", style='Details.TLabel').grid(row=2, column=2, sticky="e", padx=10, pady=5)
        self.details_trangthai = ttk.Combobox(info_frame, values=["HoatDong", "KhongHoatDong"], state="readonly", font=self.font_label, width=20)
        self.details_trangthai.grid(row=2, column=3, pady=5, padx=10, sticky="ew")

        # --- NÚT CẬP NHẬT (CHUYỂN VÀO ĐÂY) ---
        self.update_button = tk.Button(
            info_frame,
            text="CẬP NHẬT",
            font=self.font_button,
            bg="#007bff",
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            command=self.view_employee.update_employee,
            state="disabled",
            cursor=""
        )
        # Đặt nút ở dưới, căn lề phải
        self.update_button.grid(row=3, column=3, pady=10, padx=10, sticky="se")

        # Cấu hình grid co dãn
        info_frame.grid_columnconfigure(1, weight=1)
        info_frame.grid_columnconfigure(3, weight=1)

        # GỌI HÀM KIỂM TRA THAY ĐỔI
        self.details_hoten.bind("<KeyRelease>", self.view_employee.check_for_changes)
        self.details_sdt.bind("<KeyRelease>", self.view_employee.check_for_changes)
        self.details_email.bind("<KeyRelease>", self.view_employee.check_for_changes)
        self.details_vaitro.bind("<<ComboboxSelected>>", self.view_employee.check_for_changes)
        self.details_trangthai.bind("<<ComboboxSelected>>", self.view_employee.check_for_changes)
        
        # --- KẾT THÚC SỬA LỖI LAYOUT ---

    
    def view_products(self):
        self.clear_content()
        ttk.Label(
            self.content_frame,
            text="QUẢN LÝ THÔNG TIN SẢN PHẨM",
            style='Content.TLabel'
        ).pack(pady=(0, 10))
        self.search_entry = self.create_search_bar(
            self.content_frame,
            lambda keyword: self.view_product.load_view(self.product_tree, keyword)
        )

        # --- BẢNG SẢN PHẨM ---
        table_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 10))
        columns = ("Mã SP", "Tên SP", "Hãng", "Loại", "Giá bán", "Tồn kho")
        self.product_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        for col in columns:
            self.product_tree.heading(col, text=col)
            self.product_tree.column(col, width=120, anchor="center")
        self.product_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.product_tree.yview)
        self.product_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.product_tree.bind("<ButtonRelease-1>", self.view_product.on_product_select)
        self.view_product.load_view(self.product_tree)

        # --- PANEL CHI TIẾT SẢN PHẨM ---
        details_frame = ttk.LabelFrame(self.content_frame, text="Chi tiết Sản phẩm", style='Details.TLabelframe')
        details_frame.pack(fill=tk.X, expand=False, pady=(10, 0))

        # Cột trái: ảnh sản phẩm + nút tải ảnh
        image_frame = ttk.Frame(details_frame, style='Card.TFrame', width=160, height=200)
        image_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 20), pady=10)
        image_frame.pack_propagate(False)
        upload_button = ttk.Button(
            image_frame, text="Tải ảnh lên", style='Func.TButton',
            command=self.view_product.upload_image, cursor="hand2"
        )
        upload_button.pack(side=tk.BOTTOM, pady=10)
        self.product_image_label = ttk.Label(
            image_frame, text="Chọn SP", anchor="center", background="lightgrey", relief="groove")
        self.product_image_label.pack(fill=tk.BOTH, expand=True, side=tk.TOP, pady=5, padx=5)

        # Cột phải: các trường thông tin sản phẩm
        info_frame = ttk.Frame(details_frame, style='Card.TFrame')
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10, padx=(0, 20))

        # Mã sản phẩm (chỉ hiển thị)
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

        # Hãng xe
        ttk.Label(info_frame, text="Hãng:", style='Details.TLabel').grid(row=1, column=2, sticky="e", padx=10, pady=5)
        self.details_hang = ttk.Combobox(info_frame, values=["Honda", "Yamaha", "Suzuki", "..."], state="readonly", font=self.font_label, width=20)
        self.details_hang.grid(row=1, column=3, pady=5, padx=10, sticky="ew")

        # Loại xe
        ttk.Label(info_frame, text="Loại:", style='Details.TLabel').grid(row=2, column=2, sticky="e", padx=10, pady=5)
        self.details_loai = ttk.Combobox(info_frame, values=["Xe Tay Ga", "Xe Số", "Xe Côn Tay"], state="readonly", font=self.font_label, width=20)
        self.details_loai.grid(row=2, column=3, pady=5, padx=10, sticky="ew")

        # Nút cập nhật
        self.update_button = tk.Button(
            info_frame, text="CẬP NHẬT", font=self.font_button, bg="#007bff", fg="white",
            relief="flat", padx=20, pady=10, command=self.view_product.update_product, state="disabled", cursor=""
        )
        self.update_button.grid(row=3, column=3, pady=10, padx=10, sticky="e")  # hoặc sticky="w"

        info_frame.grid_columnconfigure(1, weight=1)
        info_frame.grid_columnconfigure(3, weight=1)

        # Bind sự kiện cho các trường để kiểm tra thay đổi
        self.details_name.bind("<KeyRelease>", self.view_product.check_for_changes)
        self.details_price.bind("<KeyRelease>", self.view_product.check_for_changes)
        self.details_stock.bind("<KeyRelease>", self.view_product.check_for_changes)
        self.details_hang.bind("<<ComboboxSelected>>", self.view_product.check_for_changes)
        self.details_loai.bind("<<ComboboxSelected>>", self.view_product.check_for_changes)

    
    def view_parts(self):
        self.clear_content()
        ttk.Label(
            self.content_frame,
            text="QUẢN LÝ THÔNG TIN PHỤ TÙNG",
            style='Content.TLabel'
        ).pack(pady=(0, 10))
        self.search_entry = self.create_search_bar(
            self.content_frame,
            lambda keyword: self.view_part.load_view(self.part_tree, keyword)
        )

        # BẢNG PHỤ TÙNG
        table_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 10))
        columns = ("Mã PT", "Tên PT", "Loại", "Giá bán", "Tồn kho")
        self.part_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        for col in columns:
            self.part_tree.heading(col, text=col)
            self.part_tree.column(col, width=120, anchor="center")
        self.part_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.part_tree.yview)
        self.part_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.part_tree.bind("<ButtonRelease-1>", self.view_part.on_part_select)
        self.view_part.load_view(self.part_tree)

        # PANEL CHI TIẾT PHỤ TÙNG
        details_frame = ttk.LabelFrame(self.content_frame, text="Chi tiết Phụ tùng", style='Details.TLabelframe')
        details_frame.pack(fill=tk.X, expand=False, pady=(10, 0))

        # Ảnh + nút upload
        image_frame = ttk.Frame(details_frame, style='Card.TFrame', width=160, height=200)
        image_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 20), pady=10)
        image_frame.pack_propagate(False)
        upload_button = ttk.Button(
            image_frame, text="Tải ảnh lên", style='Func.TButton',
            command=self.view_part.upload_image, cursor="hand2"
        )
        upload_button.pack(side=tk.BOTTOM, pady=10)
        self.part_image_label = ttk.Label(
            image_frame, text="Chọn PT", anchor="center", background="lightgrey", relief="groove")
        self.part_image_label.pack(fill=tk.BOTH, expand=True, side=tk.TOP, pady=5, padx=5)

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

        # Loại phụ tùng (mapping chuẩn)
        ttk.Label(info_frame, text="Loại:", style='Details.TLabel').grid(row=1, column=2, sticky="e", padx=10, pady=5)
        self.details_loai = ttk.Combobox(
            info_frame, values=list(self.view_part.loaipt_dict.keys()), state="readonly", font=self.font_label, width=20)
        self.details_loai.grid(row=1, column=3, pady=5, padx=10, sticky="ew")

        # NÚT CẬP NHẬT
        self.update_button = tk.Button(
            info_frame, text="CẬP NHẬT", font=self.font_button, bg="#007bff", fg="white",
            relief="flat", padx=20, pady=10, command=self.view_part.update_part, state="disabled", cursor=""
        )
        self.update_button.grid(row=3, column=3, pady=10, padx=10, sticky="e")  # hoặc sticky="w"

        info_frame.grid_columnconfigure(1, weight=1)
        info_frame.grid_columnconfigure(3, weight=1)

        # Bind các trường để kiểm tra thay đổi
        self.details_name.bind("<KeyRelease>", self.view_part.check_for_changes)
        self.details_price.bind("<KeyRelease>", self.view_part.check_for_changes)
        self.details_stock.bind("<KeyRelease>", self.view_part.check_for_changes)
        self.details_loai.bind("<<ComboboxSelected>>", self.view_part.check_for_changes)

    
    def show_warehouse_view(self): # <--- SỬA LỖI 2: Đổi tên hàm
        """Xem kho (Phiếu nhập kho)"""
        self.clear_content()
        ttk.Label(
            self.content_frame,
            text="DANH SÁCH PHIẾU NHẬP KHO (CHỈ XEM)",
            style='Content.TLabel'
        ).pack(pady=(0, 10))

        func_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
        func_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(func_frame, text="Tìm kiếm:", style='Std.TLabel').pack(side=tk.LEFT, padx=(0, 10))
        search_entry = ttk.Entry(func_frame, font=self.font_label, width=40)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(
            func_frame, text="Tìm", style='Func.TButton', 
            command=lambda: self.view_warehouse.load_view(self.warehouse_tree, search_entry.get()),
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=(10, 0))
        
        ttk.Button(
            func_frame, text="🔍 Xem chi tiết", style='Func.TButton', 
            command=self.view_warehouse.show_warehouse_details,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=(10, 0))
        
        search_entry.bind("<Return>", lambda e: self.view_warehouse.load_view(self.warehouse_tree, search_entry.get()))

        table_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("Mã Phiếu", "Nhà Cung Cấp", "Người Nhập", "Ngày Nhập", "Tổng Tiền", "Trạng Thái")
        self.warehouse_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=25)
        
        tree = self.warehouse_tree
        tree.heading("Mã Phiếu", text="Mã Phiếu")
        tree.column("Mã Phiếu", width=80, anchor="center")
        tree.heading("Nhà Cung Cấp", text="Nhà Cung Cấp")
        tree.column("Nhà Cung Cấp", width=250, anchor="w")
        tree.heading("Người Nhập", text="Người Nhập")
        tree.column("Người Nhập", width=150, anchor="w")
        tree.heading("Ngày Nhập", text="Ngày Nhập")
        tree.column("Ngày Nhập", width=150, anchor="center")
        tree.heading("Tổng Tiền", text="Tổng Tiền")
        tree.column("Tổng Tiền", width=150, anchor="e")
        tree.heading("Trạng Thái", text="Trạng Thái")
        tree.column("Trạng Thái", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        tree.bind("<Double-1>", lambda e: self.view_warehouse.show_warehouse_details())

        self.view_warehouse.load_view(tree)
    
    def view_customers(self):
        """Xem khách hàng"""
        self.clear_content()
        ttk.Label(
            self.content_frame,
            text="DANH SÁCH KHÁCH HÀNG (CHỈ XEM)",
            style='Content.TLabel'
        ).pack(pady=(0, 10))

        self.search_entry = self.create_search_bar(self.content_frame, lambda keyword: self.view_customer.load_view(self.customer_tree, keyword))

        table_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("Mã KH", "Họ Tên", "SĐT", "Địa Chỉ", "Loại KH")
        self.customer_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=25)
        
        tree = self.customer_tree
        tree.heading("Mã KH", text="Mã KH")
        tree.column("Mã KH", width=50, anchor="center")
        tree.heading("Họ Tên", text="Họ Tên")
        tree.column("Họ Tên", width=200, anchor="w")
        tree.heading("SĐT", text="SĐT")
        tree.column("SĐT", width=120, anchor="center")
        tree.heading("Địa Chỉ", text="Địa Chỉ")
        tree.column("Địa Chỉ", width=300, anchor="w")
        tree.heading("Loại KH", text="Loại KH")
        tree.column("Loại KH", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.view_customer.load_view(tree)
    
    def view_invoices(self):
        """Xem hóa đơn (Sử dụng VIEW)"""
        self.clear_content()
        ttk.Label(
            self.content_frame,
            text="DANH SÁCH HÓA ĐƠN (CHỈ XEM)",
            style='Content.TLabel'
        ).pack(pady=(0, 10))

        func_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
        func_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(func_frame, text="Tìm kiếm:", style='Std.TLabel').pack(side=tk.LEFT, padx=(0, 10))
        search_entry = ttk.Entry(func_frame, font=self.font_label, width=40)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(
            func_frame, text="Tìm", style='Func.TButton', 
            command=lambda: self.view_invoice.load_view(self.invoice_tree, search_entry.get()),
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=(10, 0))
        
        ttk.Button(
            func_frame, text="🔍 Xem chi tiết", style='Func.TButton', 
            command=self.view_invoice.show_invoice_details,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=(10, 0))
        
        search_entry.bind("<Return>", lambda e: self.view_invoice.load_view(self.invoice_tree, search_entry.get()))

        table_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("Mã HĐ", "Ngày Lập", "Khách Hàng", "Nhân Viên", "Tổng Tiền", "Còn Nợ", "Trạng Thái")
        self.invoice_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=25)
        
        tree = self.invoice_tree
        tree.heading("Mã HĐ", text="Mã HĐ")
        tree.column("Mã HĐ", width=60, anchor="center")
        tree.heading("Ngày Lập", text="Ngày Lập")
        tree.column("Ngày Lập", width=140, anchor="center")
        tree.heading("Khách Hàng", text="Khách Hàng")
        tree.column("Khách Hàng", width=200, anchor="w")
        tree.heading("Nhân Viên", text="Nhân Viên")
        tree.column("Nhân Viên", width=200, anchor="w")
        tree.heading("Tổng Tiền", text="Tổng Tiền")
        tree.column("Tổng Tiền", width=120, anchor="e")
        tree.heading("Còn Nợ", text="Còn Nợ")
        tree.column("Còn Nợ", width=120, anchor="e")
        tree.heading("Trạng Thái", text="Trạng Thái")
        tree.column("Trạng Thái", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        tree.bind("<Double-1>", lambda e: self.view_invoice.show_invoice_details())

        self.view_invoice.load_view(tree)
    
    def manage_attendance(self):
        """Vẽ UI Chấm công nhân viên (Chức năng logic chính)"""
        self.clear_content()
        
        ttk.Label(
            self.content_frame,
            text="CHẤM CÔNG NHÂN VIÊN",
            style='Content.TLabel'
        ).pack(pady=(0, 10))
        
        date_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
        date_frame.pack(pady=10, fill=tk.X)
        
        ttk.Label(
            date_frame,
            text="Ngày chấm công:",
            style='Std.TLabel',
            font=self.font_label
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.date_var = tk.StringVar(value=date.today().strftime('%Y-%m-%d'))
        date_entry = ttk.Entry(
            date_frame, 
            textvariable=self.date_var, 
            font=self.font_label, 
            width=15
        )
        date_entry.pack(side=tk.LEFT, padx=10)
        
        ttk.Button(
            date_frame,
            text="Tải dữ liệu",
            style='Func.TButton',
            command=self.logic_attendance.load_attendance,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=10)
        
        table_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(10,0))
        
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
        
        btn_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
        btn_frame.pack(pady=10)
        
        tk.Button(
            btn_frame,
            text="✓ Chấm công",
            font=self.font_button,
            bg="#28a745",
            fg="white",
            command=self.logic_attendance.add_attendance,
            relief="flat",
            padx=10,
            pady=5,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=5)
        
        self.logic_attendance.load_attendance()
    
    def view_reports(self):
        """Xem báo cáo (Ví dụ: Tồn kho)"""
        self.clear_content()
        ttk.Label(
            self.content_frame,
            text="BÁO CÁO TỒN KHO SẢN PHẨM (CHỈ XEM)",
            style='Content.TLabel'
        ).pack(pady=(0, 20))

        table_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("Mã SP", "Tên SP", "Hãng", "Loại", "Tồn kho", "Giá trị tồn kho")
        self.report_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=25)
        
        tree = self.report_tree
        tree.heading("Mã SP", text="Mã SP")
        tree.column("Mã SP", width=50, anchor="center")
        tree.heading("Tên SP", text="Tên SP")
        tree.column("Tên SP", width=300, anchor="w")
        tree.heading("Hãng", text="Hãng")
        tree.column("Hãng", width=100, anchor="center")
        tree.heading("Loại", text="Loại")
        tree.column("Loại", width=100, anchor="center")
        tree.heading("Tồn kho", text="Tồn kho")
        tree.column("Tồn kho", width=80, anchor="center")
        tree.heading("Giá trị tồn kho", text="Giá trị tồn kho")
        tree.column("Giá trị tồn kho", width=150, anchor="e")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.view_report.load_view(tree)