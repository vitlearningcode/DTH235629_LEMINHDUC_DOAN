# Mở file: main/Function/function_Admin/admin_reports_logic.py
# THAY THẾ TOÀN BỘ NỘI DUNG FILE CŨ BẰNG FILE NÀY:

import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from datetime import datetime

class AdminReportsLogic:
    def __init__(self, view):
        self.view = view
        self.db = view.db
        
    def _create_report_window(self, title, geometry="900x600"):
        """Hàm trợ giúp: Tạo một cửa sổ Toplevel tiêu chuẩn cho báo cáo"""
        dialog = tk.Toplevel(self.view.window)
        dialog.title(title)
        dialog.geometry(geometry)
        dialog.grab_set()
        
        tk.Label(dialog, text=title.upper(), font=("Arial", 16, "bold")).pack(pady=10)
        
        # Chỉ TẠO, không .pack()
        table_frame = ttk.Frame(dialog)
        
        return dialog, table_frame

    # --- BÁO CÁO 1: DOANH THU (Đã sửa lỗi hiển thị) ---
    def report_revenue(self):
        """Hiển thị Báo cáo doanh thu theo tháng (Dùng SP, với ô nhập liệu tích hợp)"""
        
        title = "Báo cáo Doanh thu Theo Tháng"
        dialog, table_frame = self._create_report_window(title, "800x600") 

        # --- Tạo Khung Nhập Liệu (Filter Frame) ---
        filter_frame = ttk.Frame(dialog) 
        filter_frame.pack(pady=10) # Đặt khung lọc LÊN TRÊN

        current_year = datetime.now().year
        current_month = datetime.now().month

        ttk.Label(filter_frame, text="Năm:", font=("Arial", 11)).pack(side=tk.LEFT, padx=(0, 5))
        year_entry = ttk.Entry(filter_frame, font=("Arial", 11), width=7)
        year_entry.insert(0, str(current_year))
        year_entry.pack(side=tk.LEFT, padx=5)

        ttk.Label(filter_frame, text="Tháng:", font=("Arial", 11)).pack(side=tk.LEFT, padx=(10, 5))
        month_entry = ttk.Entry(filter_frame, font=("Arial", 11), width=5)
        month_entry.insert(0, str(current_month))
        month_entry.pack(side=tk.LEFT, padx=5)

        # --- Đóng gói table_frame (BÊN DƯỚI filter_frame) ---
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # --- Tạo Treeview (bên trong table_frame) ---
        columns = ("Ngay", "SoHoaDon", "DoanhThu", "TongKhuyenMai")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=18)
        
        tree.heading("Ngay", text="Ngày")
        tree.column("Ngay", width=150, anchor="center")
        tree.heading("SoHoaDon", text="Số Hóa Đơn")
        tree.column("SoHoaDon", width=100, anchor="center")
        tree.heading("DoanhThu", text="Doanh Thu")
        tree.column("DoanhThu", width=200, anchor="e")
        tree.heading("TongKhuyenMai", text="Tổng Khuyến Mãi")
        tree.column("TongKhuyenMai", width=200, anchor="e")
        
        tree.pack(fill=tk.BOTH, expand=True)

        # --- Tạo Label Tổng Kết ---
        total_label = tk.Label(dialog, text="TỔNG DOANH THU THÁNG: 0 VNĐ", 
                               font=("Arial", 14, "bold"), fg="blue")
        total_label.pack(pady=10) # Nằm dưới cùng

        # --- Logic tải dữ liệu (hàm lồng) ---
        def load_report_data():
            try:
                year = int(year_entry.get())
                month = int(month_entry.get())
                if not (2000 <= year <= 2100 and 1 <= month <= 12):
                    raise ValueError("Date out of range")
            except ValueError:
                messagebox.showerror("Lỗi", "Năm (YYYY) hoặc Tháng (1-12) không hợp lệ.", parent=dialog)
                return

            for item in tree.get_children():
                tree.delete(item)
            dialog.title(f"Báo cáo Doanh thu Tháng {month}/{year}")

            try:
                query = "EXEC sp_ThongKeDoanhThuTheoThang @nam = ?, @thang = ?"
                records = self.db.fetch_all(query, (year, month))
                
                total_revenue = 0
                if records:
                    for rec in records:
                        total_revenue += rec['DoanhThu']
                        tree.insert("", tk.END, values=(
                            rec['Ngay'], 
                            rec['SoHoaDon'], 
                            f"{rec['DoanhThu']:,.0f} VNĐ", 
                            f"{rec['TongKhuyenMai']:,.0f} VNĐ"
                        ))
                total_label.config(text=f"TỔNG DOANH THU THÁNG: {total_revenue:,.0f} VNĐ")
            except Exception as e:
                messagebox.showerror("Lỗi CSDL", f"Không thể thực thi Stored Procedure: {e}", parent=dialog)

        # --- Nút "Tải báo cáo" ---
        load_button = ttk.Button(
            filter_frame, text="Tải báo cáo", 
            command=load_report_data, 
            cursor="hand2"
        )
        load_button.pack(side=tk.LEFT, padx=10)
        
        load_report_data() # Tải lần đầu

    # --- BÁO CÁO 2: TỒN KHO (Đã sửa lỗi hiển thị) ---
    def report_inventory(self): 
        """Hiển thị Báo cáo tồn kho (Dùng SP)"""
        
        title = "Báo cáo Tồn kho Sản phẩm"
        dialog, table_frame = self._create_report_window(title, "900x600")

        # --- SỬA LỖI: Thêm lại dòng .pack() ---
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        columns = ("Mã SP", "Tên SP", "Hãng", "Loại", "Tồn kho", "Giá trị tồn kho")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=25)
        
        tree.heading("Mã SP", text="Mã SP")
        tree.column("Mã SP", width=50, anchor="center")
        tree.heading("Tên SP", text="Tên SP")
        tree.column("Tên SP", width=300)
        tree.heading("Hãng", text="Hãng")
        tree.column("Hãng", width=100)
        tree.heading("Loại", text="Loại")
        tree.column("Loại", width=100)
        tree.heading("Tồn kho", text="Tồn kho")
        tree.column("Tồn kho", width=80, anchor="center")
        tree.heading("Giá trị tồn kho", text="Giá trị tồn kho")
        tree.column("Giá trị tồn kho", width=150, anchor="e")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        query = "EXEC sp_ThongKeTonKhoSanPham"
        records = self.db.fetch_all(query)
        if records:
            for rec in records:
                tree.insert("", tk.END, values=(
                    rec['MaSanPham'], rec['TenSanPham'], rec['TenHangXe'],
                    rec['TenLoaiXe'], rec['SoLuongTon'], f"{rec['GiaTriTonKho']:,.0f} VNĐ"
                ))
        
        tk.Button(dialog, text="Đóng", command=dialog.destroy, font=("Arial", 11, "bold"), 
                  bg="#6c757d", fg="white", width=15).pack(pady=10)

    
    # --- BÁO CÁO 3: HIỆU SUẤT NHÂN VIÊN (Đã sửa lỗi hiển thị) ---
    def report_employee_performance(self): 
        """Hiển thị Báo cáo hiệu suất nhân viên (Dùng View)"""
        
        title = "Báo cáo Hiệu suất Nhân viên"
        dialog, table_frame = self._create_report_window(title, "900x500")

        # --- SỬA LỖI: Thêm lại dòng .pack() ---
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        columns = ("MaNguoiDung", "HoTen", "VaiTro", "SoHoaDonLap", "TongDoanhThu", "SoNgayLam")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)
        
        tree.heading("MaNguoiDung", text="ID")
        tree.column("MaNguoiDung", width=50, anchor="center")
        tree.heading("HoTen", text="Họ Tên")
        tree.column("HoTen", width=200)
        tree.heading("VaiTro", text="Vai Trò")
        tree.column("VaiTro", width=100)
        tree.heading("SoHoaDonLap", text="Số HĐ Lập")
        tree.column("SoHoaDonLap", width=100, anchor="center")
        tree.heading("TongDoanhThu", text="Tổng Doanh Thu")
        tree.column("TongDoanhThu", width=150, anchor="e")
        tree.heading("SoNgayLam", text="Số Ngày Làm")
        tree.column("SoNgayLam", width=100, anchor="center")
        
        tree.pack(fill=tk.BOTH, expand=True)

        query = "SELECT * FROM v_ThongKeNhanVien"
        records = self.db.fetch_all(query)
        if records:
            for rec in records:
                tree.insert("", tk.END, values=(
                    rec['MaNguoiDung'], 
                    rec['HoTen'], 
                    rec['VaiTro'],
                    rec['SoHoaDonLap'], 
                    f"{rec['TongDoanhThu']:,.0f} VNĐ", 
                    rec['SoNgayLam']
                ))
        
        tk.Button(dialog, text="Đóng", command=dialog.destroy, font=("Arial", 11, "bold"), 
                  bg="#6c757d", fg="white", width=15).pack(pady=10)

    
    # --- BÁO CÁO 4: CÔNG NỢ (Đã sửa lỗi hiển thị) ---
    def report_debt(self): 
        """Hiển thị Báo cáo công nợ (Dùng View)"""
        
        title = "Báo cáo Công nợ Khách hàng"
        dialog, table_frame = self._create_report_window(title, "900x500")

        # --- SỬA LỖI: Thêm lại dòng .pack() ---
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        columns = ("MaHoaDon", "TenKhachHang", "SoDienThoai", "NgayLap", "TongThanhToan", "TienDaTra", "TienConNo")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)
        
        tree.heading("MaHoaDon", text="Mã HĐ")
        tree.column("MaHoaDon", width=60, anchor="center")
        tree.heading("TenKhachHang", text="Khách Hàng")
        tree.column("TenKhachHang", width=200)
        tree.heading("SoDienThoai", text="Số Điện Thoại")
        tree.column("SoDienThoai", width=100, anchor="center")
        tree.heading("NgayLap", text="Ngày Lập")
        tree.column("NgayLap", width=130, anchor="center")
        tree.heading("TongThanhToan", text="Tổng HĐ")
        tree.column("TongThanhToan", width=120, anchor="e")
        tree.heading("TienDaTra", text="Đã Trả")
        tree.column("TienDaTra", width=120, anchor="e")
        tree.heading("TienConNo", text="Còn Nợ")
        tree.column("TienConNo", width=120, anchor="e")
        
        tree.pack(fill=tk.BOTH, expand=True)

        query = """
            SELECT MaHoaDon, TenKhachHang, SoDienThoai, FORMAT(NgayLap, 'dd/MM/yyyy') as NgayLap, 
                   TongThanhToan, TienDaTra, TienConNo 
            FROM v_ChiTietHoaDon
            WHERE TrangThai = 'ConNo' AND TienConNo > 0
            ORDER BY NgayLap ASC
        """
        records = self.db.fetch_all(query)
        
        total_debt = 0
        if records:
            for rec in records:
                total_debt += rec['TienConNo']
                tree.insert("", tk.END, values=(
                    rec['MaHoaDon'], 
                    rec['TenKhachHang'], 
                    rec['SoDienThoai'],
                    rec['NgayLap'], 
                    f"{rec['TongThanhToan']:,.0f} VNĐ", 
                    f"{rec['TienDaTra']:,.0f} VNĐ",
                    f"{rec['TienConNo']:,.0f} VNĐ"
                ))
        
        tk.Label(dialog, text=f"TỔNG CÔNG NỢ PHẢI THU: {total_debt:,.0f} VNĐ", 
                 font=("Arial", 14, "bold"), fg="red").pack(pady=10)
        
        tk.Button(dialog, text="Đóng", command=dialog.destroy, font=("Arial", 11, "bold"), 
                  bg="#6c757d", fg="white", width=15).pack(pady=10)

    # --- BÁO CÁO 5 & 6 (Giữ chỗ) ---
   # --- BÁO CÁO 5: TOP SẢN PHẨM (Đã cập nhật: Chỉ Xe, Giảm dần) ---
    def report_top_products(self): 
        """Hiển thị Báo cáo Top Sản phẩm (Xe) bán chạy (Không dùng SP)"""
        
        title = "Báo cáo Top Sản Phẩm Bán Chạy"
        # Sử dụng geometry rộng hơn một chút
        dialog, table_frame = self._create_report_window(title, "800x600") 

        # --- Tạo Khung Nhập Liệu (Filter Frame) ---
        filter_frame = ttk.Frame(dialog) 
        filter_frame.pack(pady=10)

        current_year = datetime.now().year
        current_month = datetime.now().month

        ttk.Label(filter_frame, text="Năm:", font=("Arial", 11)).pack(side=tk.LEFT, padx=(0, 5))
        year_entry = ttk.Entry(filter_frame, font=("Arial", 11), width=7)
        year_entry.insert(0, str(current_year))
        year_entry.pack(side=tk.LEFT, padx=5)

        ttk.Label(filter_frame, text="Tháng:", font=("Arial", 11)).pack(side=tk.LEFT, padx=(10, 5))
        month_entry = ttk.Entry(filter_frame, font=("Arial", 11), width=5)
        month_entry.insert(0, str(current_month))
        month_entry.pack(side=tk.LEFT, padx=5)

        # --- Đóng gói table_frame ---
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # --- Tạo Treeview (Đã bỏ cột "Loại") ---
        columns = ("Ma", "Ten", "SoLuongBan")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=18)
        
        tree.heading("Ma", text="Mã SP")
        tree.column("Ma", width=80, anchor="center")
        tree.heading("Ten", text="Tên Sản Phẩm (Xe)")
        tree.column("Ten", width=450) # Tăng độ rộng
        tree.heading("SoLuongBan", text="Tổng Số Lượng Bán")
        tree.column("SoLuongBan", width=150, anchor="e")
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # --- Logic tải dữ liệu (hàm lồng) ---
        def load_report_data():
            try:
                year = int(year_entry.get())
                month = int(month_entry.get())
                if not (2000 <= year <= 2100 and 1 <= month <= 12):
                    raise ValueError("Date out of range")
            except ValueError:
                messagebox.showerror("Lỗi", "Năm (YYYY) hoặc Tháng (1-12) không hợp lệ.", parent=dialog)
                return

            for item in tree.get_children():
                tree.delete(item)
            dialog.title(f"Top Bán Chạy Tháng {month}/{year}")

            try:
                # Dùng %s vì database_connection.py sẽ tự chuyển sang '?'
                params = (year, month)
                
                # Query 1: Lấy top Sản phẩm (Xe) và sắp xếp DESC
                query_sp = """
                    SELECT 
                        sp.MaSanPham AS 'Ma',
                        sp.TenSanPham AS 'Ten',
                        SUM(ct.SoLuong) AS 'SoLuongBan'
                    FROM ChiTietHoaDonSanPham ct
                    JOIN HoaDon hd ON ct.MaHoaDon = hd.MaHoaDon
                    JOIN SanPham sp ON ct.MaSanPham = sp.MaSanPham
                    WHERE 
                        YEAR(hd.NgayLap) = %s 
                        AND MONTH(hd.NgayLap) = %s
                        AND hd.TrangThai != 'Huy'
                    GROUP BY sp.MaSanPham, sp.TenSanPham
                    ORDER BY SoLuongBan DESC
                """
                records_sp = self.db.fetch_all(query_sp, params)
                
                # Query 2: ĐÃ XÓA
                
                # Kết hợp và Sắp xếp: ĐÃ XÓA (SQL tự sắp xếp)
                
                if records_sp:
                    for rec in records_sp:
                        tree.insert("", tk.END, values=(
                            rec['Ma'], 
                            rec['Ten'], 
                            rec['SoLuongBan']
                        ))
                else:
                    tree.insert("", tk.END, values=("", "Không có dữ liệu bán hàng cho tháng này.", ""))

            except Exception as e:
                messagebox.showerror("Lỗi CSDL", f"Không thể thực thi truy vấn: {e}", parent=dialog)

        # --- Nút "Tải báo cáo" ---
        load_button = ttk.Button(
            filter_frame, text="Tải báo cáo", 
            command=load_report_data, 
            cursor="hand2"
        )
        load_button.pack(side=tk.LEFT, padx=10)
        
        load_report_data() # Tải lần đầu
    
    