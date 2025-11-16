# main/Function/function_Admin/admin_employee_logic.py
# (PHIÊN BẢN NÂNG CẤP - KẾT HỢP PANEL CHI TIẾT VÀ QUYỀN ADMIN)

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os
import shutil

class AdminEmployeeLogic:
    def __init__(self, view):
        self.view = view
        self.db = view.db
        
        # Đường dẫn đến thư mục chứa ảnh avatar
        self.resource_path = os.path.join(os.path.dirname(__file__), "..", "..", "resource")
        if not os.path.exists(self.resource_path):
            os.makedirs(self.resource_path)
            
        # Dùng để lưu trữ dữ liệu gốc khi chọn nhân viên
        self.original_data = {}
        # Dùng để lưu đường dẫn ảnh mới khi upload
        self.new_image_path = None

    def load_view(self, tree, keyword=None):
        """Tải dữ liệu nhân viên lên treeview (thay cho load_employees)"""
        for item in tree.get_children():
            tree.delete(item)
            
        # Admin có thể thấy tất cả các vai trò
        query = """
        SELECT MaNguoiDung, HoTen, SoDienThoai, Email, VaiTro, TrangThai
        FROM NguoiDung
        WHERE (VaiTro = 'NhanVien' OR VaiTro = 'QuanLy' OR VaiTro = 'Admin')
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
        """Xử lý khi bấm vào một nhân viên trên Treeview"""
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
                
            # Lưu dữ liệu gốc và reset đường dẫn ảnh
            self.original_data = data
            self.new_image_path = None
            
            # Tải ảnh và cập nhật thông tin lên panel
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
            
            # Vô hiệu hóa nút cập nhật
            self.view.update_button.config(state="disabled", cursor="")
            
        except IndexError:
            pass # Lỗi khi click vào khoảng trống
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải chi tiết: {e}")

    def load_employee_image(self, emp_id, image_path=None):
        """Tải và hiển thị ảnh avatar"""
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
        """Mở cửa sổ chọn file để tải ảnh mới"""
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
        """Kiểm tra xem thông tin trên panel có bị thay đổi so với gốc không"""
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
        """Lưu các thay đổi từ panel chi tiết vào CSDL"""
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
        
        # Thêm kiểm tra SĐT (logic từ file quanly)
        if new_sdt and not (new_sdt.isdigit() and len(new_sdt) == 10):
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
            params = (new_hoten, new_sdt or None, new_email or None, new_vaitro, new_trangthai, emp_id)
            
            result = self.db.execute_query(query, params)
            
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

    # --- CÁC HÀM GỐC CỦA ADMIN (THÊM, XÓA, VALIDATE) ---
    
    def _validate_phone(self, new_text):
        """Chỉ cho phép nhập số và giới hạn 11 ký tự"""
        if new_text == "":
            return True
        if not new_text.isdigit():
            return False
        if len(new_text) > 11:
            return False
        return True

    def add_employee(self):
        """Mở cửa sổ Toplevel để thêm nhân viên mới (Giữ nguyên logic popup)"""
        dialog = tk.Toplevel(self.view.window) 
        dialog.title("Thêm nhân viên")
        dialog.geometry("500x500")
        dialog.grab_set()

        vcmd = (dialog.register(self._validate_phone), '%P')
        
        fields = [("Tên đăng nhập:", "username"), ("Mật khẩu:", "password"), ("Họ tên:", "fullname"), 
                  ("Số điện thoại:", "phone"), ("Email:", "email"), ("Địa chỉ:", "address")]
        entries = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(dialog, text=label, font=("Arial", 11)).grid(row=i, column=0, padx=20, pady=10, sticky="w")
            entry = tk.Entry(dialog, font=("Arial", 11), width=30)
            if key == "password": entry.config(show="*")
            if key == "phone":
                entry.config(validate='key', validatecommand=vcmd)
            entry.grid(row=i, column=1, padx=20, pady=10)
            entries[key] = entry
            
        tk.Label(dialog, text="Vai trò:", font=("Arial", 11)).grid(row=len(fields), column=0, padx=20, pady=10, sticky="w")
        role_var = tk.StringVar(value="NhanVien")
        ttk.Combobox(dialog, textvariable=role_var, values=["Admin", "QuanLy", "NhanVien"], state="readonly", width=28).grid(row=len(fields), column=1, padx=20, pady=10)
        
        def save():
            data = [entries[k].get().strip() for k in ["username", "password", "fullname", "phone", "email", "address"]]
            if not data[0] or not data[1] or not data[2]:
                messagebox.showwarning("Cảnh báo", "Nhập đủ thông tin bắt buộc!", parent=dialog)
                return
            
            query = "INSERT INTO NguoiDung (TenDangNhap, MatKhau, HoTen, SoDienThoai, Email, DiaChi, VaiTro) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            
            if self.db.execute_query(query, (*data, role_var.get())):
                messagebox.showinfo("Thành công", "Đã thêm nhân viên", parent=dialog)
                dialog.destroy()
                self.load_view(self.view.employee_tree) 
            else: 
                messagebox.showerror("Lỗi", "Thất bại (Có thể trùng Tên đăng nhập)", parent=dialog)
            
        tk.Button(dialog, text="💾 Lưu", bg="#28a745", fg="white", command=save).grid(row=len(fields)+1, columnspan=2, pady=20)

    def delete_employee(self):
        """Xử lý xóa nhân viên (Giữ nguyên logic)"""
        selected = self.view.employee_tree.selection()
        if not selected:
            messagebox.showwarning("Chú ý", "Vui lòng chọn một nhân viên để xóa.")
            return
        
        item = self.view.employee_tree.item(selected[0])
        emp_id = item['values'][0]
        emp_name = item['values'][1]

        # Kiểm tra không cho tự xóa
        if emp_id == self.view.user_info['MaNguoiDung']:
             messagebox.showerror("Lỗi", "Bạn không thể tự xóa chính mình.")
             return

        if messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc muốn XÓA nhân viên:\n\n{emp_name} (ID: {emp_id})?"):
            try:
                result = self.db.execute_query("DELETE FROM NguoiDung WHERE MaNguoiDung = %s", (emp_id,))
                if result:
                    messagebox.showinfo("Thành công", "Đã xóa nhân viên.")
                    self.load_view(self.view.employee_tree) # Tải lại cây
                    # Xóa thông tin khỏi panel chi tiết
                    self.view.details_emp_id.config(text="ID: (Chưa chọn)")
                    self.view.details_hoten.delete(0, tk.END)
                    self.view.details_sdt.delete(0, tk.END)
                    self.view.details_email.delete(0, tk.END)
                    self.view.image_label.config(image=None) 
                    self.original_data = {}
                else:
                    messagebox.showerror("Lỗi", "Xóa thất bại.")
            except Exception as e:
                messagebox.showerror("Lỗi CSDL", f"Không thể xóa nhân viên này, có thể do ràng buộc dữ liệu (ví dụ: đã chấm công, lập hóa đơn).\nLỗi: {e}")