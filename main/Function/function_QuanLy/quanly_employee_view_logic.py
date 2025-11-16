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
                tree.insert(
                    "", tk.END,
                    values=(
                        rec['MaNguoiDung'], rec['HoTen'], rec['SoDienThoai'] or "",
                        rec['Email'] or "", rec['VaiTro'], rec['TrangThai']
                    )
                )

    def on_employee_select(self, event):
        try:
            selected_item = self.view.employee_tree.selection()[0]
            values = self.view.employee_tree.item(selected_item, 'values')
            if not values:
                return
            emp_id = values[0]
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
            self.view.details_vaitro.set(data['VaiTro'])
            self.view.details_trangthai.set(data['TrangThai'])
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
        try:
            if self.view.details_hoten.get() != self.original_data.get('HoTen', ''):
                is_changed = True
            if self.view.details_sdt.get() != (self.original_data.get('SoDienThoai') or ""):
                is_changed = True
            if self.view.details_email.get() != (self.original_data.get('Email') or ""):
                is_changed = True
            if self.view.details_vaitro.get() != self.original_data.get('VaiTro'):
                is_changed = True
            if self.view.details_trangthai.get() != self.original_data.get('TrangThai'):
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
        emp_id = self.original_data['MaNguoiDung']
        new_hoten = self.view.details_hoten.get().strip()
        new_sdt = self.view.details_sdt.get().strip()
        new_email = self.view.details_email.get().strip()
        new_vaitro = self.view.details_vaitro.get()
        new_trangthai = self.view.details_trangthai.get()
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
    