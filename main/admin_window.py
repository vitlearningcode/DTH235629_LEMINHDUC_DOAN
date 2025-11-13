# =================================================================
# FILE: admin_window.py
# MÔ TẢ: Class Admin - Giao diện quản trị (Phiên bản SQL Server)
# =================================================================

import tkinter as tk
from tkinter import messagebox, ttk
from database_connection import DatabaseConnection
from datetime import datetime

class Admin:
    def __init__(self, user_info):
        """Khởi tạo cửa sổ Admin"""
        self.window = tk.Tk()
        self.window.title(f"ADMIN - {user_info['HoTen']}")
        self.window.geometry("1200x700")
        self.window.state('zoomed')  # Fullscreen
        
        # Thông tin người dùng
        self.user_info = user_info
        
        # Màu sắc
        self.bg_color = "#E6F2FF"
        self.menu_color = "#4682B4"
        self.btn_color = "#5F9EA0"
        self.text_color = "#FFFFFF"
        
        # Database
        self.db = DatabaseConnection()
        self.db.connect()
        
        self.setup_ui()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()
    
    def setup_ui(self):
        """Thiết lập giao diện chính"""
        # Frame trên cùng - Header
        header_frame = tk.Frame(self.window, bg=self.menu_color, height=60)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        
        tk.Label(
            header_frame,
            text="HỆ THỐNG QUẢN LÝ CỬA HÀNG XE MÁY - ADMIN",
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
            command=self.logout
        ).pack(side=tk.RIGHT, padx=10)
        
        # Frame menu bên trái
        menu_frame = tk.Frame(self.window, bg=self.menu_color, width=250)
        menu_frame.pack(fill=tk.Y, side=tk.LEFT)
        
        # Frame nội dung chính
        self.content_frame = tk.Frame(self.window, bg=self.bg_color)
        self.content_frame.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)
        
        # Tạo menu
        self.create_menu(menu_frame)
        
        # Hiển thị trang chủ
        self.show_dashboard()
    
    def create_menu(self, parent):
        """Tạo menu điều hướng"""
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
    # 1. DASHBOARD
    # =================================================================
    def show_dashboard(self):
        """Hiển thị trang chủ"""
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
        
        stats = self.get_dashboard_stats()
        
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A"]
        for i, (label, value) in enumerate(stats.items()):
            card = tk.Frame(stats_frame, bg=colors[i % len(colors)], width=250, height=150)
            card.grid(row=i//2, column=i%2, padx=20, pady=20)
            card.pack_propagate(False)
            
            tk.Label(card, text=label, font=("Arial", 12, "bold"), bg=colors[i % len(colors)], fg="white").pack(pady=10)
            tk.Label(card, text=str(value), font=("Arial", 24, "bold"), bg=colors[i % len(colors)], fg="white").pack()
    
    def get_dashboard_stats(self):
        """Lấy thống kê tổng quan (SQL Server Syntax)"""
        stats = {}
        
        # Tổng số nhân viên
        result = self.db.fetch_one("SELECT COUNT(*) as total FROM NguoiDung WHERE VaiTro='NhanVien'")
        stats["Tổng nhân viên"] = result['total'] if result else 0
        
        # Tổng sản phẩm
        result = self.db.fetch_one("SELECT COUNT(*) as total FROM SanPham")
        stats["Tổng sản phẩm"] = result['total'] if result else 0
        
        # Tổng khách hàng
        result = self.db.fetch_one("SELECT COUNT(*) as total FROM KhachHang")
        stats["Tổng khách hàng"] = result['total'] if result else 0
        
        # Doanh thu tháng này (SQL Server dùng GETDATE())
        result = self.db.fetch_one("""
            SELECT COALESCE(SUM(TongThanhToan), 0) as total 
            FROM HoaDon 
            WHERE MONTH(NgayLap) = MONTH(GETDATE()) 
            AND YEAR(NgayLap) = YEAR(GETDATE())
            AND TrangThai != 'Huy'
        """)
        stats["Doanh thu tháng"] = f"{result['total']:,.0f} VNĐ" if result else "0 VNĐ"
        
        return stats
    
    # =================================================================
    # 2. QUẢN LÝ NHÂN VIÊN
    # =================================================================
    def manage_employees(self):
        self.clear_content()
        tk.Label(self.content_frame, text="QUẢN LÝ NHÂN VIÊN", font=("Arial", 18, "bold"), bg=self.bg_color, fg="#003366").pack(pady=10)
        
        btn_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        btn_frame.pack(pady=10)
        
        buttons = [
            ("➕ Thêm nhân viên", "#28a745", self.add_employee),
            ("✏️ Sửa thông tin", "#ffc107", self.edit_employee),
            ("🗑️ Xóa nhân viên", "#dc3545", self.delete_employee),
            ("🔄 Làm mới", "#17a2b8", self.manage_employees)
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
        
        self.load_employees()
    
    def load_employees(self):
        for item in self.employee_tree.get_children(): self.employee_tree.delete(item)
        query = "SELECT MaNguoiDung, TenDangNhap, HoTen, SoDienThoai, Email, VaiTro, TrangThai FROM NguoiDung ORDER BY MaNguoiDung"
        employees = self.db.fetch_all(query)
        for emp in employees:
            self.employee_tree.insert("", tk.END, values=(
                emp['MaNguoiDung'], emp['TenDangNhap'], emp['HoTen'], emp['SoDienThoai'] or "", emp['Email'] or "", emp['VaiTro'], emp['TrangThai']
            ))
    
    def add_employee(self):
        # Giữ nguyên logic thêm nhân viên của bạn
        dialog = tk.Toplevel(self.window)
        dialog.title("Thêm nhân viên")
        dialog.geometry("500x500")
        
        fields = [("Tên đăng nhập:", "username"), ("Mật khẩu:", "password"), ("Họ tên:", "fullname"), 
                  ("Số điện thoại:", "phone"), ("Email:", "email"), ("Địa chỉ:", "address")]
        entries = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(dialog, text=label, font=("Arial", 11)).grid(row=i, column=0, padx=20, pady=10, sticky="w")
            entry = tk.Entry(dialog, font=("Arial", 11), width=30)
            if key == "password": entry.config(show="*")
            entry.grid(row=i, column=1, padx=20, pady=10)
            entries[key] = entry
            
        tk.Label(dialog, text="Vai trò:", font=("Arial", 11)).grid(row=len(fields), column=0, padx=20, pady=10, sticky="w")
        role_var = tk.StringVar(value="NhanVien")
        ttk.Combobox(dialog, textvariable=role_var, values=["Admin", "QuanLy", "NhanVien"], state="readonly", width=28).grid(row=len(fields), column=1, padx=20, pady=10)
        
        def save():
            data = [entries[k].get().strip() for k in ["username", "password", "fullname", "phone", "email", "address"]]
            if not data[0] or not data[1] or not data[2]:
                messagebox.showwarning("Cảnh báo", "Nhập đủ thông tin bắt buộc!")
                return
            query = "INSERT INTO NguoiDung (TenDangNhap, MatKhau, HoTen, SoDienThoai, Email, DiaChi, VaiTro) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            if self.db.execute_query(query, (*data, role_var.get())):
                messagebox.showinfo("Thành công", "Đã thêm nhân viên")
                dialog.destroy()
                self.load_employees()
            else: messagebox.showerror("Lỗi", "Thất bại")
            
        tk.Button(dialog, text="💾 Lưu", bg="#28a745", fg="white", command=save).grid(row=len(fields)+1, columnspan=2, pady=20)

    def edit_employee(self):
        if not self.employee_tree.selection():
            messagebox.showwarning("Chú ý", "Chọn nhân viên cần sửa")
            return
        messagebox.showinfo("Info", "Tính năng sửa nhân viên (chưa implement)")

    def delete_employee(self):
        sel = self.employee_tree.selection()
        if not sel: return
        id = self.employee_tree.item(sel[0])['values'][0]
        if messagebox.askyesno("Xóa", "Xóa nhân viên này?"):
            self.db.execute_query("DELETE FROM NguoiDung WHERE MaNguoiDung = %s", (id,))
            self.load_employees()

    # =================================================================
    # 3. QUẢN LÝ SẢN PHẨM
    # =================================================================
    def manage_products(self):
        self.clear_content()
        tk.Label(self.content_frame, text="QUẢN LÝ SẢN PHẨM", font=("Arial", 18, "bold"), bg=self.bg_color).pack(pady=10)
        
        btn_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="➕ Thêm SP", bg="#28a745", fg="white", command=self.add_product).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="✏️ Sửa SP", bg="#ffc107", fg="white", command=self.edit_product).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🗑️ Xóa SP", bg="#dc3545", fg="white", command=self.delete_product).pack(side=tk.LEFT, padx=5)
        
        columns = ("Mã", "Tên SP", "Hãng", "Loại", "Màu", "Giá bán", "Tồn kho", "Trạng thái")
        self.product_tree = ttk.Treeview(self.content_frame, columns=columns, show="headings")
        for col in columns: self.product_tree.heading(col, text=col)
        self.product_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.load_products()

    def load_products(self):
        for item in self.product_tree.get_children(): self.product_tree.delete(item)
        query = """
            SELECT sp.MaSanPham, sp.TenSanPham, hx.TenHangXe, lx.TenLoaiXe,
                   sp.MauSac, sp.GiaBan, sp.SoLuongTon, sp.TrangThai
            FROM SanPham sp
            LEFT JOIN HangXe hx ON sp.MaHangXe = hx.MaHangXe
            LEFT JOIN LoaiXe lx ON sp.MaLoaiXe = lx.MaLoaiXe
            ORDER BY sp.MaSanPham
        """
        products = self.db.fetch_all(query)
        for p in products:
            self.product_tree.insert("", tk.END, values=(
                p['MaSanPham'], p['TenSanPham'], p['TenHangXe'], p['TenLoaiXe'],
                p['MauSac'], f"{p['GiaBan']:,.0f}", p['SoLuongTon'], p['TrangThai']
            ))

    def add_product(self): messagebox.showinfo("Info", "Chức năng Thêm Sản Phẩm")
    def edit_product(self): messagebox.showinfo("Info", "Chức năng Sửa Sản Phẩm")
    def delete_product(self): messagebox.showinfo("Info", "Chức năng Xóa Sản Phẩm")

    # =================================================================
    # 4. QUẢN LÝ PHỤ TÙNG
    # =================================================================
    def manage_parts(self):
        self.clear_content()
        tk.Label(self.content_frame, text="QUẢN LÝ PHỤ TÙNG", font=("Arial", 18, "bold"), bg=self.bg_color).pack(pady=10)
        
        btn_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="➕ Thêm", bg="#28a745", fg="white", command=self.add_part).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="✏️ Sửa", bg="#ffc107", fg="white", command=self.edit_part).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🗑️ Xóa", bg="#dc3545", fg="white", command=self.delete_part).pack(side=tk.LEFT, padx=5)
        
        columns = ("Mã", "Tên phụ tùng", "Loại", "Đơn vị", "Giá nhập", "Giá bán", "Tồn kho")
        self.part_tree = ttk.Treeview(self.content_frame, columns=columns, show="headings", height=25)
        for col in columns: self.part_tree.heading(col, text=col)
        self.part_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.load_parts()

    def load_parts(self):
        for item in self.part_tree.get_children(): self.part_tree.delete(item)
        query = """
            SELECT pt.MaPhuTung, pt.TenPhuTung, lpt.TenLoaiPhuTung, pt.DonViTinh, pt.GiaNhap, pt.GiaBan, pt.SoLuongTon
            FROM PhuTung pt
            LEFT JOIN LoaiPhuTung lpt ON pt.MaLoaiPhuTung = lpt.MaLoaiPhuTung
            ORDER BY pt.MaPhuTung
        """
        parts = self.db.fetch_all(query)
        for p in parts:
            self.part_tree.insert("", tk.END, values=(
                p['MaPhuTung'], p['TenPhuTung'], p['TenLoaiPhuTung'], p['DonViTinh'], 
                f"{p['GiaNhap']:,.0f}", f"{p['GiaBan']:,.0f}", p['SoLuongTon']
            ))

    def add_part(self): messagebox.showinfo("Info", "Chức năng Thêm Phụ Tùng")
    def edit_part(self): messagebox.showinfo("Info", "Chức năng Sửa Phụ Tùng")
    def delete_part(self): messagebox.showinfo("Info", "Chức năng Xóa Phụ Tùng")

    # =================================================================
    # 5. QUẢN LÝ KHO (Placeholder)
    # =================================================================
    def manage_warehouse(self):
        self.clear_content()
        tk.Label(self.content_frame, text="QUẢN LÝ KHO (Đang phát triển)", font=("Arial", 18, "bold"), bg=self.bg_color).pack(pady=20)

    # =================================================================
    # 6. QUẢN LÝ KHÁCH HÀNG
    # =================================================================
    def manage_customers(self):
        self.clear_content()
        tk.Label(self.content_frame, text="QUẢN LÝ KHÁCH HÀNG", font=("Arial", 18, "bold"), bg=self.bg_color).pack(pady=10)
        
        search_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        search_frame.pack(pady=10)
        tk.Label(search_frame, text="Tìm kiếm:", bg=self.bg_color).pack(side=tk.LEFT, padx=5)
        search_entry = tk.Entry(search_frame, font=("Arial", 11), width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="🔍 Tìm", bg=self.btn_color, fg="white", command=lambda: self.search_customers(search_entry.get())).pack(side=tk.LEFT, padx=5)
        
        columns = ("Mã", "Họ tên", "SĐT", "Email", "Địa chỉ", "Loại KH", "Ngày tạo")
        self.customer_tree = ttk.Treeview(self.content_frame, columns=columns, show="headings", height=22)
        for col in columns: self.customer_tree.heading(col, text=col)
        self.customer_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.load_customers()

    def load_customers(self):
        for item in self.customer_tree.get_children(): self.customer_tree.delete(item)
        # SQL Server: dùng FORMAT(NgayTao, 'dd/MM/yyyy') hoặc CONVERT
        query = """
            SELECT TOP 100 MaKhachHang, HoTen, SoDienThoai, Email, DiaChi, 
                   LoaiKhachHang, FORMAT(NgayTao, 'dd/MM/yyyy') as NgayTao
            FROM KhachHang
            ORDER BY MaKhachHang DESC
        """
        try:
            customers = self.db.fetch_all(query)
            for c in customers:
                self.customer_tree.insert("", tk.END, values=(
                    c['MaKhachHang'], c['HoTen'], c['SoDienThoai'], c['Email'], c['DiaChi'], c['LoaiKhachHang'], c['NgayTao']
                ))
        except Exception as e:
            messagebox.showerror("Lỗi Query", str(e))

    def search_customers(self, keyword):
        messagebox.showinfo("Info", f"Tìm kiếm: {keyword}")

    # =================================================================
    # 7. QUẢN LÝ HÓA ĐƠN
    # =================================================================
    def manage_invoices(self):
        self.clear_content()
        tk.Label(self.content_frame, text="QUẢN LÝ HÓA ĐƠN", font=("Arial", 18, "bold"), bg=self.bg_color).pack(pady=10)
        
        columns = ("Mã HĐ", "Khách hàng", "Nhân viên", "Ngày lập", "Tổng tiền", "Thanh toán", "Còn nợ", "Trạng thái")
        self.invoice_tree = ttk.Treeview(self.content_frame, columns=columns, show="headings", height=20)
        for col in columns: self.invoice_tree.heading(col, text=col)
        self.invoice_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.load_invoices()

    def load_invoices(self):
        for item in self.invoice_tree.get_children(): self.invoice_tree.delete(item)
        # SQL Server: TOP thay cho LIMIT, FORMAT thay cho DATE_FORMAT
        query = """
            SELECT TOP 100 hd.MaHoaDon, kh.HoTen as KhachHang, nd.HoTen as NhanVien,
                   FORMAT(hd.NgayLap, 'dd/MM/yyyy HH:mm') as NgayLap,
                   hd.TongTien, hd.TongThanhToan, hd.TienConNo, hd.TrangThai
            FROM HoaDon hd
            JOIN KhachHang kh ON hd.MaKhachHang = kh.MaKhachHang
            JOIN NguoiDung nd ON hd.MaNguoiDung = nd.MaNguoiDung
            ORDER BY hd.MaHoaDon DESC
        """
        invoices = self.db.fetch_all(query)
        for inv in invoices:
            self.invoice_tree.insert("", tk.END, values=(
                inv['MaHoaDon'], inv['KhachHang'], inv['NhanVien'], inv['NgayLap'],
                f"{inv['TongTien']:,.0f}", f"{inv['TongThanhToan']:,.0f}",
                f"{inv['TienConNo']:,.0f}", inv['TrangThai']
            ))

    # =================================================================
    # 8. QUẢN LÝ KHUYẾN MÃI
    # =================================================================
    def manage_promotions(self):
        self.clear_content()
        tk.Label(self.content_frame, text="QUẢN LÝ KHUYẾN MÃI", font=("Arial", 18, "bold"), bg=self.bg_color).pack(pady=10)
        
        columns = ("Mã", "Tên chương trình", "Loại", "Giá trị", "Từ ngày", "Đến ngày", "Trạng thái")
        self.promo_tree = ttk.Treeview(self.content_frame, columns=columns, show="headings", height=22)
        for col in columns: self.promo_tree.heading(col, text=col)
        self.promo_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.load_promotions()

    def load_promotions(self):
        for item in self.promo_tree.get_children(): self.promo_tree.delete(item)
        # SQL Server Date Format
        query = """
            SELECT MaKhuyenMai, TenKhuyenMai, LoaiKhuyenMai, GiaTri,
                   FORMAT(NgayBatDau, 'dd/MM/yyyy') as NgayBatDau,
                   FORMAT(NgayKetThuc, 'dd/MM/yyyy') as NgayKetThuc,
                   TrangThai
            FROM KhuyenMai
            ORDER BY NgayBatDau DESC
        """
        promos = self.db.fetch_all(query)
        for p in promos:
            value = f"{p['GiaTri']:,.0f}%" if p['LoaiKhuyenMai'] == 'PhanTram' else f"{p['GiaTri']:,.0f} VNĐ"
            self.promo_tree.insert("", tk.END, values=(
                p['MaKhuyenMai'], p['TenKhuyenMai'], p['LoaiKhuyenMai'], value, 
                p['NgayBatDau'], p['NgayKetThuc'], p['TrangThai']
            ))

    # =================================================================
    # 9. QUẢN LÝ CHẤM CÔNG
    # =================================================================
    def manage_attendance(self):
        self.clear_content()
        tk.Label(self.content_frame, text="QUẢN LÝ CHẤM CÔNG (Đang phát triển)", font=("Arial", 18, "bold"), bg=self.bg_color).pack(pady=20)

    # =================================================================
    # 10. BÁO CÁO THỐNG KÊ
    # =================================================================
    def show_reports(self):
        self.clear_content()
        tk.Label(self.content_frame, text="BÁO CÁO THỐNG KÊ", font=("Arial", 18, "bold"), bg=self.bg_color).pack(pady=10)
        
        report_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        report_frame.pack(pady=20)
        reports = [
            ("📊 Doanh thu theo tháng", self.report_revenue),
            ("📦 Tồn kho sản phẩm", self.report_inventory),
            ("👥 Hiệu suất nhân viên", self.report_employee_performance),
            ("🏆 Top sản phẩm bán chạy", self.report_top_products),
            ("👤 Khách hàng thân thiết", self.report_loyal_customers),
            ("💰 Công nợ khách hàng", self.report_debt)
        ]
        row, col = 0, 0
        for text, command in reports:
            btn = tk.Button(report_frame, text=text, font=("Arial", 12), bg=self.btn_color, fg="white", width=30, height=3, command=command)
            btn.grid(row=row, column=col, padx=15, pady=15)
            col += 1
            if col > 1: col, row = 0, row + 1

    def report_revenue(self):
        # (Giữ nguyên logic cửa sổ con nhưng cần chỉnh query bên trong nếu có)
        dialog = tk.Toplevel(self.window)
        dialog.title("Báo cáo doanh thu")
        dialog.geometry("800x600")
        tk.Label(dialog, text="Báo cáo doanh thu (Demo)", font=("Arial", 16)).pack(pady=20)
        
    # Các hàm placeholder để tránh lỗi
    def report_inventory(self): messagebox.showinfo("Info", "Báo cáo tồn kho")
    def report_employee_performance(self): messagebox.showinfo("Info", "Báo cáo nhân viên")
    def report_top_products(self): messagebox.showinfo("Info", "Báo cáo Top sản phẩm")
    def report_loyal_customers(self): messagebox.showinfo("Info", "Báo cáo Khách hàng")
    def report_debt(self): messagebox.showinfo("Info", "Báo cáo công nợ")

    # =================================================================
    # SYSTEM
    # =================================================================
    def logout(self):
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn đăng xuất?"):
            self.db.disconnect()
            self.window.destroy()
            # from login import Login
            # Login().run()
            print("Đã đăng xuất") # Thay thế dòng này bằng logic gọi lại màn hình login của bạn
    
    def on_closing(self):
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn thoát?"):
            self.db.disconnect()
            self.window.destroy()