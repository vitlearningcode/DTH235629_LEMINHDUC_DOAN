# main/Function/function_Admin/admin_employee_logic.py
# (PHIÊN BẢN ĐÃ VIỆT HÓA TRẠNG THÁI)

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
        self.resource_path = os.path.join(os.path.dirname(__file__), "..", "..", "resource","NhanVien")
        if not os.path.exists(self.resource_path):
            os.makedirs(self.resource_path)
            
        self.original_data = {}
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
                # --- 1. CHUYỂN ĐỔI HIỂN THỊ TRẠNG THÁI ---
                trang_thai_hien_thi = "Hoạt động" if rec['TrangThai'] == 'HoatDong' else "Nghỉ làm"
                
                tree.insert(
                    "", tk.END,
                    values=(
                        rec['MaNguoiDung'], rec['HoTen'], rec['SoDienThoai'] or "",
                        rec['Email'] or "", rec['VaiTro'], 
                        trang_thai_hien_thi # Hiển thị tiếng Việt
                    )
                )

    def on_employee_select(self, event):
        """Xử lý khi bấm vào một nhân viên trên Treeview"""
        try:
            selection = self.view.employee_tree.selection()
            if not selection:
                return
            
            selected_item = selection[0]
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
            
            # --- 2. CẬP NHẬT COMBOBOX TRẠNG THÁI SANG TIẾNG VIỆT ---
            # Cập nhật danh sách lựa chọn trong Combobox
            self.view.details_trangthai['values'] = ["Hoạt động", "Nghỉ làm"]
            
            # Set giá trị hiện tại
            display_status = "Hoạt động" if data['TrangThai'] == 'HoatDong' else "Nghỉ làm"
            self.view.details_trangthai.set(display_status)
            
            self.view.update_button.config(state="disabled", cursor="")
            
        except IndexError:
            pass 
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
        """Kiểm tra thay đổi (Cần map ngược tiếng Việt về tiếng Anh để so sánh)"""
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
                
            # So sánh trạng thái: Convert hiển thị (Việt) về Data (Anh) để so sánh
            current_ui_status = self.view.details_trangthai.get()
            current_db_status = "HoatDong" if current_ui_status == "Hoạt động" else "KhongHoatDong"
            
            if current_db_status != self.original_data.get('TrangThai'):
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
        
        # --- 3. CHUYỂN ĐỔI TRƯỚC KHI LƯU (Việt -> Anh) ---
        ui_trangthai = self.view.details_trangthai.get()
        new_trangthai = "HoatDong" if ui_trangthai == "Hoạt động" else "KhongHoatDong"
        
        if not new_hoten:
            messagebox.showwarning("Thiếu thông tin", "Họ tên không được để trống.")
            return
        
        if new_sdt and not (new_sdt.isdigit() and len(new_sdt) == 10):
            messagebox.showwarning("Sai định dạng", "Số điện thoại phải là 10 chữ số.")
            return

        try:
            if self.new_image_path:
                target_path = os.path.join(self.resource_path, f"{emp_id}.png")
                img = Image.open(self.new_image_path)
                img.save(target_path, "PNG")
                self.new_image_path = None 
                
        except Exception as e:
            messagebox.showerror("Lỗi Lưu Ảnh", f"Không thể lưu ảnh mới: {e}")
            
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
                # Load lại dữ liệu gốc mới để so sánh cho lần sau
                self.original_data = self.db.fetch_one("SELECT * FROM NguoiDung WHERE MaNguoiDung = %s", (emp_id,))
            else:
                messagebox.showerror("Lỗi", "Cập nhật CSDL thất bại.")
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Lỗi: {e}")

    # --- CÁC HÀM GỐC CỦA ADMIN ---
    
    def _validate_phone(self, new_text):
        if new_text == "": return True
        if not new_text.isdigit(): return False
        if len(new_text) > 11: return False
        return True

    def add_employee(self):
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
            if key == "phone": entry.config(validate='key', validatecommand=vcmd)
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
        selected = self.view.employee_tree.selection()
        if not selected:
            messagebox.showwarning("Chú ý", "Vui lòng chọn một nhân viên để xóa.")
            return
        
        item = self.view.employee_tree.item(selected[0])
        emp_id = item['values'][0]
        emp_name = item['values'][1]
        # Lấy trạng thái hiển thị (Tiếng Việt)
        emp_status_display = item['values'][5] 

        # 4. KIỂM TRA TRẠNG THÁI TIẾNG VIỆT
        if emp_status_display == 'Hoạt động':
            messagebox.showwarning("Không thể xóa", f"Nhân viên '{emp_name}' đang HOẠT ĐỘNG.\nVui lòng chuyển trạng thái sang 'Nghỉ làm' trước.")
            return

        if str(emp_id) == str(self.view.user_info['MaNguoiDung']):
             messagebox.showerror("Lỗi", "Bạn không thể xóa tài khoản của chính mình.")
             return

        if messagebox.askyesno("Xác nhận xóa vĩnh viễn", 
                               f"CẢNH BÁO: Bạn đang xóa nhân viên '{emp_name}' (đã nghỉ việc).\n\n"
                               "Hành động này sẽ xóa lịch sử CHẤM CÔNG và gỡ tên khỏi các HÓA ĐƠN.\n"
                               "Bạn có chắc chắn muốn tiếp tục?"):
            try:
                self.db.execute_query("DELETE FROM ChamCong WHERE MaNguoiDung = %s", (emp_id,))
                self.db.execute_query("DELETE FROM ChamCong WHERE NguoiChamCong = %s", (emp_id,))
                self.db.execute_query("UPDATE HoaDon SET MaNguoiDung = NULL WHERE MaNguoiDung = %s", (emp_id,))
                self.db.execute_query("UPDATE PhieuNhapKho SET MaNguoiDung = NULL WHERE MaNguoiDung = %s", (emp_id,))
                self.db.execute_query("UPDATE LichSuBaoHanh SET NguoiXuLy = NULL WHERE NguoiXuLy = %s", (emp_id,))

                query = "DELETE FROM NguoiDung WHERE MaNguoiDung = %s"
                result = self.db.execute_query(query, (emp_id,))
                
                if result:
                    messagebox.showinfo("Thành công", f"Đã xóa nhân viên {emp_name}.")
                    self.load_view(self.view.employee_tree, self.view.search_entry.get())
                    
                    self.view.details_emp_id.config(text="ID: (Chưa chọn)")
                    self.view.details_hoten.delete(0, tk.END)
                    self.view.details_sdt.delete(0, tk.END)
                    self.view.details_email.delete(0, tk.END)
                    self.view.details_vaitro.set('')
                    self.view.details_trangthai.set('')
                    self.view.image_label.config(image=None) 
                    self.original_data = {}
                    self.view.update_button.config(state="disabled")
                else:
                    messagebox.showerror("Lỗi", "Xóa thất bại.")
            except Exception as e:
                messagebox.showerror("Lỗi CSDL", f"Lỗi: {e}")