# =================================================================
# FILE: quanly_window.py
# MÔ TẢ: Class QuanLy - Giao diện quản lý (CHỈ CÓ UI, ĐÃ DỌN DẸP)
# =================================================================

import tkinter as tk
from tkinter import messagebox, ttk
from database_connection import DatabaseConnection
from datetime import datetime, date

# --- 1. IMPORT LỚP LOGIC ---
from Function.function_QuanLy.quanly_logic import QuanLyLogic

# --- KHÔNG CẦN IMPORT LOGIN TẠI ĐÂY ---

class QuanLy:
    def __init__(self, user_info):
        """Khởi tạo cửa sổ Quản lý"""
        self.window = tk.Tk()
        self.window.title(f"QUẢN LÝ - {user_info['HoTen']}")
        self.window.geometry("1200x700")
        self.window.state('zoomed')
        
        self.user_info = user_info
        
        # Màu sắc
        self.bg_color = "#E6F2FF"
        self.menu_color = "#5F9EA0"
        self.btn_color = "#4682B4"
        self.text_color = "#FFFFFF"
        
        # Database
        self.db = DatabaseConnection()
        self.db.connect()
        
        # --- 2. KHỞI TẠO LỚP LOGIC ---
        self.logic = QuanLyLogic(self)
        
        self.setup_ui()
        self.window.protocol("WM_DELETE_WINDOW", self.logic.on_closing)
        self.window.mainloop()
    
    def setup_ui(self):
        """Thiết lập giao diện (Chỉ UI)"""
        # Header
        header_frame = tk.Frame(self.window, bg=self.menu_color, height=60)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        
        tk.Label(
            header_frame,
            text="HỆ THỐNG QUẢN LÝ CỬA HÀNG XE MÁY - QUẢN LÝ",
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
            command=self.logic.logout 
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
            ("👥 Xem nhân viên", self.view_employees),
            ("🏍️ Xem sản phẩm", self.view_products),
            ("🔧 Xem phụ tùng", self.view_parts),
            ("📦 Xem kho", self.view_warehouse),
            ("👤 Xem khách hàng", self.view_customers),
            ("📄 Xem hóa đơn", self.view_invoices),
            ("⏰ Chấm công", self.manage_attendance), # Hàm vẽ UI
            ("📊 Xem báo cáo", self.view_reports)
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
        """Xóa nội dung frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    # =================================================================
    # CÁC HÀM VẼ GIAO DIỆN (UI-DRAWING METHODS)
    # =================================================================

    def show_dashboard(self):
        """Hiển thị trang chủ"""
        self.clear_content()
        
        tk.Label(
            self.content_frame,
            text="TRANG CHỦ QUẢN LÝ",
            font=("Arial", 20, "bold"),
            bg=self.bg_color,
            fg="#003366"
        ).pack(pady=20)
        
        info_frame = tk.Frame(self.content_frame, bg="white", bd=2, relief=tk.RAISED)
        info_frame.pack(pady=30, padx=50, fill=tk.BOTH, expand=True)
        
        tk.Label(
            info_frame,
            text="THÔNG TIN TÀI KHOẢN",
            font=("Arial", 16, "bold"),
            bg="white"
        ).pack(pady=20)
        
        info_text = f"""
        Họ tên: {self.user_info['HoTen']}
        Vai trò: Quản lý
        
        QUYỀN HẠN:
        ✓ Xem thông tin tất cả các module
        ✓ Chấm công cho nhân viên
        ✗ Không có quyền chỉnh sửa dữ liệu
        
        Ngày hôm nay: {datetime.now().strftime('%d/%m/%Y')}
        """
        
        tk.Label(
            info_frame,
            text=info_text,
            font=("Arial", 12),
            bg="white",
            justify=tk.LEFT
        ).pack(pady=20)
    
    def view_employees(self):
        """Xem danh sách nhân viên (chỉ xem)"""
        self.clear_content()
        
        tk.Label(
            self.content_frame,
            text="DANH SÁCH NHÂN VIÊN (CHỈ XEM)",
            font=("Arial", 18, "bold"),
            bg=self.bg_color,
            fg="#003366"
        ).pack(pady=10)
        
        table_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        columns = ("ID", "Họ tên", "SĐT", "Email", "Vai trò", "Trạng thái")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=25)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Logic tải dữ liệu đơn giản, giữ lại tại UI
        query = """
            SELECT MaNguoiDung, HoTen, SoDienThoai, Email, VaiTro, TrangThai
            FROM NguoiDung
            WHERE VaiTro = 'NhanVien'
            ORDER BY MaNguoiDung
        """
        employees = self.db.fetch_all(query)
        
        if employees:
            for emp in employees:
                tree.insert("", tk.END, values=(
                    emp['MaNguoiDung'],
                    emp['HoTen'],
                    emp['SoDienThoai'] or "",
                    emp['Email'] or "",
                    emp['VaiTro'],
                    emp['TrangThai']
                ))
    
    def view_products(self):
        """Xem sản phẩm"""
        self.clear_content()
        tk.Label(
            self.content_frame,
            text="DANH SÁCH SẢN PHẨM (CHỈ XEM)",
            font=("Arial", 18, "bold"),
            bg=self.bg_color
        ).pack(pady=20)
    
    def view_parts(self):
        """Xem phụ tùng"""
        self.clear_content()
        tk.Label(
            self.content_frame,
            text="DANH SÁCH PHỤ TÙNG (CHỈ XEM)",
            font=("Arial", 18, "bold"),
            bg=self.bg_color
        ).pack(pady=20)
    
    def view_warehouse(self):
        """Xem kho"""
        self.clear_content()
        tk.Label(
            self.content_frame,
            text="THÔNG TIN KHO (CHỈ XEM)",
            font=("Arial", 18, "bold"),
            bg=self.bg_color
        ).pack(pady=20)
    
    def view_customers(self):
        """Xem khách hàng"""
        self.clear_content()
        tk.Label(
            self.content_frame,
            text="DANH SÁCH KHÁCH HÀNG (CHỈ XEM)",
            font=("Arial", 18, "bold"),
            bg=self.bg_color
        ).pack(pady=20)
    
    def view_invoices(self):
        """Xem hóa đơn"""
        self.clear_content()
        tk.Label(
            self.content_frame,
            text="DANH SÁCH HÓA ĐƠN (CHỈ XEM)",
            font=("Arial", 18, "bold"),
            bg=self.bg_color
        ).pack(pady=20)
    
    def manage_attendance(self):
        """Vẽ UI Chấm công nhân viên"""
        self.clear_content()
        
        tk.Label(
            self.content_frame,
            text="CHẤM CÔNG NHÂN VIÊN",
            font=("Arial", 18, "bold"),
            bg=self.bg_color,
            fg="#003366"
        ).pack(pady=10)
        
        date_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        date_frame.pack(pady=10)
        
        tk.Label(
            date_frame,
            text="Ngày chấm công:",
            font=("Arial", 12),
            bg=self.bg_color
        ).pack(side=tk.LEFT, padx=10)
        
        self.date_var = tk.StringVar(value=date.today().strftime('%Y-%m-%d'))
        date_entry = tk.Entry(date_frame, textvariable=self.date_var, font=("Arial", 12), width=15)
        date_entry.pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            date_frame,
            text="Tải dữ liệu",
            font=("Arial", 11),
            bg=self.btn_color,
            fg="white",
            command=self.logic.load_attendance 
        ).pack(side=tk.LEFT, padx=10)
        
        table_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        columns = ("ID", "Họ tên", "Giờ vào", "Giờ ra", "Số giờ làm", "Trạng thái")
        self.attendance_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)
        
        for col in columns:
            self.attendance_tree.heading(col, text=col)
            self.attendance_tree.column(col, width=120, anchor="center")
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.attendance_tree.yview)
        self.attendance_tree.configure(yscrollcommand=scrollbar.set)
        
        self.attendance_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        btn_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        btn_frame.pack(pady=10)
        
        tk.Button(
            btn_frame,
            text="✓ Chấm công",
            font=("Arial", 11),
            bg="#28a745",
            fg="white",
            command=self.logic.add_attendance
        ).pack(side=tk.LEFT, padx=5)
        
        self.logic.load_attendance()
    
    def view_reports(self):
        """Xem báo cáo"""
        self.clear_content()
        tk.Label(
            self.content_frame,
            text="BÁO CÁO THỐNG KÊ (CHỈ XEM)",
            font=("Arial", 18, "bold"),
            bg=self.bg_color
        ).pack(pady=20)