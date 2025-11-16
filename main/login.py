# =================================================================
# FILE: login.py
# MÔ TẢ: Class Login - Giao diện đăng nhập hệ thống
# (Đã loại bỏ info_label và căn chỉnh)
# =================================================================

import tkinter as tk
from tkinter import messagebox, ttk
from database_connection import DatabaseConnection

# Import các cửa sổ con
from UI.admin_window import Admin
from UI.quanly_window import QuanLy
from UI.nhanvien_window import NhanVien

class Login:
    def __init__(self):
        """Khởi tạo cửa sổ đăng nhập"""
        self.window = tk.Tk()
        self.window.title("ĐĂNG NHẬP HỆ THỐNG")
        self.window.geometry("500x400")
        self.window.resizable(False, False)
        
        # Màu sắc chủ đạo
        self.bg_color = "#87CEEB"  # Sky Blue
        self.btn_color = "#4682B4"  # Steel Blue
        self.text_color = "#FFFFFF"
        
        # --- BỘ FONT CHỮ ---
        self.font_title = ("Segoe UI", 20, "bold")
        self.font_label = ("Segoe UI", 12)
        self.font_button = ("Segoe UI", 12, "bold")
        
        # Kết nối database
        self.db = DatabaseConnection()
        
        self.setup_styles()
        self.setup_ui()
        self.center_window()
    
    def setup_styles(self):
        """Định nghĩa style cho các widget TTK để sắc nét hơn"""
        s = ttk.Style()
        
        try:
            s.theme_use('vista')
        except tk.TclError:
            print("Lưu ý: Theme 'vista' không có sẵn, sử dụng theme mặc định.")

        s.configure('Main.TFrame', background=self.bg_color)
        
        s.configure('Title.TLabel',
                    background=self.bg_color,
                    foreground="#003366",
                    font=self.font_title)
        
        s.configure('Login.TFrame',
                    background="white",
                    relief="raised",
                    borderwidth=2)
        
        s.configure('Login.TLabel',
                    background="white",
                    font=self.font_label)
        
        s.configure('TEntry', font=self.font_label)

        s.configure('TButton',
                    font=self.font_button,
                    width=20)

    def center_window(self):
        """Căn giữa cửa sổ"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        """Thiết lập giao diện đăng nhập (Sử dụng TTK và .place())"""
        
        main_frame = ttk.Frame(self.window, style='Main.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame trung tâm để chứa mọi thứ
        center_frame = ttk.Frame(main_frame, style='Main.TFrame')
        center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Logo/Title
        title_label = ttk.Label(
            center_frame,
            text="QUẢN LÝ CỬA HÀNG XE MÁY",
            style='Title.TLabel'
        )
        title_label.pack(pady=20) 
        
        # Frame đăng nhập
        login_frame = ttk.Frame(
            center_frame,
            style='Login.TFrame',
            padding=(20, 20, 20, 20) # <-- TĂNG PADDING CHO CÂN ĐỐI
        )
        login_frame.pack(padx=50) 
        
        # Tên đăng nhập
        ttk.Label(
            login_frame,
            text="Tên đăng nhập:",
            style='Login.TLabel'
        ).grid(row=0, column=0, padx=(0, 10), pady=15, sticky="e") # Tăng pady

        self.username_entry = ttk.Entry(
            login_frame,
            font=self.font_label,
            width=25
        )
        self.username_entry.grid(row=0, column=1, pady=15)
        
        # Mật khẩu
        ttk.Label(
            login_frame,
            text="Mật khẩu:",
            style='Login.TLabel'
        ).grid(row=1, column=0, padx=(0, 10), pady=15, sticky="e") # Tăng pady

        self.password_entry = ttk.Entry(
            login_frame,
            font=self.font_label,
            width=25,
            show="*"
        )
        self.password_entry.grid(row=1, column=1, pady=15)
        
        # Nút đăng nhập
        login_btn = ttk.Button(
            login_frame,
            text="ĐĂNG NHẬP",
            style='TButton',
            cursor="hand2",
            command=self.login
        )
        login_btn.grid(row=2, column=0, columnspan=2, pady=(25, 10)) # (Tăng pady)
        
        # --- ĐÃ XÓA BỎ INFO_LABEL ---
        
        # Bind phím Enter
        self.password_entry.bind('<Return>', lambda e: self.login())
    
    def login(self):
        """Xử lý đăng nhập"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
            return
        
        if not self.db.connect():
            messagebox.showerror("Lỗi", "Không thể kết nối đến database!")
            return
        
        query = """
            SELECT MaNguoiDung, HoTen, VaiTro, TrangThai 
            FROM NguoiDung 
            WHERE TenDangNhap = %s AND MatKhau = %s
        """
        user = self.db.fetch_one(query, (username, password))
        
        if user:
            if user['TrangThai'] == 'KhongHoatDong':
                messagebox.showwarning("Cảnh báo", "Tài khoản đã bị khóa!")
                self.db.disconnect()
                return
            
            messagebox.showinfo("Thành công", f"Xin chào {user['HoTen']}!")
            self.db.disconnect()
            
            self.window.destroy()
            self.open_main_window(user)
        else:
            messagebox.showerror("Lỗi", "Sai tên đăng nhập hoặc mật khẩu!")
            self.db.disconnect()
    
    def open_main_window(self, user_info):
        """Mở giao diện chính theo vai trò"""
        if user_info['VaiTro'] == 'Admin':
            Admin(user_info)
        elif user_info['VaiTro'] == 'QuanLy':
            QuanLy(user_info)
        elif user_info['VaiTro'] == 'NhanVien':
            NhanVien(user_info)
    
    def run(self):
        """Chạy ứng dụng"""
        self.window.mainloop()


# Chạy chương trình
if __name__ == "__main__":
    app = Login()
    app.run()