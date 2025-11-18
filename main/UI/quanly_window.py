# =================================================================
# FILE: quanly_window.py
# MÔ TẢ: Class QuanLy - Giao diện quản lý (ĐÃ SỬA LỖI LAYOUT PANEL CHI TIẾT)
# =================================================================

# Import thư viện tkinter (thư viện GUI chuẩn của Python) và gán cho nó tên 'tk'
import tkinter as tk
# Import 2 thành phần cụ thể từ tkinter:
# 1. messagebox: Dùng để hiển thị các hộp thoại thông báo (lỗi, cảnh báo,...)
# 2. ttk: (themed tkinter widgets) Cung cấp các widget (nút, nhãn,...) có giao diện hiện đại hơn tk
from tkinter import messagebox, ttk
# Import lớp DatabaseConnection từ file 'database_connection.py' (do mình tự định nghĩa)
from database_connection import DatabaseConnection
# Import 2 lớp 'datetime' và 'date' từ thư viện 'datetime' để làm việc với ngày giờ
from datetime import datetime, date

# --- 1. IMPORT TẤT CẢ 10 LỚP LOGIC ---
# (Các lớp này chứa logic nghiệp vụ, tách biệt khỏi giao diện)

# Import logic cho chức năng Chấm công
from Function.function_QuanLy.quanly_attendance_logic import QuanLyAttendanceLogic
# Import logic cho chức năng Hệ thống (đăng xuất, đóng cửa sổ)
from Function.function_QuanLy.quanly_system_logic import QuanLySystemLogic
# Import logic cho chức năng Xem Nhân viên (tải, cập nhật, tìm kiếm...)
from Function.function_QuanLy.quanly_employee_view_logic import QuanLyEmployeeViewLogic
# Import logic cho chức năng Xem Sản phẩm
from Function.function_QuanLy.quanly_product_view_logic import QuanLyProductViewLogic
# Import logic cho chức năng Xem Phụ tùng
from Function.function_QuanLy.quanly_part_view_logic import QuanLyPartViewLogic
# Import logic cho chức năng Xem Kho (Phiếu nhập)
from Function.function_QuanLy.quanly_warehouse_view_logic import QuanLyWarehouseViewLogic
# Import logic cho chức năng Xem Khách hàng
from Function.function_QuanLy.quanly_customer_view_logic import QuanLyCustomerViewLogic
# Import logic cho chức năng Xem Hóa đơn
from Function.function_QuanLy.quanly_invoice_view_logic import QuanLyInvoiceViewLogic
# Import logic cho chức năng Xem Báo cáo
from Function.function_QuanLy.quanly_report_view_logic import QuanLyReportViewLogic
# Import logic cho Trang chủ (Dashboard)
from Function.function_QuanLy.quanly_dashboard_logic import QuanLyDashboardLogic


# Bắt đầu định nghĩa lớp (class) QuanLy, đây là cửa sổ giao diện chính
class QuanLy:
    # Hàm khởi tạo (constructor), được gọi tự động khi một đối tượng QuanLy được tạo
    def __init__(self, user_info):
        """Khởi tạo cửa sổ Quản lý"""
        # Tạo cửa sổ tkinter chính và gán vào 'self.window'
        self.window = tk.Tk()
        # Đặt tiêu đề cho cửa sổ, f-string để chèn tên người dùng vào tiêu đề
        self.window.title(f"QUẢN LÝ - {user_info['HoTen']}")
        # Đặt kích thước ban đầu của cửa sổ (chiều rộng x chiều cao)
        self.window.geometry("1200x700")
        # Đặt trạng thái cửa sổ là 'zoomed' (phóng to tối đa) khi mở
        self.window.state('zoomed')
        
        # Lưu thông tin người dùng (truyền vào từ lúc đăng nhập) vào biến nội bộ 'self.user_info'
        self.user_info = user_info
        
        # --- BỘ FONT CHỮ --- (Định nghĩa các font để dùng thống nhất)
        self.font_title = ("Segoe UI", 18, "bold")      # Font cho tiêu đề cửa sổ
        self.font_header = ("Segoe UI", 16, "bold")     # Font cho tiêu đề các mục (TRANG CHỦ, QUẢN LÝ NV...)
        self.font_menu_title = ("Segoe UI", 14, "bold") # Font cho chữ "MENU CHÍNH"
        self.font_menu_btn = ("Segoe UI", 11, "bold")   # Font cho các nút trong menu (Trang chủ, Xem NV...)
        self.font_label = ("Segoe UI", 12)              # Font cho các nhãn (label) và ô nhập liệu (entry)
        self.font_info = ("Segoe UI", 12)               # Font cho thông tin (tương tự font_label)
        self.font_button = ("Segoe UI", 10, "bold")     # Font cho các nút chức năng (Tìm, Cập nhật...)
        self.font_card_label = ("Segoe UI", 12, "bold") # Font cho nhãn trên thẻ (card) ở Trang chủ (vd: "Tổng nhân viên")
        self.font_card_value = ("Segoe UI", 24, "bold") # Font cho giá trị (số liệu) trên thẻ Trang chủ

        # Màu sắc (Định nghĩa các mã màu để dùng thống nhất)
        self.bg_color = "#E6F2FF"    # Màu nền chính của vùng nội dung (xanh nhạt)
        self.menu_color = "#5F9EA0"  # Màu nền của menu bên trái và header
        self.btn_color = "#4682B4"   # Màu nền mặc định của các nút menu
        self.text_color = "#FFFFFF"  # Màu chữ (trắng) dùng trên nền màu (menu, header, nút)
        self.header_fg = "#003366"   # Màu chữ của tiêu đề trong vùng nội dung (xanh đậm)
        
        # Database
        # Tạo một đối tượng (instance) từ lớp DatabaseConnection
        self.db = DatabaseConnection()
        # Gọi phương thức connect() của đối tượng đó để mở kết nối đến CSDL
        self.db.connect()
        
        # --- 2. KHỞI TẠO TẤT CẢ 10 LỚP LOGIC ---
        # Tạo một đối tượng cho mỗi lớp logic, truyền 'self' (chính là cửa sổ QuanLy) vào.
        # Điều này cho phép các lớp logic có thể truy cập và điều khiển các widget (vd: self.employee_tree)
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
        
        # Gọi hàm setup_styles (định nghĩa bên dưới) để cấu hình giao diện cho các widget TTK
        self.setup_styles()
        # Gọi hàm setup_ui (định nghĩa bên dưới) để vẽ các thành phần giao diện chính
        self.setup_ui()
        # Bắt sự kiện khi người dùng nhấn nút 'X' để đóng cửa sổ.
        # Thay vì đóng ngay, nó sẽ gọi hàm 'on_closing' trong 'logic_system' (để hỏi xác nhận hoặc đóng DB)
        self.window.protocol("WM_DELETE_WINDOW", self.logic_system.on_closing)
        # Bắt đầu vòng lặp sự kiện chính của tkinter. Cửa sổ sẽ hiện lên và chờ hành động của người dùng
        self.window.mainloop()

    # Hàm định nghĩa các Style (giao diện) cho các widget TTK
    def setup_styles(self):
        """Định nghĩa style cho các widget TTK"""
        # Tạo một đối tượng Style
        s = ttk.Style()
        try:
            # Thử sử dụng theme 'vista' (giao diện giống Windows)
            s.theme_use('vista')
        except tk.TclError:
            # Nếu không có theme 'vista' (ví dụ trên Linux), thì bỏ qua (dùng theme mặc định)
            pass 

        # Cấu hình style tên 'Content.TFrame': đặt màu nền là bg_color
        s.configure('Content.TFrame', background=self.bg_color)
        # Cấu hình style 'Content.TLabel': dùng cho tiêu đề các tab
        s.configure('Content.TLabel', background=self.bg_color, foreground=self.header_fg, font=self.font_header)
        # Cấu hình style 'Menu.TFrame': dùng cho khung menu bên trái
        s.configure('Menu.TFrame', background=self.menu_color)
        # Cấu hình style 'Menu.TLabel': dùng cho chữ "MENU CHÍNH"
        s.configure('Menu.TLabel', background=self.menu_color, foreground=self.text_color, font=self.font_menu_title)
        
        # Cấu hình style 'Std.TLabel' (Standard Label): dùng cho các nhãn thông thường
        s.configure('Std.TLabel', background=self.bg_color, font=self.font_label)
        # Cấu hình style 'Card.TFrame': dùng cho các thẻ ở trang chủ và panel chi tiết
        s.configure('Card.TFrame', background="white", relief="raised", borderwidth=2)
        # Cấu hình style 'Func.TButton' (Function Button): dùng cho các nút chức năng (Tìm, Tải ảnh...)
        s.configure('Func.TButton', font=self.font_button, padding=5)
        
        # Style cho LabelFrame nền trắng (dùng cho Detail Pane)
        # Cấu hình style 'Details.TLabelframe': cho khung chi tiết (nền trắng, đệm 10)
        s.configure('Details.TLabelframe', background="white", padding=10)
        # Cấu hình style cho *tiêu đề* (Label) của 'Details.TLabelframe'
        s.configure('Details.TLabelframe.Label', background="white", font=self.font_label, foreground="#003366")
        
        # Style cho Label bên trong LabelFrame (nền trắng)
        # Cấu hình style 'Details.TLabel': cho các nhãn (Họ tên:, SĐT:) bên trong khung chi tiết
        s.configure('Details.TLabel', background="white", font=self.font_label)
        
        # Cấu hình style cho Treeview (Bảng)
        s.configure("Treeview", 
                    rowheight=28,                  # Chiều cao mỗi dòng 28px
                    font=("Segoe UI", 10),          # Font chữ nội dung bảng
                    background="white",            # Nền chung
                    fieldbackground="white")       # Nền của các ô
        # Cấu hình style cho Tiêu đề (Heading) của Treeview
        s.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        # Thay đổi layout của Treeview để bỏ viền xám xung quanh
        s.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})]) 

    # Hàm thiết lập giao diện chính (chia 3 khu vực: Header, Menu, Content)
    def setup_ui(self):
        """Thiết lập giao diện (Sử dụng TTK)"""
        # Header (tk.Frame) - Dùng tk.Frame (thay vì ttk.Frame) để set màu nền (bg) dễ dàng
        # Tạo một Frame (khung) cho phần header (đầu trang)
        header_frame = tk.Frame(self.window, bg=self.menu_color, height=60)
        # Đặt (pack) header_frame vào cửa sổ:
        # fill=tk.X: lấp đầy theo chiều ngang
        # side=tk.TOP: nằm ở cạnh trên cùng
        # ipady=5: thêm đệm bên trong (internal padding) 5px theo chiều dọc
        header_frame.pack(fill=tk.X, side=tk.TOP, ipady=5)
        
        # Tạo một Nhãn (Label) chứa tiêu đề hệ thống
        tk.Label(
            header_frame,  # Nằm trong header_frame
            text="HỆ THỐNG QUẢN LÝ CỬA HÀNG XE MÁY - QUẢN LÝ", # Nội dung text
            font=self.font_title,     # Dùng font tiêu đề
            bg=self.menu_color,     # Màu nền (giống header)
            fg=self.text_color      # Màu chữ (trắng)
        ).pack(side=tk.LEFT, padx=20) # Đặt nhãn này: căn bên trái, đệm ngoài (padx) 20px
        
        # Tạo nhãn "Xin chào: [Tên]"
        tk.Label(
            header_frame, # Nằm trong header_frame
            text=f"Xin chào: {self.user_info['HoTen']}", # Lấy tên từ user_info
            font=self.font_label,  # Dùng font nhãn
            bg=self.menu_color,  # Màu nền
            fg=self.text_color   # Màu chữ
        ).pack(side=tk.RIGHT, padx=20) # Đặt nhãn này: căn bên phải, đệm ngoài 20px
        
        # Tạo nút "Đăng xuất" (dùng tk.Button để set màu nền bg)
        tk.Button(
            header_frame, # Nằm trong header_frame
            text="Đăng xuất", # Chữ trên nút
            font=self.font_button, # Dùng font nút
            bg="#DC143C",          # Màu nền (đỏ)
            fg=self.text_color,    # Màu chữ (trắng)
            command=self.logic_system.logout, # Khi click, gọi hàm 'logout' từ 'logic_system'
            relief="flat",         # Kiểu viền (phẳng)
            padx=10,               # Đệm trong ngang
            pady=5,                # Đệm trong dọc
            cursor="hand2"         # Đổi con trỏ thành hình bàn tay khi di chuột vào
        ).pack(side=tk.RIGHT, padx=10) # Đặt nút này: căn bên phải, đệm ngoài 10px
        
        # Menu (ttk.Frame) - Dùng ttk.Frame để dùng style 'Menu.TFrame'
        # Tạo Frame cho menu bên trái
        menu_frame = ttk.Frame(self.window, style='Menu.TFrame', width=250)
        # Đặt menu_frame: lấp đầy chiều dọc (fill=tk.Y), căn bên trái (side=tk.LEFT)
        menu_frame.pack(fill=tk.Y, side=tk.LEFT)
        # Ngăn không cho menu_frame tự co lại theo nội dung (giữ nguyên độ rộng 250px)
        menu_frame.pack_propagate(False)
        
        # Nội dung (ttk.Frame) - Khu vực chính để hiển thị các tab
        # Tạo Frame cho nội dung, dùng style 'Content.TFrame'
        self.content_frame = ttk.Frame(self.window, style='Content.TFrame', padding=20)
        # Đặt content_frame:
        # fill=tk.BOTH: lấp đầy cả ngang và dọc
        # expand=True: tự động mở rộng để lấp đầy không gian còn lại
        # side=tk.RIGHT: nằm bên phải (sau khi menu đã nằm bên trái)
        self.content_frame.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)
        
        # Gọi hàm create_menu (định nghĩa bên dưới) và truyền menu_frame vào để vẽ các nút
        self.create_menu(menu_frame)
        # Gọi hàm show_dashboard (định nghĩa bên dưới) để hiển thị Trang chủ ngay khi mở
        self.show_dashboard()
    
    # Hàm tạo các nút menu
    def create_menu(self, parent): # 'parent' chính là 'menu_frame'
        """Tạo menu điều hướng (Dùng tk.Button để giữ màu)"""
        # Tạo một danh sách (list) chứa các (tuple)
        # Mỗi tuple gồm: (Tên nút, Hàm được gọi khi click)
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
        
        # Tạo nhãn "MENU CHÍNH"
        ttk.Label(
            parent,         # Nằm trong 'parent' (menu_frame)
            text="MENU CHÍNH", # Nội dung
            style='Menu.TLabel' # Dùng style 'Menu.TLabel' (nền xanh, chữ trắng)
        ).pack(pady=20) # Đặt nhãn, đệm ngoài 20px trên dưới
        
        # Vòng lặp 'for' duyệt qua từng mục trong 'menu_items'
        for text, command in menu_items:
            # Tạo một nút (tk.Button) cho mỗi mục
            btn = tk.Button(
                parent,       # Nằm trong 'parent' (menu_frame)
                text=text,    # Lấy text (ví dụ: "🏠 Trang chủ")
                font=self.font_menu_btn, # Dùng font nút menu
                bg=self.btn_color,     # Màu nền (xanh)
                fg=self.text_color,    # Màu chữ (trắng)
                command=command,       # Lấy hàm (ví dụ: self.show_dashboard)
                cursor="hand2",        # Con trỏ bàn tay
                anchor="w",            # Căn chữ trong nút về bên trái (West)
                width=25,              # Đặt chiều rộng cố định
                relief="flat",         # Viền phẳng
                padx=10,               # Đệm trong ngang
                pady=8                 # Đệm trong dọc
            )
            # Định nghĩa màu khi di chuột qua
            hover_color = "#5A9BD8"
            # Gán sự kiện <Enter> (khi di chuột vào)
            # 'lambda e, b=btn, c=hover_color:' là cách để truyền 'btn' và 'hover_color' vào hàm
            btn.bind("<Enter>", lambda e, b=btn, c=hover_color: b.config(bg=c))
            # Gán sự kiện <Leave> (khi di chuột ra)
            btn.bind("<Leave>", lambda e, b=btn, c=self.btn_color: b.config(bg=c))
            # Đặt nút vào menu, đệm 4px trên dưới, 15px trái phải, lấp đầy chiều ngang
            btn.pack(pady=4, padx=15, fill=tk.X)
    
    # Hàm xóa tất cả widget trong 'content_frame' (để chuẩn bị vẽ tab mới)
    def clear_content(self):
        """Xóa nội dung frame"""
        # Vòng lặp qua tất cả các 'con' (widget con) trong 'self.content_frame'
        for widget in self.content_frame.winfo_children():
            # Hủy (xóa) widget đó
            widget.destroy()
    
    # Hàm tiện ích tạo thanh tìm kiếm (dùng cho nhiều tab)
    def create_search_bar(self, parent_frame, search_command):
        """Tạo một frame chứa ô tìm kiếm (LIVE SEARCH)"""
        # Tạo một Frame con (nằm trong parent_frame) để chứa nhãn và ô tìm kiếm
        search_frame = ttk.Frame(parent_frame, style='Content.TFrame')
        # Đặt search_frame, lấp đầy chiều ngang
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Tạo nhãn "Tìm kiếm:"
        ttk.Label(
            search_frame, 
            text="Tìm kiếm:", 
            style='Std.TLabel' # Dùng style nhãn chuẩn
        ).pack(side=tk.LEFT, padx=(0, 10)) # Đặt bên trái
        
        # Tạo ô nhập liệu (Entry)
        search_entry = ttk.Entry(
            search_frame, 
            font=self.font_label, 
            width=40
        )
        # Đặt ô nhập liệu: bên trái, lấp đầy ngang (fill=tk.X), tự mở rộng (expand=True)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Gán sự kiện <KeyRelease> (xảy ra khi nhả 1 phím)
        # Khi sự kiện xảy ra, gọi hàm 'lambda'
        # Hàm lambda sẽ gọi 'search_command' (truyền từ ngoài vào) và
        # truyền nội dung hiện tại của ô 'search_entry' (search_entry.get()) vào hàm đó.
        search_entry.bind("<KeyRelease>", lambda e: search_command(search_entry.get()))
        # Trả về ô search_entry để có thể dùng (ví dụ: gán vào self.search_entry)
        return search_entry

    # =================================================================
    # CÁC HÀM VẼ GIAO DIỆN (UI-DRAWING METHODS)
    # (Các hàm này được gọi khi nhấn nút menu)
    # =================================================================

    # Hàm vẽ Trang chủ (Dashboard)
    def show_dashboard(self):
        """Hiển thị trang chủ (ĐÃ NÂNG CẤP VỚI CÁC THẺ)"""
        # Xóa nội dung cũ
        self.clear_content()
        
        # Vẽ tiêu đề "TRANG CHỦ QUẢN LÝ"
        ttk.Label(
            self.content_frame,
            text="TRANG CHỦ QUẢN LÝ",
            style='Content.TLabel' # Dùng style tiêu đề nội dung
        ).pack(pady=(0, 20), anchor="center") # Đặt giữa
        
        # Tạo một Frame để chứa 4 thẻ (card) thống kê
        stats_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
        # Đặt stats_frame, lấp đầy và tự mở rộng
        stats_frame.pack(fill=tk.BOTH, expand=True)
        
        # Gọi hàm get_dashboard_stats() từ 'logic_dashboard' để lấy số liệu
        stats = self.logic_dashboard.get_dashboard_stats()
        # Định nghĩa 4 màu cho 4 thẻ
        colors = ["#17A2B8", "#28A745", "#FFC107", "#DC3545"]
        
        # Tạo 4 thẻ (dùng tk.Frame để set màu nền 'bg')
        card1 = tk.Frame(stats_frame, bg=colors[0], width=250, height=150, relief="raised", bd=2)
        # Đặt thẻ 1 vào 'stats_frame' dùng layout 'grid' (lưới)
        # row=0, column=0: Hàng 0, Cột 0
        # sticky="nsew": Tự co giãn theo 4 hướng (Bắc-Nam-Đông-Tây)
        card1.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        card2 = tk.Frame(stats_frame, bg=colors[1], width=250, height=150, relief="raised", bd=2)
        card2.grid(row=0, column=1, padx=20, pady=20, sticky="nsew") # Hàng 0, Cột 1
        card3 = tk.Frame(stats_frame, bg=colors[2], width=250, height=150, relief="raised", bd=2)
        card3.grid(row=1, column=0, padx=20, pady=20, sticky="nsew") # Hàng 1, Cột 0
        card4 = tk.Frame(stats_frame, bg=colors[3], width=250, height=150, relief="raised", bd=2)
        card4.grid(row=1, column=1, padx=20, pady=20, sticky="nsew") # Hàng 1, Cột 1
        
        # Cấu hình grid của 'stats_frame' để các cột (0, 1) và hàng (0, 1)
        # tự co dãn với tỉ lệ (weight) là 1
        stats_frame.grid_columnconfigure(0, weight=1)
        stats_frame.grid_columnconfigure(1, weight=1)
        stats_frame.grid_rowconfigure(0, weight=1)
        stats_frame.grid_rowconfigure(1, weight=1)

        # Thêm nội dung cho Thẻ 1
        tk.Label(card1, text="Tổng nhân viên", font=self.font_card_label, bg=colors[0], fg="white").pack(pady=(20, 5))
        # Lấy giá trị từ 'stats', nếu không có key "Tổng nhân viên" thì mặc định là 0
        tk.Label(card1, text=stats.get("Tổng nhân viên", 0), font=self.font_card_value, bg=colors[0], fg="white").pack(pady=5)
        # Ngăn thẻ co lại theo nội dung (giữ kích thước 250x150)
        card1.pack_propagate(False)

        # Thêm nội dung cho Thẻ 2
        tk.Label(card2, text="Tổng khách hàng", font=self.font_card_label, bg=colors[1], fg="white").pack(pady=(20, 5))
        tk.Label(card2, text=stats.get("Tổng khách hàng", 0), font=self.font_card_value, bg=colors[1], fg="white").pack(pady=5)
        card2.pack_propagate(False)

        # Thêm nội dung cho Thẻ 3
        tk.Label(card3, text="Nhân viên có mặt", font=self.font_card_label, bg=colors[2], fg="#343A40").pack(pady=(20, 5))
        tk.Label(card3, text=stats.get("Nhân viên có mặt", 0), font=self.font_card_value, bg=colors[2], fg="#343A40").pack(pady=5)
        card3.pack_propagate(False)

        # Thêm nội dung cho Thẻ 4
        tk.Label(card4, text="Doanh thu hôm nay", font=self.font_card_label, bg=colors[3], fg="white").pack(pady=(20, 5))
        tk.Label(card4, text=stats.get("Doanh thu hôm nay", "0 VNĐ"), font=self.font_card_value, bg=colors[3], fg="white").pack(pady=5)
        card4.pack_propagate(False)

    
    # =================================================================
    # HÀM XEM NHÂN VIÊN (ĐÃ SỬA LỖI LAYOUT)
    # =================================================================
    # Hàm vẽ tab Xem Nhân viên
    def view_employees(self):
        """Xem danh sách nhân viên (NÂNG CẤP: Live Search + Panel Chi Tiết)"""
        # Xóa nội dung cũ
        self.clear_content()
        
        # Vẽ tiêu đề "QUẢN LÝ THÔNG TIN NHÂN VIÊN"
        ttk.Label(
            self.content_frame,
            text="QUẢN LÝ THÔNG TIN NHÂN VIÊN",
            style='Content.TLabel'
        ).pack(pady=(0, 10))
        
        # --- 1. THANH TÌM KIẾM (Live Search) ---
        # Gọi hàm create_search_bar để tạo thanh tìm kiếm
        self.search_entry = self.create_search_bar(
            self.content_frame, # Đặt trong content_frame
            # Truyền vào một hàm lambda: khi gõ phím, nó sẽ gọi 'load_view' của 'view_employee'
            # với 2 tham số: (bảng treeview, từ khóa gõ vào)
            lambda keyword: self.view_employee.load_view(self.employee_tree, keyword)
        )
        
        # --- 2. KHUNG BẢNG (Treeview) ---
        # Tạo Frame chứa bảng
        table_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
        # Đặt table_frame, lấp đầy và tự mở rộng (expand=True, quan trọng)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 10)) 
        
        # Định nghĩa tên các cột
        columns = ("ID", "Họ tên", "SĐT", "Email", "Vai trò", "Trạng thái")
        # Tạo Treeview (bảng), gán vào 'self.employee_tree' để các hàm logic có thể truy cập
        self.employee_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        
        # Gán tree = self.employee_tree (cho ngắn gọn)
        tree = self.employee_tree
        # Đặt tiêu đề và kích thước cho từng cột
        tree.heading("ID", text="ID")
        tree.column("ID", width=50, anchor="center") # anchor="center": căn giữa
        tree.heading("Họ tên", text="Họ tên")
        tree.column("Họ tên", width=200, anchor="w") # anchor="w": căn trái (West)
        tree.heading("SĐT", text="SĐT")
        tree.column("SĐT", width=120, anchor="center")
        tree.heading("Email", text="Email")
        tree.column("Email", width=200, anchor="w")
        tree.heading("Vai trò", text="Vai trò")
        tree.column("Vai trò", width=100, anchor="center")
        tree.heading("Trạng thái", text="Trạng thái")
        tree.column("Trạng thái", width=100, anchor="center")
        
        # Tạo thanh cuộn dọc (Scrollbar)
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        # Liên kết thanh cuộn với bảng
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Đặt bảng: căn trái, lấp đầy
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # Đặt thanh cuộn: căn phải, lấp đầy chiều dọc
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Gán sự kiện <<TreeviewSelect>> (khi người dùng click chọn 1 dòng)
        # Khi sự kiện xảy ra, gọi hàm 'on_employee_select' từ 'view_employee' (logic)
        tree.bind("<<TreeviewSelect>>", self.view_employee.on_employee_select)
        # Gọi 'load_view' từ logic để tải dữ liệu vào 'tree' ngay khi vẽ xong
        self.view_employee.load_view(tree)

        # --- 3. KHUNG CHI TIẾT (Panel) ---
        # Tạo một LabelFrame (khung có tiêu đề) dùng style 'Details.TLabelframe' (nền trắng)
        details_frame = ttk.LabelFrame(self.content_frame, text="Chi tiết Nhân viên", style='Details.TLabelframe')
        # Đặt details_frame: lấp đầy ngang, KHÔNG tự mở rộng (expand=False)
        details_frame.pack(fill=tk.X, expand=False, pady=(10, 0))

        # --- SỬA LỖI LAYOUT BẮT ĐẦU TỪ ĐÂY ---
        # (Layout này chia details_frame làm 2 cột: Ảnh và Thông tin)

        # 3.1. Cột Ảnh (Bên trái)
        # Tạo Frame chứa ảnh, kích thước cố định 160x200
        image_frame = ttk.Frame(details_frame, style='Card.TFrame', width=160, height=200)
        # Đặt image_frame: căn trái
        image_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 20), pady=10)
        # Ngăn co giãn
        image_frame.pack_propagate(False) 

        # Nút Tải ảnh lên (PACK TRƯỚC VÀ ĐẶT Ở DƯỚI CÙNG)
        upload_button = ttk.Button(
            image_frame, # Nằm trong image_frame
            text="Tải ảnh lên", 
            style='Func.TButton', 
            command=self.view_employee.upload_image, # Gọi hàm upload_image từ logic
            cursor="hand2"
        )
        # Đặt nút: căn dưới cùng (side=tk.BOTTOM)
        upload_button.pack(side=tk.BOTTOM, pady=10)
        
        # Label để giữ ảnh (PACK SAU, NÓ SẼ CHIẾM PHẦN CÒN LẠI)
        # Tạo nhãn để hiển thị ảnh, gán vào 'self.image_label'
        self.image_label = ttk.Label(image_frame, text="Chọn NV", anchor="center", background="lightgrey", relief="groove")
        # Đặt nhãn: lấp đầy (fill=tk.BOTH), tự mở rộng (expand=True), nằm bên trên (side=tk.TOP)
        self.image_label.pack(fill=tk.BOTH, expand=True, side=tk.TOP, pady=5, padx=5)

        # 3.2. Cột Thông tin (Ở giữa) - (PACK CUỐI CÙNG ĐỂ NÓ TỰ GIÃN RA)
        # Tạo Frame chứa các ô thông tin
        info_frame = ttk.Frame(details_frame, style='Card.TFrame')
        # Đặt info_frame: căn trái (sau image_frame), lấp đầy và tự mở rộng (expand=True)
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10, padx=(0, 20)) 

        # Sử dụng layout 'grid' bên trong 'info_frame'

        # ID (Chỉ hiển thị)
        self.details_emp_id = ttk.Label(info_frame, text="ID: (Chưa chọn)", style='Details.TLabel', font=self.font_label)
        # Đặt tại Hàng 0, Cột 0, kéo dài 2 cột (columnspan=2), căn trái (sticky="w")
        self.details_emp_id.grid(row=0, column=0, columnspan=2, pady=10, sticky="w", padx=10)

        # --- CỘT 1 THÔNG TIN (Họ tên, SĐT, Email) ---
        ttk.Label(info_frame, text="Họ tên:", style='Details.TLabel').grid(row=1, column=0, sticky="e", padx=10, pady=5) # sticky="e": căn phải (East)
        self.details_hoten = ttk.Entry(info_frame, font=self.font_label, width=30)
        self.details_hoten.grid(row=1, column=1, pady=5, sticky="ew") # sticky="ew": co giãn ngang (East-West)
        
        ttk.Label(info_frame, text="SĐT:", style='Details.TLabel').grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.details_sdt = ttk.Entry(info_frame, font=self.font_label, width=30)
        self.details_sdt.grid(row=2, column=1, pady=5, sticky="ew")

        ttk.Label(info_frame, text="Email:", style='Details.TLabel').grid(row=3, column=0, sticky="e", padx=10, pady=5)
        self.details_email = ttk.Entry(info_frame, font=self.font_label, width=30)
        self.details_email.grid(row=3, column=1, pady=5, sticky="ew")

        # --- CỘT 2 THÔNG TIN (Vai trò, Trạng thái, Nút Cập nhật) ---
        ttk.Label(info_frame, text="Vai trò:", style='Details.TLabel').grid(row=1, column=2, sticky="e", padx=10, pady=5)
        # Tạo Combobox (hộp chọn)
        self.details_vaitro = ttk.Combobox(info_frame, values=["Nhân Viên", "Quản Lý"], state="readonly", font=self.font_label, width=20)
        self.details_vaitro.grid(row=1, column=3, pady=5, padx=10, sticky="ew")
        
        ttk.Label(info_frame, text="Trạng thái:", style='Details.TLabel').grid(row=2, column=2, sticky="e", padx=10, pady=5)
        self.details_trangthai = ttk.Combobox(info_frame, values=["Hoạt động", "Không hoạt động"], state="readonly", font=self.font_label, width=20)
        self.details_trangthai.grid(row=2, column=3, pady=5, padx=10, sticky="ew")

        # --- NÚT CẬP NHẬT (CHUYỂN VÀO ĐÂY) ---
        self.update_button = tk.Button( # Dùng tk.Button để set màu bg
            info_frame,
            text="CẬP NHẬT",
            font=self.font_button,
            bg="#007bff", # Màu xanh
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            command=self.view_employee.update_employee, # Gọi hàm update_employee từ logic
            state="disabled", # Ban đầu bị vô hiệu hóa
            cursor="" # Con trỏ mặc định (khi bị vô hiệu hóa)
        )
        # Đặt nút ở Hàng 3, Cột 3
        # sticky="se": căn góc dưới-phải (South-East) của ô grid
        self.update_button.grid(row=3, column=3, pady=10, padx=10, sticky="se")

        # Cấu hình grid co dãn
        # Cho phép Cột 1 (chứa Entry) co dãn (weight=1)
        info_frame.grid_columnconfigure(1, weight=1)
        # Cho phép Cột 3 (chứa Combobox) co dãn (weight=1)
        info_frame.grid_columnconfigure(3, weight=1)

        # GỌI HÀM KIỂM TRA THAY ĐỔI
        # Gán sự kiện cho các ô nhập liệu/chọn
        # Khi có thay đổi (gõ phím, chọn), gọi hàm 'check_for_changes' từ logic
        # (Hàm này sẽ kiểm tra và bật (enable) nút CẬP NHẬT)
        self.details_hoten.bind("<KeyRelease>", self.view_employee.check_for_changes)
        self.details_sdt.bind("<KeyRelease>", self.view_employee.check_for_changes)
        self.details_email.bind("<KeyRelease>", self.view_employee.check_for_changes)
        self.details_vaitro.bind("<<ComboboxSelected>>", self.view_employee.check_for_changes)
        self.details_trangthai.bind("<<ComboboxSelected>>", self.view_employee.check_for_changes)
        
        # --- KẾT THÚC SỬA LỖI LAYOUT ---

    
    # Hàm vẽ tab Xem Sản phẩm
    # (Cấu trúc hàm này tương tự hàm view_employees)
    def view_products(self):
        self.clear_content() # Xóa nội dung cũ
        # Vẽ tiêu đề "QUẢN LÝ THÔNG TIN SẢN PHẨM"
        ttk.Label(
            self.content_frame,
            text="QUẢN LÝ THÔNG TIN SẢN PHẨM",
            style='Content.TLabel'
        ).pack(pady=(0, 10))
        # Tạo thanh Live Search
        self.search_entry = self.create_search_bar(
            self.content_frame,
            # Khi gõ, gọi 'load_view' của 'view_product' (logic SP)
            lambda keyword: self.view_product.load_view(self.product_tree, keyword)
        )

        # --- BẢNG SẢN PHẨM ---
        table_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 10))
        columns = ("Mã SP", "Tên SP", "Hãng", "Loại", "Giá bán", "Tồn kho")
        # Tạo Treeview, gán vào 'self.product_tree'
        self.product_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        # Cấu hình các cột
        for col in columns:
            self.product_tree.heading(col, text=col)
            self.product_tree.column(col, width=120, anchor="center")
        self.product_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # Tạo và liên kết thanh cuộn
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.product_tree.yview)
        self.product_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # Gán sự kiện khi click (nhả chuột trái), gọi 'on_product_select' từ logic
        self.product_tree.bind("<ButtonRelease-1>", self.view_product.on_product_select)
        # Tải dữ liệu ban đầu
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
        # Nhãn hiển thị ảnh SP, gán vào 'self.product_image_label'
        self.product_image_label = ttk.Label(
            image_frame, text="Chọn SP", anchor="center", background="lightgrey", relief="groove")
        self.product_image_label.pack(fill=tk.BOTH, expand=True, side=tk.TOP, pady=5, padx=5)

        # Cột phải: các trường thông tin sản phẩm (dùng layout 'grid')
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
        self.update_button = tk.Button( # Dùng tk.Button để set màu
            info_frame, text="CẬP NHẬT", font=self.font_button, bg="#007bff", fg="white",
            relief="flat", padx=20, pady=10, command=self.view_product.update_product, state="disabled", cursor=""
        )
        self.update_button.grid(row=3, column=3, pady=10, padx=10, sticky="e")  # Căn phải (East)

        # Cấu hình co dãn cho cột 1 và 3
        info_frame.grid_columnconfigure(1, weight=1)
        info_frame.grid_columnconfigure(3, weight=1)

        # Bind sự kiện cho các trường để kiểm tra thay đổi
        self.details_name.bind("<KeyRelease>", self.view_product.check_for_changes)
        self.details_price.bind("<KeyRelease>", self.view_product.check_for_changes)
        self.details_stock.bind("<KeyRelease>", self.view_product.check_for_changes)
        self.details_hang.bind("<<ComboboxSelected>>", self.view_product.check_for_changes)
        self.details_loai.bind("<<ComboboxSelected>>", self.view_product.check_for_changes)

    
    # Hàm vẽ tab Xem Phụ tùng
    # (Cấu trúc tương tự view_products)
    def view_parts(self):
        self.clear_content() # Xóa nội dung cũ
        # Vẽ tiêu đề "QUẢN LÝ THÔNG TIN PHỤ TÙNG"
        ttk.Label(
            self.content_frame,
            text="QUẢN LÝ THÔNG TIN PHỤ TÙNG",
            style='Content.TLabel'
        ).pack(pady=(0, 10))
        # Tạo thanh Live Search
        self.search_entry = self.create_search_bar(
            self.content_frame,
            # Khi gõ, gọi 'load_view' của 'view_part' (logic PT)
            lambda keyword: self.view_part.load_view(self.part_tree, keyword)
        )

        # BẢNG PHỤ TÙNG
        table_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 10))
        columns = ("Mã PT", "Tên PT", "Loại", "Giá bán", "Tồn kho")
        # Tạo Treeview, gán vào 'self.part_tree'
        self.part_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        # Cấu hình các cột
        for col in columns:
            self.part_tree.heading(col, text=col)
            self.part_tree.column(col, width=120, anchor="center")
        self.part_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # Tạo và liên kết thanh cuộn
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.part_tree.yview)
        self.part_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # Gán sự kiện click, gọi 'on_part_select' từ logic
        self.part_tree.bind("<ButtonRelease-1>", self.view_part.on_part_select)
        # Tải dữ liệu ban đầu
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
        # Nhãn hiển thị ảnh PT, gán vào 'self.part_image_label'
        self.part_image_label = ttk.Label(
            image_frame, text="Chọn PT", anchor="center", background="lightgrey", relief="groove")
        self.part_image_label.pack(fill=tk.BOTH, expand=True, side=tk.TOP, pady=5, padx=5)

        # Khung thông tin (dùng 'grid')
        info_frame = ttk.Frame(details_frame, style='Card.TFrame')
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10, padx=(0, 20))

        # Mã PT (chỉ hiển thị)
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
        # Lấy danh sách 'values' (các loại PT) từ 'loaipt_dict' trong 'view_part' (logic)
        self.details_loai = ttk.Combobox(
            info_frame, values=list(self.view_part.loaipt_dict.keys()), state="readonly", font=self.font_label, width=20)
        self.details_loai.grid(row=1, column=3, pady=5, padx=10, sticky="ew")

        # NÚT CẬP NHẬT
        self.update_button = tk.Button( # Dùng tk.Button để set màu
            info_frame, text="CẬP NHẬT", font=self.font_button, bg="#007bff", fg="white",
            relief="flat", padx=20, pady=10, command=self.view_part.update_part, state="disabled", cursor=""
        )
        self.update_button.grid(row=3, column=3, pady=10, padx=10, sticky="e") # Căn phải (East)

        # Cấu hình co dãn cột 1 và 3
        info_frame.grid_columnconfigure(1, weight=1)
        info_frame.grid_columnconfigure(3, weight=1)

        # Bind các trường để kiểm tra thay đổi
        self.details_name.bind("<KeyRelease>", self.view_part.check_for_changes)
        self.details_price.bind("<KeyRelease>", self.view_part.check_for_changes)
        self.details_stock.bind("<KeyRelease>", self.view_part.check_for_changes)
        self.details_loai.bind("<<ComboboxSelected>>", self.view_part.check_for_changes)

    
    # Hàm vẽ tab Xem Kho (Phiếu nhập)
    # (Hàm này đã đổi tên, chỉ xem, không có panel chi tiết, tìm kiếm bằng nút 'Tìm')
    def show_warehouse_view(self): # <--- SỬA LỖI 2: Đổi tên hàm
        """Xem kho (Phiếu nhập kho)"""
        self.clear_content() # Xóa nội dung cũ
        # Vẽ tiêu đề "DANH SÁCH PHIẾU NHẬP KHO (CHỈ XEM)"
        ttk.Label(
            self.content_frame,
            text="DANH SÁCH PHIẾU NHẬP KHO (CHỈ XEM)",
            style='Content.TLabel'
        ).pack(pady=(0, 10))

        # Tạo Frame chứa các nút chức năng (Tìm kiếm, Xem chi tiết)
        func_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
        func_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Nhãn "Tìm kiếm:"
        ttk.Label(func_frame, text="Tìm kiếm:", style='Std.TLabel').pack(side=tk.LEFT, padx=(0, 10))
        # Ô nhập liệu (không phải live search)
        search_entry = ttk.Entry(func_frame, font=self.font_label, width=40)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Nút "Tìm"
        ttk.Button(
            func_frame, text="Tìm", style='Func.TButton', 
            # Khi click, gọi 'load_view' của 'view_warehouse' và lấy nội dung từ 'search_entry'
            command=lambda: self.view_warehouse.load_view(self.warehouse_tree, search_entry.get()),
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=(10, 0))
        
        # Nút "🔍 Xem chi tiết"
        ttk.Button(
            func_frame, text="🔍 Xem chi tiết", style='Func.TButton', 
            # Khi click, gọi 'show_warehouse_details' từ logic
            command=self.view_warehouse.show_warehouse_details,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=(10, 0))
        
        # Gán sự kiện phím <Return> (Enter) trên ô tìm kiếm, chạy lệnh 'Tìm'
        search_entry.bind("<Return>", lambda e: self.view_warehouse.load_view(self.warehouse_tree, search_entry.get()))

        # Khung chứa bảng
        table_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
        # Đặt bảng, lấp đầy và co giãn (expand=True)
        table_frame.pack(fill=tk.BOTH, expand=True)

        # Định nghĩa các cột
        columns = ("Mã Phiếu", "Nhà Cung Cấp", "Người Nhập", "Ngày Nhập", "Tổng Tiền", "Trạng Thái")
        # Tạo Treeview, gán vào 'self.warehouse_tree'
        self.warehouse_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=25)
        
        # Cấu hình các cột
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
        tree.column("Tổng Tiền", width=150, anchor="e") # anchor="e": căn phải (East)
        tree.heading("Trạng Thái", text="Trạng Thái")
        tree.column("Trạng Thái", width=100, anchor="center")

        # Tạo và liên kết thanh cuộn
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Gán sự kiện <Double-1> (Double click chuột trái)
        # Khi double click, gọi 'show_warehouse_details' từ logic
        tree.bind("<Double-1>", lambda e: self.view_warehouse.show_warehouse_details())

        # Tải dữ liệu ban đầu
        self.view_warehouse.load_view(tree)
    
    # Hàm vẽ tab Xem Khách hàng
    # (Chỉ xem, có Live Search)
    def view_customers(self):
        """Xem khách hàng"""
        self.clear_content() # Xóa nội dung cũ
        # Vẽ tiêu đề "DANH SÁCH KHÁCH HÀNG (CHỈ XEM)"
        ttk.Label(
            self.content_frame,
            text="DANH SÁCH KHÁCH HÀNG (CHỈ XEM)",
            style='Content.TLabel'
        ).pack(pady=(0, 10))

        # Tạo thanh Live Search
        self.search_entry = self.create_search_bar(
            self.content_frame, 
            # Khi gõ, gọi 'load_view' của 'view_customer'
            lambda keyword: self.view_customer.load_view(self.customer_tree, keyword)
        )

        # Khung chứa bảng
        table_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
        table_frame.pack(fill=tk.BOTH, expand=True)

        # Định nghĩa các cột
        columns = ("Mã KH", "Họ Tên", "SĐT", "Địa Chỉ", "Loại KH")
        # Tạo Treeview, gán vào 'self.customer_tree'
        self.customer_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=25)
        
        # Cấu hình các cột
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

        # Tạo và liên kết thanh cuộn
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Tải dữ liệu ban đầu
        self.view_customer.load_view(tree)
    
    # Hàm vẽ tab Xem Hóa đơn
    # (Tương tự Xem Kho, chỉ xem, tìm kiếm bằng nút 'Tìm')
    def view_invoices(self):
        """Xem hóa đơn (Sử dụng VIEW)"""
        self.clear_content() # Xóa nội dung cũ
        # Vẽ tiêu đề "DANH SÁCH HÓA ĐƠN (CHỈ XEM)"
        ttk.Label(
            self.content_frame,
            text="DANH SÁCH HÓA ĐƠN (CHỈ XEM)",
            style='Content.TLabel'
        ).pack(pady=(0, 10))

        # Tạo Frame chứa các nút chức năng
        func_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
        func_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Nhãn "Tìm kiếm:"
        ttk.Label(func_frame, text="Tìm kiếm:", style='Std.TLabel').pack(side=tk.LEFT, padx=(0, 10))
        # Ô nhập liệu tìm kiếm
        search_entry = ttk.Entry(func_frame, font=self.font_label, width=40)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Nút "Tìm"
        ttk.Button(
            func_frame, text="Tìm", style='Func.TButton', 
            # Khi click, gọi 'load_view' của 'view_invoice'
            command=lambda: self.view_invoice.load_view(self.invoice_tree, search_entry.get()),
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=(10, 0))
        
        # Nút "🔍 Xem chi tiết"
        ttk.Button(
            func_frame, text="🔍 Xem chi tiết", style='Func.TButton', 
            # Khi click, gọi 'show_invoice_details' từ logic
            command=self.view_invoice.show_invoice_details,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=(10, 0))
        
        # Gán phím <Return> (Enter)
        search_entry.bind("<Return>", lambda e: self.view_invoice.load_view(self.invoice_tree, search_entry.get()))

        # Khung chứa bảng
        table_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
        table_frame.pack(fill=tk.BOTH, expand=True)

        # Định nghĩa các cột
        columns = ("Mã HĐ", "Ngày Lập", "Khách Hàng", "Nhân Viên", "Tổng Tiền", "Còn Nợ", "Trạng Thái")
        # Tạo Treeview, gán vào 'self.invoice_tree'
        self.invoice_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=25)
        
        # Cấu hình các cột
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

        # Tạo và liên kết thanh cuộn
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Gán sự kiện Double Click
        tree.bind("<Double-1>", lambda e: self.view_invoice.show_invoice_details())

        # Tải dữ liệu ban đầu
        self.view_invoice.load_view(tree)
    
    # Hàm vẽ tab Chấm công
    def manage_attendance(self):
        """Vẽ UI Chấm công nhân viên (Chức năng logic chính)"""
        self.clear_content() # Xóa nội dung cũ
        
        # Vẽ tiêu đề "CHẤM CÔNG NHÂN VIÊN"
        ttk.Label(
            self.content_frame,
            text="CHẤM CÔNG NHÂN VIÊN",
            style='Content.TLabel'
        ).pack(pady=(0, 10))
        
        # Tạo Frame chứa ô chọn ngày và nút "Tải"
        date_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
        date_frame.pack(pady=10, fill=tk.X)
        
        # Nhãn "Ngày chấm công:"
        ttk.Label(
            date_frame,
            text="Ngày chấm công:",
            style='Std.TLabel',
            font=self.font_label
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # Tạo một biến 'StringVar' (biến đặc biệt của tkinter)
        # Gán giá trị mặc định là ngày hôm nay (định dạng 'YYYY-MM-DD')
        self.date_var = tk.StringVar(value=date.today().strftime('%Y-%m-%d'))
        # Tạo ô Entry để hiển thị ngày
        date_entry = ttk.Entry(
            date_frame, 
            textvariable=self.date_var, # Liên kết ô Entry với 'self.date_var'
            font=self.font_label, 
            width=15
        )
        date_entry.pack(side=tk.LEFT, padx=10)
        
        # Nút "Tải dữ liệu"
        ttk.Button(
            date_frame,
            text="Tải dữ liệu",
            style='Func.TButton',
            # Khi click, gọi 'load_attendance' từ logic
            command=self.logic_attendance.load_attendance,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=10)
        
        # Khung chứa bảng
        table_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(10,0))
        
        # Định nghĩa các cột
        columns = ("ID", "Họ tên", "Giờ vào", "Giờ ra", "Số giờ làm", "Trạng thái")
        # Tạo Treeview, gán vào 'self.attendance_tree'
        self.attendance_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        
        # Cấu hình các cột
        tree = self.attendance_tree
        for col in columns:
            tree.heading(col, text=col)
            # Dùng toán tử 3 ngôi: nếu cột là "Họ tên" thì rộng 150, ngược lại 100
            width = 150 if col == "Họ tên" else 100
            tree.column(col, width=width, anchor="center")
        
        # Tạo và liên kết thanh cuộn
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Tạo Frame chứa nút "Chấm công"
        btn_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
        btn_frame.pack(pady=10)
        
        # Tạo nút "✓ Chấm công" (dùng tk.Button để set màu xanh)
        tk.Button(
            btn_frame,
            text="✓ Chấm công",
            font=self.font_button,
            bg="#28a745", # Màu xanh lá
            fg="white",
            # Khi click, gọi 'add_attendance' từ logic
            command=self.logic_attendance.add_attendance,
            relief="flat",
            padx=10,
            pady=5,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=5)
        
        # Tải dữ liệu chấm công của ngày hôm nay ngay khi mở tab
        self.logic_attendance.load_attendance()
    
    # Hàm vẽ tab Xem Báo cáo
    def view_reports(self):
        """Xem báo cáo (Ví dụ: Tồn kho)"""
        self.clear_content() # Xóa nội dung cũ
        # Vẽ tiêu đề "BÁO CÁO TỒN KHO SẢN PHẨM (CHỈ XEM)"
        ttk.Label(
            self.content_frame,
            text="BÁO CÁO TỒN KHO SẢN PHẨM (CHỈ XEM)",
            style='Content.TLabel'
        ).pack(pady=(0, 20))

        # Khung chứa bảng
        table_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
        table_frame.pack(fill=tk.BOTH, expand=True)

        # Định nghĩa các cột
        columns = ("Mã SP", "Tên SP", "Hãng", "Loại", "Tồn kho", "Giá trị tồn kho")
        # Tạo Treeview, gán vào 'self.report_tree'
        self.report_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=25)
        
        # Cấu hình các cột
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

        # Tạo và liên kết thanh cuộn
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Tải dữ liệu báo cáo (gọi 'load_view' từ 'view_report' (logic))
        self.view_report.load_view(tree)