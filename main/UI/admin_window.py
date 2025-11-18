# =================================================================
# FILE: admin_window.py
# MÔ TẢ: Class Admin - Giao diện quản trị (ĐÃ DỌN DẸP)
# =================================================================
import tkinter as tk                         # CHÚ THÍCH: import thư viện tkinter dưới tên 'tk'
from tkinter import messagebox, ttk          # CHÚ THÍCH: import các thành phần phụ của tkinter
from database_connection import DatabaseConnection  # CHÚ THÍCH: import lớp kết nối CSDL
from datetime import datetime, date         # CHÚ THÍCH: import datetime và date từ module datetime

# --- IMPORT TẤT CẢ CÁC LỚP LOGIC ---
from Function.function_Admin.admin_dashboard_logic import AdminDashboardLogic  # CHÚ THÍCH: logic cho dashboard
from Function.function_Admin.admin_employee_logic import AdminEmployeeLogic    # CHÚ THÍCH: logic nhân viên
from Function.function_Admin.admin_product_logic import AdminProductLogic      # CHÚ THÍCH: logic sản phẩm
from Function.function_Admin.admin_part_logic import AdminPartLogic            # CHÚ THÍCH: logic phụ tùng
from Function.function_Admin.admin_customer_logic import AdminCustomerLogic    # CHÚ THÍCH: logic khách hàng
from Function.function_Admin.admin_invoice_logic import AdminInvoiceLogic      # CHÚ THÍCH: logic hóa đơn
from Function.function_Admin.admin_promotion_logic import AdminPromotionLogic  # CHÚ THÍCH: logic khuyến mãi
from Function.function_Admin.admin_reports_logic import AdminReportsLogic      # CHÚ THÍCH: logic báo cáo
from Function.function_Admin.admin_system_logic import AdminSystemLogic        # CHÚ THÍCH: logic hệ thống
#-------------------------------------------------------------------------
# imoport mới đưa vào ở đây hieu
from Function.function_Admin.admin_warehouse_logic import AdminWarehouseLogic  # CHÚ THÍCH: logic kho (hieu thêm)
#-------------------------------------------------------------------------
from Function.function_Admin.admin_attendance_logic import AdminAttendanceLogic  # CHÚ THÍCH: logic chấm công
#-------------------------------------------------------------------------
from Function.function_Admin.admin_warranty_logic import AdminWarrantyLogic    # CHÚ THÍCH: logic bảo hành
# --- KHÔNG CẦN IMPORT LOGIN TẠI ĐÂY ---

class Admin:                                 # CHÚ THÍCH: khai báo class Admin
    def __init__(self, user_info):           # CHÚ THÍCH: hàm khởi tạo, nhận user_info (dict)
        """Khởi tạo cửa sổ Admin"""
        self.window = tk.Tk()                # CHÚ THÍCH: tạo cửa sổ chính Tk
        self.window.title(f"ADMIN - {user_info['HoTen']}")  # CHÚ THÍCH: đặt tiêu đề cửa sổ kèm tên user
        self.window.geometry("1200x700")     # CHÚ THÍCH: đặt kích thước ban đầu
        self.window.state('zoomed')          # CHÚ THÍCH: phóng to cửa sổ (maximized)
        
        self.user_info = user_info           # CHÚ THÍCH: lưu thông tin user vào thể hiện
        
        # --- BỘ FONT CHỮ (ĐÃ BỔ SUNG ĐỂ SỬA LỖI) ---
        self.font_title = ("Segoe UI", 18, "bold")     # CHÚ THÍCH: font cho tiêu đề
        self.font_header = ("Segoe UI", 16, "bold")    # CHÚ THÍCH: font cho header
        self.font_menu_title = ("Segoe UI", 14, "bold")# CHÚ THÍCH: font tiêu đề menu
        self.font_menu_btn = ("Segoe UI", 11, "bold")  # CHÚ THÍCH: font cho nút menu
        self.font_label = ("Segoe UI", 12)             # CHÚ THÍCH: font cho label thông thường
        self.font_info = ("Segoe UI", 12)              # CHÚ THÍCH: font cho thông tin
        self.font_button = ("Segoe UI", 10, "bold")    # CHÚ THÍCH: font mặc định cho nút
        self.font_card_label = ("Segoe UI", 12, "bold")# CHÚ THÍCH: font nhãn card
        self.font_card_value = ("Segoe UI", 24, "bold")# CHÚ THÍCH: font giá trị lớn trên card

        # Màu sắc
        self.bg_color = "#E6F2FF"            # CHÚ THÍCH: màu nền content
        self.menu_color = "#4682B4"          # CHÚ THÍCH: màu nền menu
        self.btn_color = "#5F9EA0"           # CHÚ THÍCH: màu nút chung
        self.text_color = "#FFFFFF"          # CHÚ THÍCH: màu chữ trên nền tối
        
        # Database
        self.db = DatabaseConnection()       # CHÚ THÍCH: tạo instance kết nối DB
        self.db.connect()                    # CHÚ THÍCH: gọi method connect để nối DB
        
        # --- KHỞI TẠO TẤT CẢ LOGIC HELPER ---
        self.dashboard_logic = AdminDashboardLogic(self)   # CHÚ THÍCH: init logic dashboard, truyền view (self)
        self.emp_logic = AdminEmployeeLogic(self)          # CHÚ THÍCH: init logic nhân viên
        self.prod_logic = AdminProductLogic(self)          # CHÚ THÍCH: init logic sản phẩm
        self.part_logic = AdminPartLogic(self)             # CHÚ THÍCH: init logic phụ tùng
        self.cust_logic = AdminCustomerLogic(self)         # CHÚ THÍCH: init logic khách hàng
        self.invoice_logic = AdminInvoiceLogic(self)       # CHÚ THÍCH: init logic hóa đơn
        self.promo_logic = AdminPromotionLogic(self)       # CHÚ THÍCH: init logic khuyến mãi
        self.report_logic = AdminReportsLogic(self)        # CHÚ THÍCH: init logic báo cáo
        self.system_logic = AdminSystemLogic(self)         # CHÚ THÍCH: init logic hệ thống
        #-------------------------------------------------------------------------
        # dòng mới đc hieu thêm vào
        self.warehouse_logic = AdminWarehouseLogic(self)   # CHÚ THÍCH: init logic kho
        #-------------------------------------------------------------------------
        self.attend_logic = AdminAttendanceLogic(self)     # CHÚ THÍCH: init logic chấm công
        #-------------------------------------------------------------------------
        self.warranty_logic = AdminWarrantyLogic(self)     # CHÚ THÍCH: init logic bảo hành
        #-------------------------------------------------------------------------
        self.setup_styles()                # CHÚ THÍCH: cấu hình style ttk
        self.setup_ui()                    # CHÚ THÍCH: xây dựng giao diện UI
        self.window.protocol("WM_DELETE_WINDOW", self.system_logic.on_closing)  # CHÚ THÍCH: bắt sự kiện đóng cửa sổ
        self.window.mainloop()             # CHÚ THÍCH: chạy vòng lặp chính của Tk
    
    def setup_styles(self):               # CHÚ THÍCH: định nghĩa style cho widget TTK
        """Định nghĩa style cho các widget TTK"""
        s = ttk.Style()                  # CHÚ THÍCH: tạo instance Style
        try:
            s.theme_use('vista')         # CHÚ THÍCH: cố gắng sử dụng theme 'vista' nếu có
        except tk.TclError:
            pass                         # CHÚ THÍCH: nếu không có theme thì bỏ qua

        # Đặt tên style dựa trên màu nền của Admin
        s.configure('Content.TFrame', background=self.bg_color)   # CHÚ THÍCH: style frame nội dung
        s.configure('Content.TLabel', background=self.bg_color, foreground="#003366", font=("Segoe UI", 16, "bold"))  # CHÚ THÍCH: style label nội dung
        s.configure('Menu.TFrame', background=self.menu_color)    # CHÚ THÍCH: style frame menu
        s.configure('Menu.TLabel', background=self.menu_color, foreground=self.text_color, font=("Segoe UI", 14, "bold"))  # CHÚ THÍCH: style label menu
        
        s.configure('Std.TLabel', background=self.bg_color, font=("Segoe UI", 12))  # CHÚ THÍCH: style label chuẩn
        s.configure('Card.TFrame', background="white", relief="raised", borderwidth=2)  # CHÚ THÍCH: style card trắng
        s.configure('Func.TButton', font=("Segoe UI", 10, "bold"), padding=5)  # CHÚ THÍCH: style cho nút chức năng
        
        # Style cho LabelFrame nền trắng (dùng cho Detail Pane)
        s.configure('Details.TLabelframe', background="white", padding=10)  # CHÚ THÍCH: style labelframe chi tiết
        s.configure('Details.TLabelframe.Label', background="white", font=("Segoe UI", 12), foreground="#003366")  # CHÚ THÍCH: style label labelframe
        
        # Style cho Label bên trong LabelFrame (nền trắng)
        s.configure('Details.TLabel', background="white", font=("Segoe UI", 12))  # CHÚ THÍCH: style cho label trong details
        
        s.configure("Treeview", 
                    rowheight=28, 
                    font=("Segoe UI", 10),
                    background="white",
                    fieldbackground="white")  # CHÚ THÍCH: style tổng quan cho Treeview
        s.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))  # CHÚ THÍCH: style header Treeview
        s.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})]) # CHÚ THÍCH: loại bỏ viền Treeview
    def setup_ui(self):                   # CHÚ THÍCH: tạo giao diện chính (UI)
        """Thiết lập giao diện chính (Chỉ UI)"""
        # Header
        header_frame = tk.Frame(self.window, bg=self.menu_color, height=60)  # CHÚ THÍCH: frame header phía trên
        header_frame.pack(fill=tk.X, side=tk.TOP)     # CHÚ THÍCH: đặt header trên cùng
        
        tk.Label(
            header_frame,
            text="HỆ THỐNG QUẢN LÝ CỬA HÀNG XE MÁY - CHỦ CỬA HÀNG",
            font=("Arial", 18, "bold"),
            bg=self.menu_color,
            fg=self.text_color
        ).pack(side=tk.LEFT, padx=20, pady=10)         # CHÚ THÍCH: label tiêu đề hệ thống
        
        tk.Label(
            header_frame,
            text=f"Xin chào: {self.user_info['HoTen']}",
            font=("Arial", 12),
            bg=self.menu_color,
            fg=self.text_color
        ).pack(side=tk.RIGHT, padx=20, pady=10)        # CHÚ THÍCH: hiển thị tên user bên phải
        
        tk.Button(
            header_frame,
            text="Đăng xuất",
            font=("Arial", 10, "bold"),
            bg="#DC143C",
            fg=self.text_color,
            command=self.system_logic.logout
        ).pack(side=tk.RIGHT, padx=10)                 # CHÚ THÍCH: nút đăng xuất ở header
        
        # Menu
        menu_frame = tk.Frame(self.window, bg=self.menu_color, width=250)  # CHÚ THÍCH: frame menu bên trái
        menu_frame.pack(fill=tk.Y, side=tk.LEFT)        # CHÚ THÍCH: gắn menu sang trái
        
        # Nội dung
        self.content_frame = tk.Frame(self.window, bg=self.bg_color)  # CHÚ THÍCH: frame chính chứa nội dung
        self.content_frame.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)  # CHÚ THÍCH: chiếm phần còn lại bên phải
        
        self.create_menu(menu_frame)                # CHÚ THÍCH: gọi hàm tạo menu
        self.show_dashboard()                       # CHÚ THÍCH: hiển thị dashboard mặc định
    
    def create_menu(self, parent):                 # CHÚ THÍCH: tạo các nút menu điều hướng
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
        ]                                            # CHÚ THÍCH: danh sách menu item và hàm tương ứng
        
        tk.Label(
            parent,
            text="MENU CHÍNH",
            font=("Arial", 14, "bold"),
            bg=self.menu_color,
            fg=self.text_color
        ).pack(pady=20)                               # CHÚ THÍCH: tiêu đề menu
        
        for text, command in menu_items:              # CHÚ THÍCH: lặp qua danh sách menu để tạo nút
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
            btn.pack(pady=5, padx=10)               # CHÚ THÍCH: đóng gói từng nút vào menu
    
    def clear_content(self):                        # CHÚ THÍCH: xóa hết widget trong content_frame
        """Xóa nội dung frame chính"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()                       # CHÚ THÍCH: gọi destroy cho từng widget
            
   
    # =================================================================
    # CÁC HÀM VẼ GIAO DIỆN (UI-DRAWING METHODS)
    # =================================================================
    
    def create_search_bar(self, parent_frame, search_command):  # CHÚ THÍCH: tạo thanh tìm kiếm dùng chung
        """Tạo một frame chứa ô tìm kiếm (LIVE SEARCH)"""
        search_frame = ttk.Frame(parent_frame, style='Content.TFrame')  # CHÚ THÍCH: frame tìm kiếm dùng style
        search_frame.pack(fill=tk.X, pady=(0, 10))  # CHÚ THÍCH: đóng gói frame tìm kiếm
        
        ttk.Label(
            search_frame, 
            text="Tìm kiếm:", 
            style='Std.TLabel'
        ).pack(side=tk.LEFT, padx=(0, 10))           # CHÚ THÍCH: nhãn "Tìm kiếm"
        
        search_entry = ttk.Entry(
            search_frame, 
            font=("Segoe UI", 12), # Sử dụng font chuẩn
            width=40
        )
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)  # CHÚ THÍCH: Entry để nhập từ khóa
        
        # Gán sự kiện <KeyRelease> để tìm kiếm live
        search_entry.bind("<KeyRelease>", lambda e: search_command(search_entry.get()))  # CHÚ THÍCH: bind sự kiện gõ phím để live-search
        return search_entry                         # CHÚ THÍCH: trả về widget Entry để dùng sau
    
    def show_dashboard(self):                       # CHÚ THÍCH: vẽ trang chủ admin
        """Hiển thị trang chủ (Cập nhật: 4 thẻ kích thước bằng nhau tuyệt đối)"""
        self.clear_content()                        # CHÚ THÍCH: xóa content trước khi vẽ mới
        
        # 1. Tiêu đề
        tk.Label(
            self.content_frame,
            text="TRANG CHỦ ADMIN",
            font=("Arial", 20, "bold"),
            bg=self.bg_color,
            fg="#003366"
        ).pack(pady=(0, 20))                        # CHÚ THÍCH: tiêu đề trang chủ
        
        # 2. Khung chứa thống kê
        stats_frame = tk.Frame(self.content_frame, bg=self.bg_color)  # CHÚ THÍCH: frame chứa các card thống kê
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)  # CHÚ THÍCH: đóng gói với padding
        
        stats = self.dashboard_logic.get_dashboard_stats()  # CHÚ THÍCH: lấy số liệu thống kê từ logic
        
        # 3. Cấu hình lưới (QUAN TRỌNG: Thêm uniform="group_name")
        # uniform="cols": Ép tất cả các cột có cùng tag "cols" phải rộng bằng nhau
        stats_frame.grid_columnconfigure(0, weight=1, uniform="cols")  # CHÚ THÍCH: cấu hình cột 0
        stats_frame.grid_columnconfigure(1, weight=1, uniform="cols")  # CHÚ THÍCH: cấu hình cột 1
        
        # uniform="rows": Ép tất cả các hàng có cùng tag "rows" phải cao bằng nhau
        stats_frame.grid_rowconfigure(0, weight=1, uniform="rows")     # CHÚ THÍCH: cấu hình hàng 0
        stats_frame.grid_rowconfigure(1, weight=1, uniform="rows")     # CHÚ THÍCH: cấu hình hàng 1
        
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A"]           # CHÚ THÍCH: danh sách màu cho các card
        
        for i, (label, value) in enumerate(stats.items()):              # CHÚ THÍCH: lặp tạo card cho mỗi mục
            # Tạo thẻ (Card)
            card = tk.Frame(stats_frame, bg=colors[i % len(colors)], relief="raised", bd=2)  # CHÚ THÍCH: frame thẻ với màu và border
            
            # Đặt vào lưới
            card.grid(row=i//2, column=i%2, padx=20, pady=20, sticky="nsew")  # CHÚ THÍCH: đặt theo grid để chia 2x2
            
            # --- FRAME CON ĐỂ CĂN GIỮA NỘI DUNG ---
            # Frame này chứa chữ và luôn nằm giữa tâm thẻ
            content_frame = tk.Frame(card, bg=colors[i % len(colors)])  # CHÚ THÍCH: frame con đặt ở giữa card
            content_frame.place(relx=0.5, rely=0.5, anchor="center")     # CHÚ THÍCH: căn giữa bằng place
            
            # Label tiêu đề
            tk.Label(
                content_frame, 
                text=label, 
                font=("Arial", 16, "bold"), 
                bg=colors[i % len(colors)], 
                fg="white"
            ).pack(pady=5)                                             # CHÚ THÍCH: nhãn tên thống kê
            
            # Label giá trị
            tk.Label(
                content_frame, 
                text=str(value), 
                font=("Arial", 30, "bold"), 
                bg=colors[i % len(colors)], 
                fg="white"
            ).pack(pady=5)                                             # CHÚ THÍCH: nhãn giá trị lớn trên card
    
    def manage_employees(self):                      # CHÚ THÍCH: vẽ giao diện quản lý nhân viên
        """Hiển thị UI Quản lý nhân viên (ĐÃ NÂNG CẤP VỚI PANEL CHI TIẾT)"""
        self.clear_content()                         # CHÚ THÍCH: xóa content hiện tại
        
        # --- SỬA LỖI: Dùng tk.Label (thay vì ttk.Label) để nhận 'bg' và 'fg' ---
        tk.Label(
            self.content_frame,
            text="QUẢN LÝ THÔNG TIN NHÂN VIÊN",
            font=("Arial", 18, "bold"), 
            bg=self.bg_color, 
            fg="#003366"
        ).pack(pady=(0, 10))                          # CHÚ THÍCH: tiêu đề màn hình nhân viên
        
        # --- 1. KHUNG NÚT BẤM CHỨC NĂNG (Thêm, Xóa) ---
        btn_frame = tk.Frame(self.content_frame, bg=self.bg_color)  # CHÚ THÍCH: frame chứa nút chức năng
        btn_frame.pack(pady=5, fill=tk.X, padx=20)  # CHÚ THÍCH: đóng gói frame nút với padding
        
        tk.Button(
            btn_frame, text="➕ Thêm nhân viên", font=("Arial", 11), bg="#28a745", fg="white", 
            command=self.emp_logic.add_employee, cursor="hand2"
        ).pack(side=tk.LEFT, padx=5, ipady=4)         # CHÚ THÍCH: nút thêm nhân viên
        
        tk.Button(
            btn_frame, text="🗑️ Xóa nhân viên", font=("Arial", 11), bg="#dc3545", fg="white", 
            command=self.emp_logic.delete_employee, cursor="hand2"
        ).pack(side=tk.LEFT, padx=5, ipady=4)         # CHÚ THÍCH: nút xóa nhân viên
        
        # --- 2. THANH TÌM KIẾM (Live Search) ---
        # Đặt thanh tìm kiếm trong content_frame, có padding
        search_bar_container = tk.Frame(self.content_frame, bg=self.bg_color)  # CHÚ THÍCH: container cho thanh tìm kiếm
        search_bar_container.pack(fill=tk.X, padx=20)   # CHÚ THÍCH: đóng gói container
        self.search_entry = self.create_search_bar(
            search_bar_container, 
            lambda keyword: self.emp_logic.load_view(self.employee_tree, keyword)
        )                                               # CHÚ THÍCH: tạo search entry và bind hàm load view
        
        # --- 3. KHUNG BẢNG (Treeview) ---
        table_frame = ttk.Frame(self.content_frame, style='Content.TFrame')  # CHÚ THÍCH: frame cho bảng với style
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 10), padx=20)  # CHÚ THÍCH: đóng gói bảng
        
        columns = ("ID", "Họ tên", "SĐT", "Email", "Vai trò", "Trạng thái")  # CHÚ THÍCH: tên cột cho Treeview
        self.employee_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)  # CHÚ THÍCH: tạo Treeview
        
        tree = self.employee_tree                         # CHÚ THÍCH: tham chiếu ngắn cho Treeview
        tree.heading("ID", text="ID")                     # CHÚ THÍCH: đặt header cột ID
        tree.column("ID", width=50, anchor="center")     # CHÚ THÍCH: cấu hình cột ID
        tree.heading("Họ tên", text="Họ tên")            # CHÚ THÍCH: header Họ tên
        tree.column("Họ tên", width=200, anchor="w")     # CHÚ THÍCH: cấu hình cột Họ tên
        tree.heading("SĐT", text="SĐT")                  # CHÚ THÍCH: header SĐT
        tree.column("SĐT", width=120, anchor="center")   # CHÚ THÍCH: cấu hình cột SĐT
        tree.heading("Email", text="Email")              # CHÚ THÍCH: header Email
        tree.column("Email", width=200, anchor="w")      # CHÚ THÍCH: cấu hình cột Email
        tree.heading("Vai trò", text="Vai trò")         # CHÚ THÍCH: header Vai trò
        tree.column("Vai trò", width=100, anchor="center")  # CHÚ THÍCH: cấu hình cột Vai trò
        tree.heading("Trạng thái", text="Trạng thái")   # CHÚ THÍCH: header Trạng thái
        tree.column("Trạng thái", width=100, anchor="center")  # CHÚ THÍCH: cấu hình cột Trạng thái
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)  # CHÚ THÍCH: scrollbar dọc cho bảng
        tree.configure(yscrollcommand=scrollbar.set)  # CHÚ THÍCH: nối Treeview với scrollbar
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # CHÚ THÍCH: đóng gói Treeview bên trái
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)           # CHÚ THÍCH: đóng gói scrollbar bên phải
        
        tree.bind("<<TreeviewSelect>>", self.emp_logic.on_employee_select)  # CHÚ THÍCH: bind sự kiện khi chọn dòng

        # --- 4. KHUNG CHI TIẾT (Panel) ---
        details_frame = ttk.LabelFrame(self.content_frame, text="Chi tiết Nhân viên", style='Details.TLabelframe')  # CHÚ THÍCH: labelframe chứa chi tiết nhân viên
        details_frame.pack(fill=tk.X, expand=False, pady=(10, 0), padx=20)  # CHÚ THÍCH: đóng gói detail pane

        # 4.1. Cột Ảnh (Bên trái)
        image_frame = ttk.Frame(details_frame, style='Card.TFrame', width=160, height=200)  # CHÚ THÍCH: frame cho ảnh
        image_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 20), pady=10)  # CHÚ THÍCH: đóng gói image frame
        image_frame.pack_propagate(False)   # CHÚ THÍCH: không cho frame thay đổi kích thước theo nội dung

        upload_button = ttk.Button(
            image_frame, 
            text="Tải ảnh lên", 
            style='Func.TButton', 
            command=self.emp_logic.upload_image, # Gọi logic
            cursor="hand2"
        )
        upload_button.pack(side=tk.BOTTOM, pady=10)  # CHÚ THÍCH: nút tải ảnh lên
        
        self.image_label = ttk.Label(image_frame, text="Chọn NV", anchor="center", background="lightgrey", relief="groove")  # CHÚ THÍCH: label hiển thị ảnh hoặc placeholder
        self.image_label.pack(fill=tk.BOTH, expand=True, side=tk.TOP, pady=5, padx=5)  # CHÚ THÍCH: đóng gói label ảnh

        # 4.2. Cột Thông tin (Bên phải)
        info_frame = ttk.Frame(details_frame, style='Card.TFrame')  # CHÚ THÍCH: frame chứa các trường thông tin
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10, padx=(0, 20))  # CHÚ THÍCH: đóng gói

        self.details_emp_id = ttk.Label(info_frame, text="ID: (Chưa chọn)", style='Details.TLabel', font=("Segoe UI", 12))  # CHÚ THÍCH: label hiển thị ID đang chọn
        self.details_emp_id.grid(row=0, column=0, columnspan=2, pady=10, sticky="w", padx=10)  # CHÚ THÍCH: đặt bằng grid

        # Cột 1 thông tin
        ttk.Label(info_frame, text="Họ tên:", style='Details.TLabel').grid(row=1, column=0, sticky="e", padx=10, pady=5)  # CHÚ THÍCH: nhãn Họ tên
        self.details_hoten = ttk.Entry(info_frame, font=("Segoe UI", 12), width=30)  # CHÚ THÍCH: entry Họ tên
        self.details_hoten.grid(row=1, column=1, pady=5, sticky="ew")  # CHÚ THÍCH: đặt entry vào grid
        
        ttk.Label(info_frame, text="SĐT:", style='Details.TLabel').grid(row=2, column=0, sticky="e", padx=10, pady=5)  # CHÚ THÍCH: nhãn SĐT
        self.details_sdt = ttk.Entry(info_frame, font=("Segoe UI", 12), width=30)  # CHÚ THÍCH: entry SĐT
        self.details_sdt.grid(row=2, column=1, pady=5, sticky="ew")  # CHÚ THÍCH: đặt entry vào grid

        ttk.Label(info_frame, text="Email:", style='Details.TLabel').grid(row=3, column=0, sticky="e", padx=10, pady=5)  # CHÚ THÍCH: nhãn Email
        self.details_email = ttk.Entry(info_frame, font=("Segoe UI", 12), width=30)  # CHÚ THÍCH: entry Email
        self.details_email.grid(row=3, column=1, pady=5, sticky="ew")  # CHÚ THÍCH: đặt entry vào grid

        # Cột 2 thông tin
        ttk.Label(info_frame, text="Vai trò:", style='Details.TLabel').grid(row=1, column=2, sticky="e", padx=10, pady=5)  # CHÚ THÍCH: nhãn Vai trò
        self.details_vaitro = ttk.Combobox(info_frame, values=["Admin", "QuanLy", "NhanVien"], state="readonly", font=("Segoe UI", 12), width=20)  # CHÚ THÍCH: combobox vai trò
        self.details_vaitro.grid(row=1, column=3, pady=5, padx=10, sticky="ew")  # CHÚ THÍCH: đặt combobox vào grid
        
        ttk.Label(info_frame, text="Trạng thái:", style='Details.TLabel').grid(row=2, column=2, sticky="e", padx=10, pady=5)  # CHÚ THÍCH: nhãn Trạng thái
        self.details_trangthai = ttk.Combobox(info_frame, values=["HoatDong", "KhongHoatDong"], state="readonly", font=("Segoe UI", 12), width=20)  # CHÚ THÍCH: combobox trạng thái
        self.details_trangthai.grid(row=2, column=3, pady=5, padx=10, sticky="ew")  # CHÚ THÍCH: đặt combobox vào grid

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
        self.update_button.grid(row=3, column=3, pady=10, padx=10, sticky="se")  # CHÚ THÍCH: nút cập nhật mặc định disabled

        # Cấu hình grid co dãn
        info_frame.grid_columnconfigure(1, weight=1)  # CHÚ THÍCH: cho cột 1 co dãn
        info_frame.grid_columnconfigure(3, weight=1)  # CHÚ THÍCH: cho cột 3 co dãn

        # Gán sự kiện thay đổi
        self.details_hoten.bind("<KeyRelease>", self.emp_logic.check_for_changes)  # CHÚ THÍCH: bind sự kiện để bật nút lưu khi có thay đổi
        self.details_sdt.bind("<KeyRelease>", self.emp_logic.check_for_changes)
        self.details_email.bind("<KeyRelease>", self.emp_logic.check_for_changes)
        self.details_vaitro.bind("<<ComboboxSelected>>", self.emp_logic.check_for_changes)
        self.details_trangthai.bind("<<ComboboxSelected>>", self.emp_logic.check_for_changes)
        
        # Tải dữ liệu lần đầu
        self.emp_logic.load_view(self.employee_tree)  # CHÚ THÍCH: load danh sách nhân viên lên table
    
    def manage_products(self):                       # CHÚ THÍCH: giao diện quản lý sản phẩm
        """Hiển thị UI Quản lý sản phẩm (NÂNG CẤP)"""
        self.clear_content()                         # CHÚ THÍCH: xóa nội dung trước khi vẽ
        
        # Header
        ttk.Label(self.content_frame, text="QUẢN LÝ SẢN PHẨM", style='Content.TLabel').pack(pady=(0, 10))  # CHÚ THÍCH: tiêu đề
        
        # 1. Nút chức năng
        btn_frame = ttk.Frame(self.content_frame, style='Content.TFrame')  # CHÚ THÍCH: frame chứa nút
        btn_frame.pack(pady=5, fill=tk.X, padx=20)  # CHÚ THÍCH: đóng gói
        
        tk.Button(btn_frame, text="➕ Thêm Mới", font=self.font_button, bg="#28a745", fg="white", 
                  command=self.prod_logic.add_product).pack(side=tk.LEFT, padx=5, ipady=4)  # CHÚ THÍCH: nút thêm sản phẩm
        
        tk.Button(btn_frame, text="🗑️ Xóa SP", font=self.font_button, bg="#dc3545", fg="white", 
                  command=self.prod_logic.delete_product).pack(side=tk.LEFT, padx=5, ipady=4)  # CHÚ THÍCH: nút xóa sản phẩm
        
        # 2. Tìm kiếm
        container_search = tk.Frame(self.content_frame, bg=self.bg_color)  # CHÚ THÍCH: container tìm kiếm
        container_search.pack(fill=tk.X, padx=20)  # CHÚ THÍCH: đóng gói
        self.search_entry = self.create_search_bar(
            container_search,
            lambda keyword: self.prod_logic.load_products(self.product_tree, keyword)
        )                                           # CHÚ THÍCH: tạo thanh tìm kiếm cho sản phẩm

        # 3. Bảng dữ liệu
        table_frame = ttk.Frame(self.content_frame, style='Content.TFrame')  # CHÚ THÍCH: frame cho bảng
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=20)  # CHÚ THÍCH: đóng gói
        
        columns = ("Mã SP", "Tên SP", "Hãng", "Loại", "Giá bán", "Tồn kho")  # CHÚ THÍCH: cột cho bảng sản phẩm
        self.product_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)  # CHÚ THÍCH: tạo Treeview
        
        # Cấu hình cột
        self.product_tree.heading("Mã SP", text="Mã")  # CHÚ THÍCH: header cột mã SP
        self.product_tree.column("Mã SP", width=60, anchor="center")  # CHÚ THÍCH: cấu hình cột mã
        self.product_tree.heading("Tên SP", text="Tên Sản Phẩm")  # CHÚ THÍCH: header tên sản phẩm
        self.product_tree.column("Tên SP", width=250)  # CHÚ THÍCH: cấu hình cột tên
        self.product_tree.heading("Hãng", text="Hãng")  # CHÚ THÍCH: header hãng
        self.product_tree.column("Hãng", width=100, anchor="center")  # CHÚ THÍCH: cấu hình cột hãng
        self.product_tree.heading("Loại", text="Loại")  # CHÚ THÍCH: header loại
        self.product_tree.column("Loại", width=100, anchor="center")  # CHÚ THÍCH: cấu hình cột loại
        self.product_tree.heading("Giá bán", text="Giá bán")  # CHÚ THÍCH: header giá bán
        self.product_tree.column("Giá bán", width=120, anchor="e")   # CHÚ THÍCH: cấu hình cột giá bán
        self.product_tree.heading("Tồn kho", text="Tồn")  # CHÚ THÍCH: header tồn kho
        self.product_tree.column("Tồn kho", width=60, anchor="center")  # CHÚ THÍCH: cấu hình cột tồn kho

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.product_tree.yview)  # CHÚ THÍCH: scrollbar cho product_tree
        self.product_tree.configure(yscrollcommand=scrollbar.set)  # CHÚ THÍCH: nối scrollbar với tree
        self.product_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # CHÚ THÍCH: đóng gói tree
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)           # CHÚ THÍCH: đóng gói scrollbar bên phải
        
        # Sự kiện chọn dòng
        self.product_tree.bind("<ButtonRelease-1>", self.prod_logic.on_product_select)  # CHÚ THÍCH: bind khi click chọn product
        
        # 4. Panel Chi tiết
        details_frame = ttk.LabelFrame(self.content_frame, text="Thông tin chi tiết & Cập nhật", style='Details.TLabelframe')  # CHÚ THÍCH: labelframe chi tiết product
        details_frame.pack(fill=tk.X, expand=False, pady=(0, 20), padx=20)  # CHÚ THÍCH: đóng gói

        # -- Cột Ảnh (Trái) -
        image_frame = ttk.Frame(details_frame, style='Card.TFrame', width=160, height=200)  # CHÚ THÍCH: frame ảnh product
        image_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 20), pady=10)  # CHÚ THÍCH: đóng gói
        image_frame.pack_propagate(False)  # CHÚ THÍCH: không cho resize theo nội dung
        
        
        
        
        upload_button = ttk.Button(
            image_frame, 
            text="Tải ảnh lên", 
            style='Func.TButton', 
            command=self.prod_logic.upload_image, # Gọi logic
            cursor="hand2"
        )
        upload_button.pack(side=tk.BOTTOM, pady=10)  # CHÚ THÍCH: nút upload ảnh sản phẩm
        
        self.product_image_label = ttk.Label(image_frame, text="No Image", anchor="center", background="lightgrey", relief="groove")  # CHÚ THÍCH: label hiển thị ảnh sản phẩm hoặc placeholder
        self.product_image_label.pack(fill=tk.BOTH, expand=True, side=tk.TOP, pady=5, padx=5)  # CHÚ THÍCH: đóng gói label ảnh
       
        # -- Cột Thông tin (Phải) --
        info_frame = ttk.Frame(details_frame, style='Card.TFrame')  # CHÚ THÍCH: frame chứa các trường thông tin
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10, padx=(0, 20))  # CHÚ THÍCH: đóng gói

        # Hàng 1
        self.details_product_id = ttk.Label(info_frame, text="Mã: ...", font=("Segoe UI", 12, "bold"))  # CHÚ THÍCH: label hiển thị mã sản phẩm
        self.details_product_id.grid(row=0, column=0, sticky="w", padx=10, pady=5)  # CHÚ THÍCH: đặt vị trí bằng grid

        # Hàng 2: Tên & Trạng thái
        ttk.Label(info_frame, text="Tên SP:", style='Details.TLabel').grid(row=1, column=0, sticky="e", padx=5)  # CHÚ THÍCH: nhãn Tên SP
        self.details_name = ttk.Entry(info_frame, font=("Segoe UI", 11))  # CHÚ THÍCH: entry Tên SP
        self.details_name.grid(row=1, column=1, sticky="ew", padx=5)  # CHÚ THÍCH: đặt entry Tên SP
        
        ttk.Label(info_frame, text="Trạng thái:", style='Details.TLabel').grid(row=1, column=2, sticky="e", padx=5)  # CHÚ THÍCH: nhãn Trạng thái
        self.details_trangthai = ttk.Combobox(info_frame, state="readonly", font=("Segoe UI", 11))  # CHÚ THÍCH: combobox trạng thái (giá trị sẽ được cập nhật)
        self.details_trangthai.grid(row=1, column=3, sticky="ew", padx=5)  # CHÚ THÍCH: đặt combobox trạng thái

        # Hàng 3: Giá & Hãng
        ttk.Label(info_frame, text="Giá bán:", style='Details.TLabel').grid(row=2, column=0, sticky="e", padx=5)  # CHÚ THÍCH: nhãn Giá bán
        self.details_price = ttk.Entry(info_frame, font=("Segoe UI", 11))  # CHÚ THÍCH: entry giá bán
        self.details_price.grid(row=2, column=1, sticky="ew", padx=5)  # CHÚ THÍCH: đặt entry giá
        
        ttk.Label(info_frame, text="Hãng xe:", style='Details.TLabel').grid(row=2, column=2, sticky="e", padx=5)  # CHÚ THÍCH: nhãn Hãng xe
        self.details_hang = ttk.Combobox(info_frame, state="readonly", font=("Segoe UI", 11))  # CHÚ THÍCH: combobox hãng
        self.details_hang.grid(row=2, column=3, sticky="ew", padx=5)  # CHÚ THÍCH: đặt combobox hãng

        # Hàng 4: Tồn kho & Loại
        ttk.Label(info_frame, text="Tồn kho:", style='Details.TLabel').grid(row=3, column=0, sticky="e", padx=5)  # CHÚ THÍCH: nhãn Tồn kho
        self.details_stock = ttk.Entry(info_frame, font=("Segoe UI", 11))  # CHÚ THÍCH: entry tồn kho
        self.details_stock.grid(row=3, column=1, sticky="ew", padx=5)  # CHÚ THÍCH: đặt entry tồn kho

        ttk.Label(info_frame, text="Loại xe:", style='Details.TLabel').grid(row=3, column=2, sticky="e", padx=5)  # CHÚ THÍCH: nhãn Loại xe
        self.details_loai = ttk.Combobox(info_frame, state="readonly", font=("Segoe UI", 11))  # CHÚ THÍCH: combobox loại
        self.details_loai.grid(row=3, column=3, sticky="ew", padx=5)  # CHÚ THÍCH: đặt combobox loại
        
        # Nút Cập nhật
        self.update_button = tk.Button(info_frame, text="LƯU THAY ĐỔI", bg="#cccccc", fg="white", 
                                       font=("Segoe UI", 10, "bold"), state="disabled",
                                       command=self.prod_logic.update_product)
        self.update_button.grid(row=4, column=3, sticky="e", padx=5, pady=15)  # CHÚ THÍCH: nút lưu thay đổi disabled ban đầu

        # Cấu hình grid
        info_frame.columnconfigure(1, weight=1)  # CHÚ THÍCH: cột 1 co dãn
        info_frame.columnconfigure(3, weight=1)  # CHÚ THÍCH: cột 3 co dãn

        # Bind sự kiện
        self.details_name.bind("<KeyRelease>", self.prod_logic.check_for_changes)  # CHÚ THÍCH: bind detect thay đổi tên
        self.details_price.bind("<KeyRelease>", self.prod_logic.check_for_changes)  # CHÚ THÍCH: bind giá
        self.details_stock.bind("<KeyRelease>", self.prod_logic.check_for_changes)  # CHÚ THÍCH: bind tồn kho
        self.details_loai.bind("<<ComboboxSelected>>", self.prod_logic.check_for_changes)  # CHÚ THÍCH: bind combobox loại
        self.details_hang.bind("<<ComboboxSelected>>", self.prod_logic.check_for_changes)      # <--- MỚI THÊM
        self.details_trangthai.bind("<<ComboboxSelected>>", self.prod_logic.check_for_changes) # <--- MỚI THÊM
        
        # --- QUAN TRỌNG: GỌI LOGIC SAU KHI UI ĐÃ TẠO ---
        self.prod_logic.update_combobox_data() # Đổ dữ liệu vào combo  # CHÚ THÍCH: cập nhật dữ liệu cho các combobox
        self.prod_logic.load_products(self.product_tree) # Tải dữ liệu bảng  # CHÚ THÍCH: load danh sách sản phẩm lên tree
        
    def manage_parts(self):                        # CHÚ THÍCH: giao diện quản lý phụ tùng
        """Hiển thị UI Quản lý phụ tùng (NÂNG CẤP VỚI PANEL CHI TIẾT)"""
        self.clear_content()                        # CHÚ THÍCH: xóa nội dung
        
        ttk.Label(
            self.content_frame,
            text="QUẢN LÝ THÔNG TIN PHỤ TÙNG",
            style='Content.TLabel'
        ).pack(pady=(0, 10))                         # CHÚ THÍCH: tiêu đề phụ tùng

        # --- 1. KHUNG NÚT BẤM CHỨC NĂNG (Giữ lại của Admin) ---
        btn_frame = ttk.Frame(self.content_frame, style='Content.TFrame')  # CHÚ THÍCH: frame nút
        btn_frame.pack(pady=5, fill=tk.X)          # CHÚ THÍCH: đóng gói
        
        tk.Button(
            btn_frame, text="➕ Thêm PT", font=self.font_button, bg="#28a745", fg="white", 
            command=self.part_logic.add_part, cursor="hand2"
        ).pack(side=tk.LEFT, padx=5, ipady=4)        # CHÚ THÍCH: nút thêm phụ tùng
        
        tk.Button(
            btn_frame, text="🗑️ Xóa PT", font=self.font_button, bg="#dc3545", fg="white", 
            command=self.part_logic.delete_part, cursor="hand2"
        ).pack(side=tk.LEFT, padx=5, ipady=4)        # CHÚ THÍCH: nút xóa phụ tùng
        
        # --- 2. THANH TÌM KIẾM (Lấy từ quanly_window) ---
        self.search_entry = self.create_search_bar(
            self.content_frame,
            lambda keyword: self.part_logic.load_parts(self.part_tree, keyword) # Sửa tên hàm logic
        )                                           # CHÚ THÍCH: tạo thanh tìm kiếm, bind hàm load_parts

        # --- 3. KHUNG BẢNG (Treeview) ---
        table_frame = ttk.Frame(self.content_frame, style='Content.TFrame')  # CHÚ THÍCH: frame cho bảng phụ tùng
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 10))  # CHÚ THÍCH: đóng gói
        
        # Cập nhật cột để giống hệt file quanly_window
        columns = ("Mã PT", "Tên PT", "Loại", "Giá bán", "Tồn kho")  # CHÚ THÍCH: tên cột
        self.part_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)  # CHÚ THÍCH: tạo Treeview
        
        tree = self.part_tree
        tree.heading("Mã PT", text="Mã PT")               # CHÚ THÍCH: header mã PT
        tree.column("Mã PT", width=50, anchor="center")  # CHÚ THÍCH: cấu hình cột mã PT
        tree.heading("Tên PT", text="Tên PT")            # CHÚ THÍCH: header tên PT
        tree.column("Tên PT", width=250, anchor="w")     # CHÚ THÍCH: cấu hình cột tên PT
        tree.heading("Loại", text="Loại")                # CHÚ THÍCH: header loại
        tree.column("Loại", width=120, anchor="center") # CHÚ THÍCH: cấu hình cột loại
        tree.heading("Giá bán", text="Giá bán")          # CHÚ THÍCH: header giá bán
        tree.column("Giá bán", width=120, anchor="e")   # CHÚ THÍCH: cấu hình cột giá bán
        tree.heading("Tồn kho", text="Tồn kho")         # CHÚ THÍCH: header tồn kho
        tree.column("Tồn kho", width=80, anchor="center")  # CHÚ THÍCH: cấu hình cột tồn kho

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)  # CHÚ THÍCH: scrollbar cho part_tree
        tree.configure(yscrollcommand=scrollbar.set)  # CHÚ THÍCH: nối scrollbar
       
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # CHÚ THÍCH: đóng gói tree
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)           # CHÚ THÍCH: đóng gói scrollbar bên phải
        
        tree.bind("<ButtonRelease-1>", self.part_logic.on_part_select)  # CHÚ THÍCH: bind sự kiện chọn phụ tùng
        
        # --- 4. KHUNG CHI TIẾT (Panel) ---
        details_frame = ttk.LabelFrame(self.content_frame, text="Chi tiết Phụ tùng", style='Details.TLabelframe')  # CHÚ THÍCH: labelframe chi tiết phụ tùng
        details_frame.pack(fill=tk.X, expand=False, pady=(10, 0))  # CHÚ THÍCH: đóng gói

        # Cột trái: ảnh
        image_frame = ttk.Frame(details_frame, style='Card.TFrame', width=160, height=200)  # CHÚ THÍCH: frame ảnh phụ tùng
        image_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 20), pady=10)  # CHÚ THÍCH: đóng gói
        image_frame.pack_propagate(False)  # CHÚ THÍCH: không cho resize theo nội dung
        upload_button = ttk.Button(
            image_frame, text="Tải ảnh lên", style='Func.TButton',
            command=self.part_logic.upload_image, cursor="hand2"
        )
        upload_button.pack(side=tk.BOTTOM, pady=10)  # CHÚ THÍCH: nút upload ảnh phụ tùng
        self.part_image_label = ttk.Label(
            image_frame, text="Chọn PT", anchor="center", background="lightgrey", relief="groove")  # CHÚ THÍCH: label ảnh placeholder
        self.part_image_label.pack(fill=tk.BOTH, expand=True, side=tk.TOP, pady=5, padx=5)  # CHÚ THÍCH: đóng gói label ảnh

        # Cột phải: thông tin
        info_frame = ttk.Frame(details_frame, style='Card.TFrame')  # CHÚ THÍCH: frame chứa các trường thông tin
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10, padx=(0, 20))  # CHÚ THÍCH: đóng gói

        self.details_part_id = ttk.Label(info_frame, text="Mã: (Chưa chọn)", style='Details.TLabel', font=self.font_label)  # CHÚ THÍCH: label mã PT
        self.details_part_id.grid(row=0, column=0, pady=10, sticky="w", padx=10)  # CHÚ THÍCH: đặt vị trí

        # Tên PT
        ttk.Label(info_frame, text="Tên PT:", style='Details.TLabel').grid(row=1, column=0, sticky="e", padx=10, pady=5)  # CHÚ THÍCH: nhãn tên PT
        self.details_name = ttk.Entry(info_frame, font=self.font_label, width=30)  # CHÚ THÍCH: entry tên PT
        self.details_name.grid(row=1, column=1, pady=5, sticky="ew")  # CHÚ THÍCH: đặt entry

        # Giá bán
        ttk.Label(info_frame, text="Giá bán:", style='Details.TLabel').grid(row=2, column=0, sticky="e", padx=10, pady=5)  # CHÚ THÍCH: nhãn giá bán
        self.details_price = ttk.Entry(info_frame, font=self.font_label, width=30)  # CHÚ THÍCH: entry giá bán
        self.details_price.grid(row=2, column=1, pady=5, sticky="ew")  # CHÚ THÍCH: đặt entry

        # Tồn kho
        ttk.Label(info_frame, text="Tồn kho:", style='Details.TLabel').grid(row=3, column=0, sticky="e", padx=10, pady=5)  # CHÚ THÍCH: nhãn tồn kho
        self.details_stock = ttk.Entry(info_frame, font=self.font_label, width=30)  # CHÚ THÍCH: entry tồn kho
        self.details_stock.grid(row=3, column=1, pady=5, sticky="ew")  # CHÚ THÍCH: đặt entry

        # Loại phụ tùng
        ttk.Label(info_frame, text="Loại:", style='Details.TLabel').grid(row=1, column=2, sticky="e", padx=10, pady=5)  # CHÚ THÍCH: nhãn loại
        self.details_loai = ttk.Combobox(
            info_frame, values=[], state="readonly", font=self.font_label, width=20)  # CHÚ THÍCH: combobox loại (giá trị sẽ nạp sau)
        self.details_loai.grid(row=1, column=3, pady=5, padx=10, sticky="ew")  # CHÚ THÍCH: đặt combobox

        # Nút cập nhật
        self.update_button = tk.Button(
            info_frame, text="CẬP NHẬT", font=self.font_button, bg="#007bff", fg="white",
            relief="flat", padx=20, pady=10, command=self.part_logic.update_part, state="disabled", cursor=""
        )
        self.update_button.grid(row=3, column=3, pady=10, padx=10, sticky="e")  # CHÚ THÍCH: nút cập nhật PT disabled

        info_frame.grid_columnconfigure(1, weight=1)  # CHÚ THÍCH: cột 1 co dãn
        info_frame.grid_columnconfigure(3, weight=1)  # CHÚ THÍCH: cột 3 co dãn

        # Bind sự kiện
        self.details_name.bind("<KeyRelease>", self.part_logic.check_for_changes)  # CHÚ THÍCH: bind detect thay đổi tên
        self.details_price.bind("<KeyRelease>", self.part_logic.check_for_changes)  # CHÚ THÍCH: bind giá
        self.details_stock.bind("<KeyRelease>", self.part_logic.check_for_changes)  # CHÚ THÍCH: bind tồn kho
        self.details_loai.bind("<<ComboboxSelected>>", self.part_logic.check_for_changes)  # CHÚ THÍCH: bind combobox loại

        # Tải dữ liệu ban đầu
        self.part_logic.load_parts(tree)  # CHÚ THÍCH: load dữ liệu phụ tùng lên tree



    def manage_warehouse(self):                       # CHÚ THÍCH: giao diện quản lý kho (phiếu nhập)
        """Hiển thị UI Quản lý Kho (Phiếu Nhập)"""
        self.clear_content()                          # CHÚ THÍCH: xóa nội dung
        tk.Label(self.content_frame, text="QUẢN LÝ KHO - PHIẾU NHẬP", 
                 font=("Arial", 18, "bold"), bg=self.bg_color, fg="#003366").pack(pady=10)  # CHÚ THÍCH: tiêu đề
        
        btn_frame = tk.Frame(self.content_frame, bg=self.bg_color)  # CHÚ THÍCH: frame chứa nút chức năng
        btn_frame.pack(pady=10)                        # CHÚ THÍCH: đóng gói
        
        # Sử dụng self.warehouse_logic (đã khởi tạo trong __init__)
        buttons = [
            ("➕ Tạo Phiếu Nhập Mới", "#28a745", self.warehouse_logic.add_phieu_nhap),
            ("🔍 Xem Chi Tiết", "#007bff", self.warehouse_logic.view_chi_tiet),
            ("✅ Xác Nhận Phiếu", "#218838", self.warehouse_logic.confirm_phieu_nhap), 
            
            # NÚT MỚI: HỦY PHIẾU
            ("⚠️ Hủy Phiếu", "#ffc107", self.warehouse_logic.cancel_phieu_nhap),
            ("🗑️ Xóa Phiếu Nhập", "#dc3545", self.warehouse_logic.delete_phieu_nhap),
            ("🔄 Tải lại", "#17a2b8", self.manage_warehouse) 
        ]                                            # CHÚ THÍCH: danh sách nút với màu và hàm
        
        for text, bg, cmd in buttons:                 # CHÚ THÍCH: tạo và pack từng nút
            tk.Button(btn_frame, text=text, font=("Arial", 11), bg=bg, fg="white", command=cmd, width=20).pack(side=tk.LEFT, padx=5)
        
        table_frame = tk.Frame(self.content_frame, bg=self.bg_color)  # CHÚ THÍCH: frame cho tree phiếu nhập
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)  # CHÚ THÍCH: đóng gói
        
        columns = ("Mã Phiếu", "Nhà Cung Cấp", "Người Nhập", "Ngày Nhập", "Tổng Tiền", "Trạng Thái")  # CHÚ THÍCH: cột cho tree
        
        # Tạo Treeview và gán vào self.view (chính là self của admin_window)
        # Bằng cách này, file logic có thể truy cập qua self.view.phieu_nhap_tree
        self.phieu_nhap_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=25)  # CHÚ THÍCH: tạo Treeview phiếu nhập
        
        widths = {"Mã Phiếu": 80, "Nhà Cung Cấp": 250, "Người Nhập": 200, "Ngày Nhập": 150, "Tổng Tiền": 120, "Trạng Thái": 100}  # CHÚ THÍCH: dict width cho cột
        
        for col in columns: 
            self.phieu_nhap_tree.heading(col, text=col)  # CHÚ THÍCH: đặt header
            self.phieu_nhap_tree.column(col, width=widths[col], anchor="center")  # CHÚ THÍCH: cấu hình column

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.phieu_nhap_tree.yview)  # CHÚ THÍCH: scrollbar cho phieu_nhap_tree
        self.phieu_nhap_tree.configure(yscrollcommand=scrollbar.set)  # CHÚ THÍCH: nối scrollbar
        
        self.phieu_nhap_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # CHÚ THÍCH: đóng gói tree
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # CHÚ THÍCH: đóng gói scrollbar
        
        # Tải dữ liệu ban đầu
        self.warehouse_logic.load_phieu_nhap()  # CHÚ THÍCH: gọi logic để load phiếu nhập



    # Mở file: main/UI/admin_window.py
# THAY THẾ toàn bộ hàm manage_customers CŨ bằng hàm MỚI này:

    def manage_customers(self):                       # CHÚ THÍCH: giao diện quản lý khách hàng
        """Hiển thị UI Quản lý khách hàng"""
        self.clear_content()                          # CHÚ THÍCH: xóa nội dung
        tk.Label(self.content_frame, text="QUẢN LÝ KHÁCH HÀNG", font=("Arial", 18, "bold"), bg=self.bg_color, fg="#003366").pack(pady=10)  # CHÚ THÍCH: tiêu đề
        
        # --- KHUNG CHỨC NĂNG (TÌM KIẾM + NÚT BẤM) ---
        func_frame = tk.Frame(self.content_frame, bg=self.bg_color)  # CHÚ THÍCH: frame chức năng
        func_frame.pack(pady=10, fill=tk.X, padx=20)  # CHÚ THÍCH: đóng gói
        
        tk.Label(func_frame, text="Tìm kiếm (theo Tên hoặc SĐT):", bg=self.bg_color, font=("Arial", 11)).pack(side=tk.LEFT, padx=(0, 5))  # CHÚ THÍCH: nhãn hướng dẫn tìm kiếm
        
        search_entry = tk.Entry(func_frame, font=("Arial", 11), width=25)  # CHÚ THÍCH: entry nhập từ khóa
        search_entry.pack(side=tk.LEFT, padx=5, ipady=4)  # CHÚ THÍCH: đóng gói entry
        
        # Nút Tìm kiếm (gọi load_customers với từ khóa)
        tk.Button(
            func_frame, text="🔍 Tìm", font=("Arial", 10, "bold"), bg=self.btn_color, fg="white", 
            command=lambda: self.cust_logic.load_customers(search_entry.get())
        ).pack(side=tk.LEFT, padx=5, ipady=4)  # CHÚ THÍCH: nút tìm theo từ khóa
        
        # Nút Làm mới (gọi load_customers không có từ khóa)
        tk.Button(
            func_frame, text="🔄 Làm mới", font=("Arial", 10, "bold"), bg="#17a2b8", fg="white",
            command=lambda: (search_entry.delete(0, tk.END), self.cust_logic.load_customers())
        ).pack(side=tk.LEFT, padx=5, ipady=4)  # CHÚ THÍCH: nút làm mới và xóa entry
        
        # Các nút nghiệp vụ
        tk.Button(
            func_frame, text="➕ Thêm Khách Hàng", font=("Arial", 10, "bold"), bg="#28a745", fg="white", 
            command=self.cust_logic.add_customer
        ).pack(side=tk.LEFT, padx=(20, 5), ipady=4)  # CHÚ THÍCH: nút thêm khách hàng
        
        tk.Button(
            func_frame, text="✏️ Sửa Thông Tin", font=("Arial", 10, "bold"), bg="#ffc107", fg="white",
            command=self.cust_logic.edit_customer
        ).pack(side=tk.LEFT, padx=5, ipady=4)  # CHÚ THÍCH: nút sửa thông tin khách hàng
        
        tk.Button(
            func_frame, text="🗑️ Xóa Khách Hàng", font=("Arial", 10, "bold"), bg="#dc3545", fg="white",
            command=self.cust_logic.delete_customer
        ).pack(side=tk.LEFT, padx=5, ipady=4)  # CHÚ THÍCH: nút xóa khách hàng

        # --- KHUNG HIỂN THỊ DANH SÁCH ---
        table_frame = tk.Frame(self.content_frame, bg=self.bg_color)  # CHÚ THÍCH: frame chứa bảng khách hàng
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)  # CHÚ THÍCH: đóng gói
        
        columns = ("Mã", "Họ tên", "SĐT", "Email", "Địa chỉ", "Loại KH", "Ngày tạo")  # CHÚ THÍCH: cột cho customer_tree
        self.customer_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=22)  # CHÚ THÍCH: tạo Treeview khách hàng
        
        self.customer_tree.heading("Mã", text="Mã")  # CHÚ THÍCH: header Mã
        self.customer_tree.column("Mã", width=50, anchor="center")  # CHÚ THÍCH: cấu hình cột Mã
        self.customer_tree.heading("Họ tên", text="Họ tên")  # CHÚ THÍCH: header Họ tên
        self.customer_tree.column("Họ tên", width=200)  # CHÚ THÍCH: cấu hình cột Họ tên
        self.customer_tree.heading("SĐT", text="SĐT")  # CHÚ THÍCH: header SĐT
        self.customer_tree.column("SĐT", width=120, anchor="center")  # CHÚ THÍCH: cấu hình cột SĐT
        self.customer_tree.heading("Email", text="Email")  # CHÚ THÍCH: header Email
        self.customer_tree.column("Email", width=200)  # CHÚ THÍCH: cấu hình cột Email
        self.customer_tree.heading("Địa chỉ", text="Địa chỉ")  # CHÚ THÍCH: header Địa chỉ
        self.customer_tree.column("Địa chỉ", width=250)  # CHÚ THÍCH: cấu hình cột Địa chỉ
        self.customer_tree.heading("Loại KH", text="Loại KH")  # CHÚ THÍCH: header Loại KH
        self.customer_tree.column("Loại KH", width=100, anchor="center")  # CHÚ THÍCH: cấu hình cột Loại KH
        self.customer_tree.heading("Ngày tạo", text="Ngày tạo")  # CHÚ THÍCH: header Ngày tạo
        self.customer_tree.column("Ngày tạo", width=120, anchor="center")  # CHÚ THÍCH: cấu hình cột Ngày tạo

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.customer_tree.yview)  # CHÚ THÍCH: scrollbar cho customer_tree
        self.customer_tree.configure(yscrollcommand=scrollbar.set)  # CHÚ THÍCH: nối scrollbar
        
        self.customer_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # CHÚ THÍCH: đóng gói tree
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # CHÚ THÍCH: đóng gói scrollbar bên phải
        
        self.cust_logic.load_customers() # Tải dữ liệu ban đầu  # CHÚ THÍCH: gọi logic load danh sách khách hàng

   # FILE: main/UI/admin_window.py

    def manage_invoices(self):                        # CHÚ THÍCH: giao diện quản lý hóa đơn
        """Hiển thị UI Quản lý hóa đơn"""
        self.clear_content()                          # CHÚ THÍCH: xóa content
        tk.Label(self.content_frame, text="QUẢN LÝ HÓA ĐƠN", font=("Arial", 18, "bold"), bg=self.bg_color, fg="#003366").pack(pady=10)  # CHÚ THÍCH: tiêu đề

        # --- KHUNG CHỨC NĂNG (TÌM KIẾM & NÚT) ---
        func_frame = tk.Frame(self.content_frame, bg=self.bg_color)  # CHÚ THÍCH: frame cho các nút chức năng
        func_frame.pack(pady=10, fill=tk.X, padx=20)  # CHÚ THÍCH: đóng gói

        # Ô tìm kiếm
        tk.Label(func_frame, text="Tìm kiếm (Tên KH hoặc Mã HĐ):", bg=self.bg_color, font=("Arial", 11)).pack(side=tk.LEFT, padx=(0, 5))  # CHÚ THÍCH: nhãn tìm kiếm
        search_entry = tk.Entry(func_frame, font=("Arial", 11), width=30)  # CHÚ THÍCH: entry tìm kiếm
        search_entry.pack(side=tk.LEFT, padx=5, ipady=4)  # CHÚ THÍCH: đóng gói

        # Nút Tìm kiếm [MỚI]
        tk.Button(
            func_frame, text="🔍 Tìm", font=("Arial", 10, "bold"), bg=self.btn_color, fg="white", 
            command=lambda: self.invoice_logic.load_invoices(search_entry.get())
        ).pack(side=tk.LEFT, padx=5, ipady=4)  # CHÚ THÍCH: nút thực hiện tìm kiếm

        # Nút Làm mới [CẬP NHẬT]
        tk.Button(
            func_frame, text="🔄 Tải lại", font=("Arial", 10, "bold"), bg="#17a2b8", fg="white",
            command=lambda: (search_entry.delete(0, tk.END), self.invoice_logic.load_invoices())
        ).pack(side=tk.LEFT, padx=5, ipady=4)  # CHÚ THÍCH: nút tải lại và xóa entry
        
        # Nút Xem chi tiết
        tk.Button(
            func_frame, text="👁️ Xem Chi Tiết", font=("Arial", 10, "bold"), bg="#007bff", fg="white", 
            command=self.invoice_logic.show_invoice_details
        ).pack(side=tk.LEFT, padx=5, ipady=4)  # CHÚ THÍCH: nút xem chi tiết hóa đơn

        # Nút Xóa hóa đơn [MỚI]
        tk.Button(
            func_frame, text="🗑️ Xóa Hóa Đơn", font=("Arial", 10, "bold"), bg="#dc3545", fg="white", 
            command=self.invoice_logic.delete_invoice
        ).pack(side=tk.LEFT, padx=5, ipady=4)  # CHÚ THÍCH: nút xóa hóa đơn

        # --- KHUNG HIỂN THỊ DANH SÁCH ---
        table_frame = tk.Frame(self.content_frame, bg=self.bg_color)  # CHÚ THÍCH: frame cho tree invoices
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)  # CHÚ THÍCH: đóng gói

        columns = ("Mã HĐ", "Khách hàng", "Nhân viên", "Ngày lập", "Tổng tiền", "Thanh toán", "Còn nợ", "Trạng thái")  # CHÚ THÍCH: cột cho invoices
        self.invoice_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)  # CHÚ THÍCH: tạo Treeview invoices
        
        # ... (Phần định dạng cột Treeview giữ nguyên như cũ) ...
        self.invoice_tree.heading("Mã HĐ", text="Mã HĐ")  # CHÚ THÍCH: header Mã HĐ
        self.invoice_tree.column("Mã HĐ", width=60, anchor="center")  # CHÚ THÍCH: cấu hình cột
        self.invoice_tree.heading("Khách hàng", text="Khách hàng")  # CHÚ THÍCH: header Khách hàng
        self.invoice_tree.column("Khách hàng", width=200)  # CHÚ THÍCH: cấu hình cột
        self.invoice_tree.heading("Nhân viên", text="Nhân viên")  # CHÚ THÍCH: header Nhân viên
        self.invoice_tree.column("Nhân viên", width=150)  # CHÚ THÍCH: cấu hình cột
        self.invoice_tree.heading("Ngày lập", text="Ngày lập")  # CHÚ THÍCH: header Ngày lập
        self.invoice_tree.column("Ngày lập", width=130, anchor="center")  # CHÚ THÍCH: cấu hình cột
        self.invoice_tree.heading("Tổng tiền", text="Tổng tiền")  # CHÚ THÍCH: header Tổng tiền
        self.invoice_tree.column("Tổng tiền", width=120, anchor="e")  # CHÚ THÍCH: cấu hình cột
        self.invoice_tree.heading("Thanh toán", text="Thanh toán")  # CHÚ THÍCH: header Thanh toán
        self.invoice_tree.column("Thanh toán", width=120, anchor="e")  # CHÚ THÍCH: cấu hình cột
        self.invoice_tree.heading("Còn nợ", text="Còn nợ")  # CHÚ THÍCH: header Còn nợ
        self.invoice_tree.column("Còn nợ", width=100, anchor="e")  # CHÚ THÍCH: cấu hình cột
        self.invoice_tree.heading("Trạng thái", text="Trạng thái")  # CHÚ THÍCH: header Trạng thái
        self.invoice_tree.column("Trạng thái", width=100, anchor="center")  # CHÚ THÍCH: cấu hình cột

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.invoice_tree.yview)  # CHÚ THÍCH: scrollbar cho invoice_tree
        self.invoice_tree.configure(yscrollcommand=scrollbar.set)  # CHÚ THÍCH: nối scrollbar
        
        self.invoice_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # CHÚ THÍCH: đóng gói tree
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # CHÚ THÍCH: đóng gói scrollbar bên phải
        
        # Bind sự kiện enter để tìm kiếm
        search_entry.bind("<Return>", lambda e: self.invoice_logic.load_invoices(search_entry.get()))  # CHÚ THÍCH: enter trong entry -> tìm
        
        self.invoice_tree.bind("<Double-1>", lambda e: self.invoice_logic.show_invoice_details())  # CHÚ THÍCH: double click -> xem chi tiết
        
        self.invoice_logic.load_invoices()  # CHÚ THÍCH: load danh sách hóa đơn ban đầu

    def manage_promotions(self):                      # CHÚ THÍCH: giao diện quản lý khuyến mãi
        """Hiển thị UI Quản lý khuyến mãi"""
        self.clear_content()                          # CHÚ THÍCH: xóa nội dung
        tk.Label(self.content_frame, text="QUẢN LÝ KHUYẾN MÃI", font=("Arial", 18, "bold"), bg=self.bg_color, fg="#003366").pack(pady=10)  # CHÚ THÍCH: tiêu đề
        
        # --- THÊM KHUNG NÚT BẤM ---
        btn_frame = tk.Frame(self.content_frame, bg=self.bg_color)  # CHÚ THÍCH: frame nút
        btn_frame.pack(pady=10)                        # CHÚ THÍCH: đóng gói
        
        buttons = [
            ("➕ Thêm khuyến mãi", "#28a745", self.promo_logic.add_promotion),
            ("✏️ Sửa khuyến mãi", "#ffc107", self.promo_logic.edit_promotion),
            ("🗑️ Xóa khuyến mãi", "#dc3545", self.promo_logic.delete_promotion)
        ]                                            # CHÚ THÍCH: danh sách nút khuyến mãi
        
        for text, bg, cmd in buttons:
            tk.Button(btn_frame, text=text, font=("Arial", 11), bg=bg, fg="white", command=cmd, width=20).pack(side=tk.LEFT, padx=10)  # CHÚ THÍCH: tạo và pack nút
        
        # --- KHUNG HIỂN THỊ DANH SÁCH ---
        table_frame = tk.Frame(self.content_frame, bg=self.bg_color)  # CHÚ THÍCH: frame bảng khuyến mãi
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)  # CHÚ THÍCH: đóng gói
        
        columns = ("Mã", "Tên chương trình", "Loại", "Giá trị", "Từ ngày", "Đến ngày", "Trạng thái")  # CHÚ THÍCH: cột promo
        self.promo_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=22)  # CHÚ THÍCH: tạo Treeview
        
        # Định dạng các cột
        self.promo_tree.heading("Mã", text="Mã")  # CHÚ THÍCH: header Mã
        self.promo_tree.column("Mã", width=50, anchor="center")  # CHÚ THÍCH: cấu hình cột
        
        self.promo_tree.heading("Tên chương trình", text="Tên chương trình")  # CHÚ THÍCH: header tên chương trình
        self.promo_tree.column("Tên chương trình", width=300)  # CHÚ THÍCH: cấu hình cột tên
        
        self.promo_tree.heading("Loại", text="Loại")  # CHÚ THÍCH: header Loại
        self.promo_tree.column("Loại", width=100, anchor="center")  # CHÚ THÍCH: cấu hình cột
        
        self.promo_tree.heading("Giá trị", text="Giá trị")  # CHÚ THÍCH: header Giá trị
        self.promo_tree.column("Giá trị", width=120, anchor="e")  # CHÚ THÍCH: cấu hình cột
        
        self.promo_tree.heading("Từ ngày", text="Từ ngày")  # CHÚ THÍCH: header Từ ngày
        self.promo_tree.column("Từ ngày", width=100, anchor="center")  # CHÚ THÍCH: cấu hình cột
        
        self.promo_tree.heading("Đến ngày", text="Đến ngày")  # CHÚ THÍCH: header Đến ngày
        self.promo_tree.column("Đến ngày", width=100, anchor="center")  # CHÚ THÍCH: cấu hình cột
        
        self.promo_tree.heading("Trạng thái", text="Trạng thái")  # CHÚ THÍCH: header Trạng thái
        self.promo_tree.column("Trạng thái", width=100, anchor="center")  # CHÚ THÍCH: cấu hình cột

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.promo_tree.yview)  # CHÚ THÍCH: scrollbar cho promo_tree
        self.promo_tree.configure(yscrollcommand=scrollbar.set)  # CHÚ THÍCH: nối scrollbar
        
        self.promo_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # CHÚ THÍCH: đóng gói tree
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # CHÚ THÍCH: đóng gói scrollbar
        
        self.promo_logic.load_promotions() # Tải dữ liệu  # CHÚ THÍCH: gọi logic load promotions

    # Mở file: main/UI/admin_window.py
# THAY THẾ toàn bộ hàm manage_attendance CŨ bằng hàm MỚI này:

    def manage_attendance(self):                      # CHÚ THÍCH: giao diện chấm công nhân viên
        """Vẽ UI Chấm công nhân viên (Chức năng logic chính)"""
        self.clear_content()                          # CHÚ THÍCH: xóa nội dung
        
        tk.Label(
            self.content_frame,
            text="CHẤM CÔNG NHÂN VIÊN",
            font=("Arial", 18, "bold"), 
            bg=self.bg_color, 
            fg="#003366"
        ).pack(pady=(0, 10))                            # CHÚ THÍCH: tiêu đề
        
        date_frame = tk.Frame(self.content_frame, bg=self.bg_color)  # CHÚ THÍCH: frame cho chọn ngày
        date_frame.pack(pady=10, fill=tk.X, padx=20)  # CHÚ THÍCH: đóng gói
        
        tk.Label(
            date_frame,
            text="Ngày chấm công (YYYY-MM-DD):",
            font=("Arial", 11),
            bg=self.bg_color
        ).pack(side=tk.LEFT, padx=(0, 10))             # CHÚ THÍCH: nhãn ngày
        
        self.date_var = tk.StringVar(value=date.today().strftime('%Y-%m-%d'))  # CHÚ THÍCH: biến StringVar lưu ngày mặc định là hôm nay
        date_entry = tk.Entry(
            date_frame, 
            textvariable=self.date_var, 
            font=("Arial", 11), 
            width=15
        )
        date_entry.pack(side=tk.LEFT, padx=10)        # CHÚ THÍCH: entry nhập ngày
        
        tk.Button(
            date_frame,
            text="Tải dữ liệu",
            font=("Arial", 10, "bold"),
            bg=self.btn_color,
            fg="white",
            command=self.attend_logic.load_attendance, # <-- Đã đổi
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=10, ipady=4)        # CHÚ THÍCH: nút tải dữ liệu chấm công theo ngày
        
        table_frame = tk.Frame(self.content_frame, bg=self.bg_color)  # CHÚ THÍCH: frame chứa tree chấm công
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(10,0), padx=20)  # CHÚ THÍCH: đóng gói
        
        columns = ("ID", "Họ tên", "Giờ vào", "Giờ ra", "Số giờ làm", "Trạng thái")  # CHÚ THÍCH: cột cho bảng chấm công
        self.attendance_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)  # CHÚ THÍCH: tạo Treeview chấm công
        
        tree = self.attendance_tree
        for col in columns:
            tree.heading(col, text=col)              # CHÚ THÍCH: đặt header cho từng cột
            width = 150 if col == "Họ tên" else 100  # CHÚ THÍCH: đặt width khác cho cột Họ tên
            tree.column(col, width=width, anchor="center")  # CHÚ THÍCH: cấu hình cột
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)  # CHÚ THÍCH: scrollbar cho attendance_tree
        tree.configure(yscrollcommand=scrollbar.set)  # CHÚ THÍCH: nối scrollbar
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # CHÚ THÍCH: đóng gói tree
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # CHÚ THÍCH: đóng gói scrollbar
        
        btn_frame = tk.Frame(self.content_frame, bg=self.bg_color)  # CHÚ THÍCH: frame cho nút thao tác
        btn_frame.pack(pady=10)                         # CHÚ THÍCH: đóng gói
        
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
        ).pack(side=tk.LEFT, padx=5)                   # CHÚ THÍCH: nút thêm/sửa chấm công
        
        self.attend_logic.load_attendance()  # Tải dữ liệu ban đầu  # CHÚ THÍCH: load chấm công mặc định

    # Mở file: main/UI/admin_window.py
# BỔ SUNG HÀM MỚI NÀY vào gần cuối file (ví dụ: bên trên hàm manage_reports)

    def manage_warranty(self):                         # CHÚ THÍCH: giao diện quản lý bảo hành & sửa chữa
        """Vẽ Màn hình Quản lý Bảo hành & Sửa chữa (Admin)"""
        self.clear_content()                          # CHÚ THÍCH: xóa nội dung
        
        tk.Label(
            self.content_frame,
            text="QUẢN LÝ BẢO HÀNH VÀ SỬA CHỮA",
            font=("Arial", 18, "bold"),
            bg=self.bg_color,
            fg="#003366"
        ).pack(pady=10)                               # CHÚ THÍCH: tiêu đề
        
        # --- KHUNG TÌM KIẾM & CHỨC NĂNG ---
        search_frame = tk.Frame(self.content_frame, bg=self.bg_color)  # CHÚ THÍCH: frame tìm kiếm
        search_frame.pack(pady=10, fill=tk.X, padx=20)  # CHÚ THÍCH: đóng gói
        
        # Ô tìm kiếm
        tk.Label(search_frame, text="Tìm (Tên KH, SĐT, Tên Xe):", bg=self.bg_color, font=("Arial", 11)).pack(side=tk.LEFT, padx=(0, 5))  # CHÚ THÍCH: nhãn tìm kiếm
        search_entry = tk.Entry(search_frame, font=("Arial", 11), width=30)  # CHÚ THÍCH: entry tìm kiếm
        search_entry.pack(side=tk.LEFT, padx=5, ipady=4)  # CHÚ THÍCH: đóng gói
        
        # Nút Tìm kiếm
        tk.Button(
            search_frame, text="🔍 Tìm", font=("Arial", 10, "bold"), bg=self.btn_color, fg="white", 
            command=lambda: self.warranty_logic.load_all_warranties(search_entry.get())
        ).pack(side=tk.LEFT, padx=5, ipady=4)  # CHÚ THÍCH: nút gọi logic load with keyword
        
        # Nút Tải lại
        tk.Button(
            search_frame, text="🔄 Tải lại", font=("Arial", 10, "bold"), bg="#17a2b8", fg="white",
            command=lambda: (search_entry.delete(0, tk.END), self.warranty_logic.load_all_warranties())
        ).pack(side=tk.LEFT, padx=5, ipady=4)  # CHÚ THÍCH: nút tải lại and clear
        
        # === [MỚI] NÚT CHỈNH SỬA BẢO HÀNH ===
        tk.Button(
            search_frame, text="✏️ Sửa hạn BH", font=("Arial", 10, "bold"), bg="#ffc107", fg="black",
            command=self.warranty_logic.edit_warranty
        ).pack(side=tk.LEFT, padx=5, ipady=4)  # CHÚ THÍCH: nút sửa hạn bảo hành

        # --- KHUNG NỘI DUNG CHIA ĐÔI ---
        main_frame = tk.Frame(self.content_frame, bg=self.bg_color)  # CHÚ THÍCH: frame chính chia 2 cột
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)  # CHÚ THÍCH: đóng gói
        
        # --- CỘT TRÁI: DANH SÁCH PHIẾU BẢO HÀNH ---
        left_frame = tk.Frame(main_frame, bg=self.bg_color)  # CHÚ THÍCH: frame bên trái
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))  # CHÚ THÍCH: đóng gói

        warranty_frame = tk.LabelFrame(left_frame, text="Tất cả Phiếu Bảo Hành", 
                                       font=("Arial", 12, "bold"), bg="white", padx=10, pady=10)  # CHÚ THÍCH: labelframe danh sách bảo hành
        warranty_frame.pack(fill=tk.BOTH, expand=True)  # CHÚ THÍCH: đóng gói
        
        # Treeview Phiếu Bảo Hành
        cols_warranty = ("ID", "Khách Hàng", "SĐT", "Tên Xe", "Từ Ngày", "Đến Ngày", "Trạng Thái")  # CHÚ THÍCH: cột cho tree warranty
        self.warranty_tree = ttk.Treeview(warranty_frame, columns=cols_warranty, show="headings", height=15)  # CHÚ THÍCH: tạo Treeview
        
        for col in cols_warranty: 
            self.warranty_tree.heading(col, text=col)  # CHÚ THÍCH: đặt header cho từng cột
        
        self.warranty_tree.column("ID", width=40, anchor="center")  # CHÚ THÍCH: cấu hình cột ID
        self.warranty_tree.column("Khách Hàng", width=150)         # CHÚ THÍCH: cấu hình cột Khách Hàng
        self.warranty_tree.column("SĐT", width=100, anchor="center")  # CHÚ THÍCH: cấu hình cột SĐT
        self.warranty_tree.column("Tên Xe", width=150)             # CHÚ THÍCH: cấu hình cột Tên Xe
        self.warranty_tree.column("Từ Ngày", width=90, anchor="center")  # CHÚ THÍCH: cấu hình cột Từ ngày
        self.warranty_tree.column("Đến Ngày", width=90, anchor="center")  # CHÚ THÍCH: cấu hình cột Đến ngày
        self.warranty_tree.column("Trạng Thái", width=110, anchor="center") # CHÚ THÍCH: cấu hình cột Trạng thái
        
        self.warranty_tree.bind("<<TreeviewSelect>>", self.warranty_logic.on_warranty_select)  # CHÚ THÍCH: bind chọn phiếu -> show history
        
        self.warranty_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # CHÚ THÍCH: đóng gói tree
        scrollbar_left = ttk.Scrollbar(warranty_frame, orient="vertical", command=self.warranty_tree.yview)  # CHÚ THÍCH: scrollbar trái
        self.warranty_tree.configure(yscrollcommand=scrollbar_left.set)  # CHÚ THÍCH: nối scrollbar
        scrollbar_left.pack(side=tk.RIGHT, fill=tk.Y)  # CHÚ THÍCH: pack scrollbar
        
        # Nút xóa Phiếu Bảo Hành
        tk.Button(
            left_frame, text="🗑️ Xóa Phiếu Bảo Hành", font=("Arial", 10, "bold"), bg="#dc3545", fg="white",
            command=self.warranty_logic.delete_warranty_entry
        ).pack(pady=10)  # CHÚ THÍCH: nút xóa phiếu bảo hành

        # --- CỘT PHẢI: LỊCH SỬ SỬA CHỮA (Giữ nguyên) ---
        right_frame = tk.Frame(main_frame, bg=self.bg_color)  # CHÚ THÍCH: frame bên phải
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))  # CHÚ THÍCH: đóng gói
        
        history_frame = tk.LabelFrame(right_frame, text="Lịch Sử Sửa Chữa (của phiếu đã chọn)", 
                                   font=("Arial", 12, "bold"), bg="white", padx=10, pady=10)  # CHÚ THÍCH: labelframe lịch sử sửa chữa
        history_frame.pack(fill=tk.BOTH, expand=True)  # CHÚ THÍCH: đóng gói
        
        cols_history = ("ID LS", "Ngày Sửa", "Mô Tả Lỗi", "Người Xử Lý", "Chi Phí", "Trạng Thái")  # CHÚ THÍCH: cột history
        self.history_tree = ttk.Treeview(history_frame, columns=cols_history, show="headings", height=15)  # CHÚ THÍCH: tạo Treeview lịch sử
        
        self.history_tree.heading("ID LS", text="ID")  # CHÚ THÍCH: header ID lịch sử
        self.history_tree.column("ID LS", width=40, anchor="center")  # CHÚ THÍCH: cấu hình cột
        self.history_tree.heading("Ngày Sửa", text="Ngày Sửa")  # CHÚ THÍCH: header ngày sửa
        self.history_tree.column("Ngày Sửa", width=90, anchor="center")  # CHÚ THÍCH: cấu hình cột
        self.history_tree.heading("Mô Tả Lỗi", text="Mô Tả Lỗi")  # CHÚ THÍCH: header mô tả lỗi
        self.history_tree.column("Mô Tả Lỗi", width=200)  # CHÚ THÍCH: cấu hình cột
        self.history_tree.heading("Người Xử Lý", text="Người Xử Lý")  # CHÚ THÍCH: header người xử lý
        self.history_tree.column("Người Xử Lý", width=120)  # CHÚ THÍCH: cấu hình cột
        self.history_tree.heading("Chi Phí", text="Chi Phí")  # CHÚ THÍCH: header chi phí
        self.history_tree.column("Chi Phí", width=90, anchor="e")  # CHÚ THÍCH: cấu hình cột
        self.history_tree.heading("Trạng Thái", text="Trạng Thái")  # CHÚ THÍCH: header trạng thái
        self.history_tree.column("Trạng Thái", width=90, anchor="center")  # CHÚ THÍCH: cấu hình cột
        
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # CHÚ THÍCH: đóng gói history tree
        scrollbar_right = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_tree.yview)  # CHÚ THÍCH: scrollbar phải
        self.history_tree.configure(yscrollcommand=scrollbar_right.set)  # CHÚ THÍCH: nối scrollbar phải
        scrollbar_right.pack(side=tk.RIGHT, fill=tk.Y)  # CHÚ THÍCH: pack scrollbar phải

        # Nút xóa Lịch Sử Sửa Chữa
        tk.Button(
            right_frame, text="🗑️ Xóa Lịch Sử", font=("Arial", 10, "bold"), bg="#ffc107", fg="black",
            command=self.warranty_logic.delete_history_entry
        ).pack(pady=10)  # CHÚ THÍCH: nút xóa mục lịch sử
        
        # Tải dữ liệu ban đầu
        self.warranty_logic.load_all_warranties()  # CHÚ THÍCH: load toàn bộ phiếu bảo hành ban đầu

    def show_reports(self):                          # CHÚ THÍCH: giao diện báo cáo
        """Hiển thị UI Báo cáo thống kê"""
        self.clear_content()                         # CHÚ THÍCH: xóa nội dung
        tk.Label(self.content_frame, text="BÁO CÁO THỐNG KÊ", font=("Arial", 18, "bold"), bg=self.bg_color).pack(pady=10)  # CHÚ THÍCH: tiêu đề
        
        report_frame = tk.Frame(self.content_frame, bg=self.bg_color)  # CHÚ THÍCH: frame chứa các nút báo cáo
        report_frame.pack(pady=20)                    # CHÚ THÍCH: đóng gói
        
        reports = [
            ("📊 Doanh thu theo tháng", self.report_logic.report_revenue),
            ("📦 Tồn kho sản phẩm", self.report_logic.report_inventory),
            ("👥 Hiệu suất nhân viên", self.report_logic.report_employee_performance),
            ("🏆 Top sản phẩm bán chạy", self.report_logic.report_top_products),
            
            ("💰 Công nợ khách hàng", self.report_logic.report_debt)
        ]                                            # CHÚ THÍCH: danh sách report và hàm tương ứng
        row, col = 0, 0
        for text, command in reports:
            btn = tk.Button(report_frame, text=text, font=("Arial", 12), bg=self.btn_color, fg="white", width=30, height=3, command=command)
            btn.grid(row=row, column=col, padx=15, pady=15)  # CHÚ THÍCH: đặt các nút báo cáo theo grid
            col += 1
            if col > 1: col, row = 0, row + 1  # CHÚ THÍCH: chuyển dòng khi đã có 2 cột