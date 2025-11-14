# =================================================================
# FILE: login.py
# MÔ TẢ: Class Login - Giao diện đăng nhập hệ thống
# (Đã cập nhật đường dẫn import)
# =================================================================

import tkinter as tk
from tkinter import messagebox, ttk
from database_connection import DatabaseConnection

# --- THAY ĐỔI DUY NHẤT LÀ Ở 3 DÒNG DƯỚI ĐÂY ---
# Chúng ta thêm tiền tố "UI." vào trước tên file
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
        
        # Kết nối database
        self.db = DatabaseConnection()
        
        self.setup_ui()
        self.center_window()
    
    def center_window(self):
        """Căn giữa cửa sổ"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        """Thiết lập giao diện đăng nhập"""
        # Frame chính
        main_frame = tk.Frame(self.window, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Logo/Title
        title_label = tk.Label(
            main_frame,
            text="QUẢN LÝ CỬA HÀNG XE MÁY",
            font=("Arial", 20, "bold"),
            bg=self.bg_color,
            fg="#003366"
        )
        title_label.pack(pady=30)
        
        # Frame đăng nhập
        login_frame = tk.Frame(main_frame, bg="white", bd=2, relief=tk.RAISED)
        login_frame.pack(padx=50, pady=20)
        
        # Tên đăng nhập
        tk.Label(
            login_frame,
            text="Tên đăng nhập:",
            font=("Arial", 12),
            bg="white"
        ).grid(row=0, column=0, padx=20, pady=15, sticky="w")
        
        self.username_entry = tk.Entry(
            login_frame,
            font=("Arial", 12),
            width=25
        )
        self.username_entry.grid(row=0, column=1, padx=20, pady=15)
        
        # Mật khẩu
        tk.Label(
            login_frame,
            text="Mật khẩu:",
            font=("Arial", 12),
            bg="white"
        ).grid(row=1, column=0, padx=20, pady=15, sticky="w")
        
        self.password_entry = tk.Entry(
            login_frame,
            font=("Arial", 12),
            width=25,
            show="*"
        )
        self.password_entry.grid(row=1, column=1, padx=20, pady=15)
        
        # Nút đăng nhập
        login_btn = tk.Button(
            login_frame,
            text="ĐĂNG NHẬP",
            font=("Arial", 12, "bold"),
            bg=self.btn_color,
            fg=self.text_color,
            width=20,
            cursor="hand2",
            command=self.login
        )
        login_btn.grid(row=2, column=0, columnspan=2, pady=25)
        
        # Thông tin mặc định
        info_label = tk.Label(
            main_frame,
            text="Tài khoản mặc định:\nAdmin: admin/123456\nQuản lý: quanly01/123456\nNhân viên: nhanvien01/123456",
            font=("Arial", 9),
            bg=self.bg_color,
            fg="#003366",
            justify=tk.LEFT
        )
        info_label.pack(pady=10)
        
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
