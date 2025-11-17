# main/Function/function_QuanLy/quanly_employee_view_logic.py

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from database_connection import DatabaseConnection
from PIL import Image, ImageTk
import os
import shutil

class QuanLyEmployeeViewLogic:
    def __init__(self, view):
        self.view = view
        self.db = view.db
        self.resource_path = os.path.join(os.path.dirname(__file__), "..", "..", "resource","NhanVien")
        if not os.path.exists(self.resource_path):
            os.makedirs(self.resource_path)
        self.original_data = {}
        self.new_image_path = None
        
        # --- Ánh xạ trạng thái và vai trò sang Tiếng Việt (GIỮ NGUYÊN) ---
        self.vaitro_map = {
            'Admin': 'Quản trị viên',
            'QuanLy': 'Quản lý',
            'NhanVien': 'Nhân viên'
        }
        self.trangthai_map = {
            'HoatDong': 'Hoạt động',
            'KhongHoatDong': 'Không hoạt động'
        }
        # --- Ánh xạ ngược (Cần để set Combobox trong on_employee_select) ---
        self.vaitro_reverse_map = {v: k for k, v in self.vaitro_map.items()}
        self.trangthai_reverse_map = {v: k for k, v in self.trangthai_map.items()}

    def load_view(self, tree, keyword=None):
        for item in tree.get_children():
            tree.delete(item)
        query = """
        SELECT MaNguoiDung, HoTen, SoDienThoai, Email, VaiTro, TrangThai
        FROM NguoiDung
        WHERE (VaiTro = 'NhanVien' OR VaiTro = 'QuanLy')
        """
        params = []
        if keyword:
            query += " AND (HoTen LIKE %s OR SoDienThoai LIKE %s)"
            params.extend([f"%{keyword}%", f"%{keyword}%"])
        query += " ORDER BY MaNguoiDung"
        records = self.db.fetch_all(query, params)
        if records:
            for rec in records:
                
                # Ánh xạ cho bảng Treeview (LIST)
                display_vaitro = self.vaitro_map.get(rec['VaiTro'], rec['VaiTro'])
                display_trangthai = self.trangthai_map.get(rec['TrangThai'], rec['TrangThai'])
                
                tree.insert(
                    "", tk.END,
                    values=(
                        rec['MaNguoiDung'], rec['HoTen'], rec['SoDienThoai'] or "",
                        rec['Email'] or "", display_vaitro, display_trangthai
                    )
                )

    def on_employee_select(self, event):
        try:
            selected_item = self.view.employee_tree.selection()[0]
            # Lấy dữ liệu đã được ánh xạ tiếng Việt từ Treeview
            values = self.view.employee_tree.item(selected_item, 'values')
            
            if not values or len(values) < 6:
                return
            
            # Lấy ID (không bị ánh xạ) để truy vấn CSDL
            emp_id = values[0] 
            
            # Tải lại dữ liệu gốc từ CSDL
            query = "SELECT * FROM NguoiDung WHERE MaNguoiDung = %s"
            data = self.db.fetch_one(query, (emp_id,))
            
            if not data:
                messagebox.showerror("Lỗi", "Không tìm thấy dữ liệu nhân viên.")
                return
            
            self.original_data = data
            self.new_image_path = None
            self.load_employee_image(emp_id)
            
            self.view.details_emp_id.config(text=f"ID: {data['MaNguoiDung']}")
            self.view.details_hoten.delete(0, tk.END)
            self.view.details_hoten.insert(0, data['HoTen'])
            self.view.details_sdt.delete(0, tk.END)
            self.view.details_sdt.insert(0, data['SoDienThoai'] or "")
            self.view.details_email.delete(0, tk.END)
            self.view.details_email.insert(0, data['Email'] or "")
            
            # --- CẬP NHẬT CHỖ NÀY: Ánh xạ giá trị gốc sang Tiếng Việt để set Combobox ---
            # Ví dụ: data['VaiTro'] = 'QuanLy' -> set Combobox = 'Quản lý'
            display_vaitro = self.vaitro_map.get(data['VaiTro'], data['VaiTro'])
            display_trangthai = self.trangthai_map.get(data['TrangThai'], data['TrangThai'])
            
            # Phải đảm bảo danh sách values của Combobox trong file UI cũng là tiếng Việt
            # DÙNG DISPLAY VALUE ĐỂ SET CHO UI
            self.view.details_vaitro.set(display_vaitro)
            self.view.details_trangthai.set(display_trangthai)
            # -------------------------------------------------------------------------
            
            self.view.update_button.config(state="disabled")
        except IndexError:
            pass
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải chi tiết: {e}")

    def load_employee_image(self, emp_id, image_path=None):
        try:
            if image_path is None:
                image_path = os.path.join(self.resource_path, f"{emp_id}.png")
            if not os.path.exists(image_path):
                image_path = os.path.join(self.resource_path, "default_avatar.png")
            if not os.path.exists(image_path):
                img = Image.new('RGB', (150, 150), color='grey')
                img.save(image_path)
            img = Image.open(image_path)
            img = img.resize((150, 150), Image.Resampling.LANCZOS)
            self.view.employee_photo = ImageTk.PhotoImage(img)
            self.view.image_label.config(image=self.view.employee_photo)
        except Exception as e:
            print(f"Lỗi tải ảnh: {e}")
            pass

    def upload_image(self):
        try:
            file_path = filedialog.askopenfilename(
                title="Chọn ảnh đại diện mới",
                filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif")]
            )
            if not file_path:
                return
            self.new_image_path = file_path
            self.load_employee_image(None, image_path=file_path)
            self.check_for_changes()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở ảnh: {e}")

    def check_for_changes(self, event=None):
        if not self.original_data:
            return
        is_changed = False
        if self.new_image_path is not None:
            is_changed = True
            
        # --- Lấy giá trị gốc (mã) để so sánh với original_data ---
        # Ta cần map ngược giá trị tiếng Việt trong Combobox về mã gốc trước khi so sánh
        current_vaitro_vn = self.view.details_vaitro.get()
        current_trangthai_vn = self.view.details_trangthai.get()
        
        current_vaitro_code = self.vaitro_reverse_map.get(current_vaitro_vn, current_vaitro_vn)
        current_trangthai_code = self.trangthai_reverse_map.get(current_trangthai_vn, current_trangthai_vn)
        # ---------------------------------------------------------
        
        try:
            if self.view.details_hoten.get() != self.original_data.get('HoTen', ''):
                is_changed = True
            if self.view.details_sdt.get() != (self.original_data.get('SoDienThoai') or ""):
                is_changed = True
            if self.view.details_email.get() != (self.original_data.get('Email') or ""):
                is_changed = True
                
            # So sánh mã gốc
            if current_vaitro_code != self.original_data.get('VaiTro'):
                is_changed = True
            if current_trangthai_code != self.original_data.get('TrangThai'):
                is_changed = True
        except Exception:
            pass
            
        if is_changed:
            self.view.update_button.config(state="normal", cursor="hand2")
        else:
            self.view.update_button.config(state="disabled", cursor="")

    def update_employee(self):
        if not self.original_data:
            messagebox.showerror("Lỗi", "Không có nhân viên nào được chọn.")
            return
            
        # Lấy giá trị tiếng Việt từ Combobox
        new_vaitro_vn = self.view.details_vaitro.get()
        new_trangthai_vn = self.view.details_trangthai.get()
        
        # --- Ánh xạ ngược về mã gốc để lưu vào CSDL ---
        new_vaitro = self.vaitro_reverse_map.get(new_vaitro_vn, new_vaitro_vn)
        new_trangthai = self.trangthai_reverse_map.get(new_trangthai_vn, new_trangthai_vn)
        # -----------------------------------------------
        
        emp_id = self.original_data['MaNguoiDung']
        new_hoten = self.view.details_hoten.get().strip()
        new_sdt = self.view.details_sdt.get().strip()
        new_email = self.view.details_email.get().strip()
        
        if not new_hoten:
            messagebox.showwarning("Thiếu thông tin", "Họ tên không được để trống.")
            return
        if not (new_sdt.isdigit() and len(new_sdt) == 10):
            messagebox.showwarning("Sai định dạng", "Số điện thoại phải là 10 chữ số.")
            return
            
        try:
            if self.new_image_path:
                target_path = os.path.join(self.resource_path, f"{emp_id}.png")
                img = Image.open(self.new_image_path)
                img.save(target_path, "PNG")
                print(f"Đã thay thế ảnh cho ID {emp_id} tại {target_path}")
                self.new_image_path = None
        except Exception as e:
            messagebox.showerror("Lỗi Lưu Ảnh", f"Không thể lưu ảnh mới: {e}\n\nTuy nhiên, thông tin vẫn sẽ được cập nhật.")
            
        try:
            query = """
            UPDATE NguoiDung
            SET HoTen = %s, SoDienThoai = %s, Email = %s, VaiTro = %s, TrangThai = %s, NgayCapNhat = GETDATE()
            WHERE MaNguoiDung = %s
            """
            # SỬ DỤNG MÃ GỐC ĐÃ ÁNH XẠ NGƯỢC
            params = (new_hoten, new_sdt, new_email or None, new_vaitro, new_trangthai, emp_id)
            print("Params cập nhật:", params)
            result = self.db.execute_query(query, params)
            print("Kết quả cập nhật:", result)
            
            if result:
                messagebox.showinfo("Thành công", "Cập nhật thông tin nhân viên thành công.")
                self.load_view(self.view.employee_tree, self.view.search_entry.get())
                self.view.update_button.config(state="disabled")
                self.original_data = self.db.fetch_one("SELECT * FROM NguoiDung WHERE MaNguoiDung = %s", (emp_id,))
            else:
                messagebox.showerror("Lỗi", "Cập nhật CSDL thất bại.")
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Lỗi: {e}")
            print(f"Lỗi SQL khi update: {e}")