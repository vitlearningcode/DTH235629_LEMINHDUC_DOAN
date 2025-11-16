# Mở file: main/Function/function_Admin/admin_customer_logic.py
# THAY THẾ toàn bộ nội dung file CŨ bằng code MỚI này:

import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

class AdminCustomerLogic:
    def __init__(self, view):
        self.view = view
        self.db = view.db

    def load_customers(self, keyword=None):
        """Tải danh sách khách hàng, có hỗ trợ tìm kiếm theo Tên hoặc SĐT"""
        for item in self.view.customer_tree.get_children(): 
            self.view.customer_tree.delete(item)
        
        query = """
            SELECT TOP 100 MaKhachHang, HoTen, SoDienThoai, Email, DiaChi, 
                   LoaiKhachHang, FORMAT(NgayTao, 'dd/MM/yyyy') as NgayTao
            FROM KhachHang
        """
        params = []
        
        if keyword:
            query += " WHERE HoTen LIKE %s OR SoDienThoai LIKE %s"
            params.extend([f"%{keyword}%", f"%{keyword}%"])
            
        query += " ORDER BY MaKhachHang ASC"
        
        try:
            customers = self.db.fetch_all(query, params)
            if customers:
                for c in customers:
                    self.view.customer_tree.insert("", tk.END, values=(
                        c['MaKhachHang'], 
                        c['HoTen'], 
                        c['SoDienThoai'], 
                        c['Email'] or "", 
                        c['DiaChi'] or "", 
                        c['LoaiKhachHang'], 
                        c['NgayTao']
                    ))
        except Exception as e:
            messagebox.showerror("Lỗi Query", str(e))

    def _show_customer_dialog(self, customer_data=None):
        """Hàm nội bộ: Hiển thị cửa sổ Toplevel cho Thêm hoặc Sửa Khách hàng"""
        
        is_edit = customer_data is not None
        
        dialog = tk.Toplevel(self.view.window)
        dialog.title("Thêm Khách Hàng Mới" if not is_edit else f"Cập Nhật Khách Hàng (ID: {customer_data['MaKhachHang']})")
        dialog.resizable(False, False)
        dialog.grab_set()

        container = tk.Frame(dialog, padx=20, pady=20)
        container.pack(fill="none", expand=False)

        entries = {}
        
        # Định nghĩa các trường dựa trên database_setup.sql
        fields = [
            ("Họ Tên (*):", "HoTen", "entry", None),
            ("Số Điện Thoại (*):", "SoDienThoai", "entry", None),
            ("Email:", "Email", "entry", None),
            ("Địa Chỉ:", "DiaChi", "entry", None),
            ("CMND:", "CMND", "entry", None),
            ("Ngày Sinh (YYYY-MM-DD):", "NgaySinh", "entry", None),
            ("Giới Tính:", "GioiTinh", "combo", ['Nam', 'Nu', 'Khac']),
            ("Loại Khách Hàng:", "LoaiKhachHang", "combo", ['ThongThuong', 'ThanThiet', 'TiemNang'])
        ]

        # Tạo các widget
        for i, (text, key, widget_type, default) in enumerate(fields):
            tk.Label(container, text=text, font=("Arial", 11)).grid(row=i, column=0, padx=10, pady=10, sticky="e")
            
            if widget_type == "entry":
                val = ""
                if is_edit:
                    val = customer_data.get(key) or ""
                    # Xử lý ngày sinh (chỉ lấy phần ngày)
                    if key == "NgaySinh" and val:
                        val = str(val).split(" ")[0]
                entry = tk.Entry(container, font=("Arial", 11), width=40)
                entry.grid(row=i, column=1, padx=10, pady=10)
                entry.insert(0, str(val))
                entries[key] = entry
                
            elif widget_type == "combo":
                val = tk.StringVar()
                if is_edit:
                    val.set(customer_data.get(key) or default[0])
                else:
                    val.set(default[0]) # 'Nam' hoặc 'ThongThuong'

                combo = ttk.Combobox(container, textvariable=val, values=default, state="readonly", width=38, font=("Arial", 11))
                combo.grid(row=i, column=1, padx=10, pady=10)
                entries[key] = combo

        def save():
            try:
                data = {}
                for key, widget in entries.items():
                    data[key] = widget.get().strip()
                
                # Xác thực
                if not data['HoTen'] or not data['SoDienThoai']:
                    messagebox.showwarning("Thiếu thông tin", "Họ Tên và Số Điện Thoại là bắt buộc.", parent=dialog)
                    return
                
                # Xử lý các giá trị có thể là NULL
                ngay_sinh = data['NgaySinh'] if data['NgaySinh'] else None
                if ngay_sinh:
                    # Kiểm tra định dạng ngày
                    datetime.strptime(ngay_sinh, '%Y-%m-%d')

                email = data['Email'] or None
                dia_chi = data['DiaChi'] or None
                cmnd = data['CMND'] or None
                
                # Chuẩn bị query
                if is_edit:
                    query = """
                        UPDATE KhachHang SET 
                        HoTen=%s, SoDienThoai=%s, Email=%s, DiaChi=%s, CMND=%s, 
                        NgaySinh=%s, GioiTinh=%s, LoaiKhachHang=%s, NgayCapNhat=GETDATE()
                        WHERE MaKhachHang=%s
                    """
                    params = (
                        data['HoTen'], data['SoDienThoai'], email, dia_chi, cmnd,
                        ngay_sinh, data['GioiTinh'], data['LoaiKhachHang'],
                        customer_data['MaKhachHang'] # ID cho WHERE
                    )
                else:
                    query = """
                        INSERT INTO KhachHang 
                        (HoTen, SoDienThoai, Email, DiaChi, CMND, NgaySinh, GioiTinh, LoaiKhachHang)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    params = (
                        data['HoTen'], data['SoDienThoai'], email, dia_chi, cmnd,
                        ngay_sinh, data['GioiTinh'], data['LoaiKhachHang']
                    )
                
                # Thực thi
                if self.db.execute_query(query, params):
                    messagebox.showinfo("Thành công", "Lưu thông tin khách hàng thành công!", parent=dialog)
                    dialog.destroy()
                    self.load_customers() # Tải lại danh sách
                else:
                    messagebox.showerror("Lỗi CSDL", "Không thể lưu khách hàng. (Có thể trùng SĐT hoặc Email).", parent=dialog)
                    
            except ValueError:
                messagebox.showerror("Lỗi nhập liệu", "Ngày Sinh phải đúng định dạng YYYY-MM-DD.", parent=dialog)
            except Exception as e:
                messagebox.showerror("Lỗi không xác định", f"{e}", parent=dialog)

        btn_text = "💾 Lưu Thay Đổi" if is_edit else "💾 Thêm Khách Hàng"
        btn_color = "#007bff" if is_edit else "#28a745"
        
        tk.Button(container, text=btn_text, font=("Arial", 12, "bold"), bg=btn_color, fg="white", command=save, width=20, height=2).grid(row=len(fields), column=0, columnspan=2, pady=20)


    # --- CHỨC NĂNG THÊM MỚI ---
    def add_customer(self):
        self._show_customer_dialog(None)
    
    # --- CHỨC NĂNG SỬA ---
    def edit_customer(self):
        selected = self.view.customer_tree.selection()
        if not selected:
            messagebox.showwarning("Chú ý", "Vui lòng chọn một khách hàng để sửa.")
            return
        
        customer_id = self.view.customer_tree.item(selected[0])['values'][0]
        
        # Lấy dữ liệu GỐC từ CSDL
        customer_data = self.db.fetch_one("SELECT * FROM KhachHang WHERE MaKhachHang = %s", (customer_id,))
        
        if customer_data:
            self._show_customer_dialog(customer_data)
        else:
            messagebox.showerror("Lỗi", "Không tìm thấy dữ liệu khách hàng này.")

    # --- CHỨC NĂNG XÓA ---
    def delete_customer(self):
        selected = self.view.customer_tree.selection()
        if not selected:
            messagebox.showwarning("Chú ý", "Vui lòng chọn một khách hàng để xóa.")
            return

        item = self.view.customer_tree.item(selected[0])
        customer_id = item['values'][0]
        customer_name = item['values'][1]

        # Kiểm tra ràng buộc khóa ngoại (MaKhachHang trong HoaDon và PhieuBaoHanh)
        check_hd = self.db.fetch_one("SELECT COUNT(*) as total FROM HoaDon WHERE MaKhachHang = %s", (customer_id,))
        check_bh = self.db.fetch_one("SELECT COUNT(*) as total FROM PhieuBaoHanh WHERE MaKhachHang = %s", (customer_id,))

        if (check_hd and check_hd['total'] > 0) or (check_bh and check_bh['total'] > 0):
            messagebox.showerror("Lỗi Ràng Buộc", 
                                 f"Không thể xóa khách hàng '{customer_name}'.\n"
                                 f"Khách hàng này đã được liên kết với {check_hd['total']} hóa đơn và {check_bh['total']} phiếu bảo hành.")
            return

        if messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc muốn XÓA VĨNH VIỄN khách hàng:\n\n{customer_name} (ID: {customer_id})"):
            try:
                result = self.db.execute_query("DELETE FROM KhachHang WHERE MaKhachHang = %s", (customer_id,))
                
                if result:
                    messagebox.showinfo("Thành công", f"Đã xóa khách hàng '{customer_name}'.")
                    self.load_customers()
                else:
                    messagebox.showerror("Lỗi", "Xóa thất bại.")
            except Exception as e:
                messagebox.showerror("Lỗi CSDL", f"Không thể xóa: {e}")