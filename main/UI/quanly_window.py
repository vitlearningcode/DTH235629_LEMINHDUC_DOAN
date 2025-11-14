# =================================================================
# FILE: quanly_window.py
# MÔ TẢ: Class QuanLy - Giao diện quản lý (ĐÃ THÊM THANH TÌM KIẾM)
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
        self.view_warehouse = QuanLyWarehouseViewLogic(self)
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
            pass # Sử dụng theme mặc định nếu 'vista' không có

        s.configure('Content.TFrame', background=self.bg_color)
        s.configure('Content.TLabel', background=self.bg_color, foreground=self.header_fg, font=self.font_header)
        s.configure('Menu.TFrame', background=self.menu_color)
        s.configure('Menu.TLabel', background=self.menu_color, foreground=self.text_color, font=self.font_menu_title)
        
        s.configure('Std.TLabel', background=self.bg_color, font=self.font_label)
        s.configure('Card.TFrame', background="white", relief="raised", borderwidth=2)
        s.configure('Func.TButton', font=self.font_button, padding=5)
        
        s.configure("Treeview", 
                    rowheight=28, 
                    font=("Segoe UI", 10),
                    background="white",
                    fieldbackground="white")
        s.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        s.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

    def setup_ui(self):
        """Thiết lập giao diện (Sử dụng TTK)"""
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
        
        menu_frame = ttk.Frame(self.window, style='Menu.TFrame', width=250)
        menu_frame.pack(fill=tk.Y, side=tk.LEFT)
        menu_frame.pack_propagate(False)
        
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
            ("📦 Xem kho", self.view_warehouse),
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
    
    # --- Hàm trợ giúp tạo thanh tìm kiếm ---
    def create_search_bar(self, parent_frame, search_command):
        """Tạo một frame chứa ô tìm kiếm và nút tìm"""
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
        
        search_button = ttk.Button(
            search_frame, 
            text="Tìm", 
            style='Func.TButton', 
            command=lambda: search_command(search_entry.get()),
            cursor="hand2"
        )
        search_button.pack(side=tk.LEFT, padx=(10, 0))
        
        # Bind phím Enter
        search_entry.bind("<Return>", lambda e: search_command(search_entry.get()))

        return search_entry # Trả về entry để có thể .get()

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
        
        # (Sử dụng tk.Frame và tk.Label để dễ dàng set màu nền)
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

    
    def view_employees(self):
        """Xem danh sách nhân viên (ĐÃ THÊM TÌM KIẾM)"""
        self.clear_content()
        
        ttk.Label(
            self.content_frame,
            text="DANH SÁCH NHÂN VIÊN (CHỈ XEM)",
            style='Content.TLabel'
        ).pack(pady=(0, 10))
        
        table_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
        
        columns = ("ID", "Họ tên", "SĐT", "Email", "Vai trò", "Trạng thái")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=25)
        
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
        
        # --- THÊM THANH TÌM KIẾM ---
        self.create_search_bar(self.content_frame, lambda keyword: self.view_employee.load_view(tree, keyword))
        
        table_frame.pack(fill=tk.BOTH, expand=True) # Đặt table_frame sau search_bar
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Tải dữ liệu ban đầu (không có keyword)
        self.view_employee.load_view(tree)
    
    def view_products(self):
        """Xem sản phẩm (ĐÃ THÊM TÌM KIẾM)"""
        self.clear_content()
        ttk.Label(
            self.content_frame,
            text="DANH SÁCH SẢN PHẨM (CHỈ XEM)",
            style='Content.TLabel'
        ).pack(pady=(0, 10))

        table_frame = ttk.Frame(self.content_frame, style='Content.TFrame')

        columns = ("Mã SP", "Tên SP", "Hãng", "Loại", "Giá bán", "Tồn kho")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=25)

        tree.heading("Mã SP", text="Mã SP")
        tree.column("Mã SP", width=50, anchor="center")
        tree.heading("Tên SP", text="Tên SP")
        tree.column("Tên SP", width=300, anchor="w")
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
        
        # --- THÊM THANH TÌM KIẾM ---
        self.create_search_bar(self.content_frame, lambda keyword: self.view_product.load_view(tree, keyword))
        
        table_frame.pack(fill=tk.BOTH, expand=True)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.view_product.load_view(tree) # Tải ban đầu
    
    def view_parts(self):
        """Xem phụ tùng (ĐÃ THÊM TÌM KIẾM)"""
        self.clear_content()
        ttk.Label(
            self.content_frame,
            text="DANH SÁCH PHỤ TÙNG (CHỈ XEM)",
            style='Content.TLabel'
        ).pack(pady=(0, 10))

        table_frame = ttk.Frame(self.content_frame, style='Content.TFrame')

        columns = ("Mã PT", "Tên Phụ Tùng", "Loại", "Giá bán", "Tồn kho")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=25)

        tree.heading("Mã PT", text="Mã PT")
        tree.column("Mã PT", width=50, anchor="center")
        tree.heading("Tên Phụ Tùng", text="Tên Phụ Tùng")
        tree.column("Tên Phụ Tùng", width=300, anchor="w")
        tree.heading("Loại", text="Loại")
        tree.column("Loại", width=150, anchor="center")
        tree.heading("Giá bán", text="Giá bán")
        tree.column("Giá bán", width=120, anchor="e")
        tree.heading("Tồn kho", text="Tồn kho")
        tree.column("Tồn kho", width=80, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # --- THÊM THANH TÌM KIẾM ---
        self.create_search_bar(self.content_frame, lambda keyword: self.view_part.load_view(tree, keyword))

        table_frame.pack(fill=tk.BOTH, expand=True)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.view_part.load_view(tree) # Tải ban đầu
    
    def view_warehouse(self):
        """Xem kho (Phiếu nhập kho) (ĐÃ THÊM TÌM KIẾM)"""
        self.clear_content()
        ttk.Label(
            self.content_frame,
            text="DANH SÁCH PHIẾU NHẬP KHO (CHỈ XEM)",
            style='Content.TLabel'
        ).pack(pady=(0, 10))

        table_frame = ttk.Frame(self.content_frame, style='Content.TFrame')

        columns = ("Mã Phiếu", "Nhà Cung Cấp", "Người Nhập", "Ngày Nhập", "Tổng Tiền", "Trạng Thái")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=25)

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
        
        # --- THÊM THANH TÌM KIẾM ---
        self.create_search_bar(self.content_frame, lambda keyword: self.view_warehouse.load_view(tree, keyword))

        table_frame.pack(fill=tk.BOTH, expand=True)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.view_warehouse.load_view(tree) # Tải ban đầu
    
    def view_customers(self):
        """Xem khách hàng (ĐÃ THÊM TÌM KIẾM)"""
        self.clear_content()
        ttk.Label(
            self.content_frame,
            text="DANH SÁCH KHÁCH HÀNG (CHỈ XEM)",
            style='Content.TLabel'
        ).pack(pady=(0, 10))

        table_frame = ttk.Frame(self.content_frame, style='Content.TFrame')

        columns = ("Mã KH", "Họ Tên", "SĐT", "Địa Chỉ", "Loại KH")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=25)

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
        
        # --- THÊM THANH TÌM KIẾM ---
        self.create_search_bar(self.content_frame, lambda keyword: self.view_customer.load_view(tree, keyword))
        
        table_frame.pack(fill=tk.BOTH, expand=True)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.view_customer.load_view(tree) # Tải ban đầu
    
    def view_invoices(self):
        """Xem hóa đơn (Sử dụng VIEW) (ĐÃ THÊM TÌM KIẾM)"""
        self.clear_content()
        ttk.Label(
            self.content_frame,
            text="DANH SÁCH HÓA ĐƠN (CHỈ XEM)",
            style='Content.TLabel'
        ).pack(pady=(0, 10))

        table_frame = ttk.Frame(self.content_frame, style='Content.TFrame')

        columns = ("Mã HĐ", "Ngày Lập", "Khách Hàng", "Nhân Viên", "Tổng Tiền", "Còn Nợ", "Trạng Thái")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=25)

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
        
        # --- THÊM THANH TÌM KIẾM ---
        self.create_search_bar(self.content_frame, lambda keyword: self.view_invoice.load_view(tree, keyword))

        table_frame.pack(fill=tk.BOTH, expand=True)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.view_invoice.load_view(tree) # Tải ban đầu
    
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
        
        for col in columns:
            self.attendance_tree.heading(col, text=col)
            width = 150 if col == "Họ tên" else 100
            self.attendance_tree.column(col, width=width, anchor="center")
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.attendance_tree.yview)
        self.attendance_tree.configure(yscrollcommand=scrollbar.set)
        
        self.attendance_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
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
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=25)

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