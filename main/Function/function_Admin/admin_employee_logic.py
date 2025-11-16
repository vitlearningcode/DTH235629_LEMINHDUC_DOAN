# main/Function/function_Admin/admin_employee_logic.py

import tkinter as tk
from tkinter import messagebox, ttk

class AdminEmployeeLogic:
    def __init__(self, view):
        self.view = view
        self.db = view.db

    def load_employees(self):
        """Tải dữ liệu nhân viên lên treeview"""
        # Truy cập treeview qua self.view.employee_tree
        for item in self.view.employee_tree.get_children(): 
            self.view.employee_tree.delete(item)
        
        query = "SELECT MaNguoiDung, TenDangNhap, HoTen, SoDienThoai, Email, VaiTro, TrangThai FROM NguoiDung ORDER BY MaNguoiDung"
        employees = self.db.fetch_all(query)
        for emp in employees:
            self.view.employee_tree.insert("", tk.END, values=(
                emp['MaNguoiDung'], emp['TenDangNhap'], emp['HoTen'], emp['SoDienThoai'] or "", emp['Email'] or "", emp['VaiTro'], emp['TrangThai']
            ))
    
    def _validate_phone(self, new_text):
        """Chỉ cho phép nhập số và giới hạn 11 ký tự"""
        if new_text == "":
            return True  # Cho phép xóa (chuỗi rỗng)
        if not new_text.isdigit():
            return False # Từ chối nếu không phải là số
        if len(new_text) > 11:
            return False # Từ chối nếu dài hơn 11 số
        return True

    def add_employee(self):
        """Mở cửa sổ Toplevel để thêm nhân viên mới"""
        dialog = tk.Toplevel(self.view.window) # Dùng self.view.window làm cha
        dialog.title("Thêm nhân viên")
        dialog.geometry("500x500")

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
                messagebox.showwarning("Cảnh báo", "Nhập đủ thông tin bắt buộc!")
                return
            
            query = "INSERT INTO NguoiDung (TenDangNhap, MatKhau, HoTen, SoDienThoai, Email, DiaChi, VaiTro) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            
            # Gọi CSDL qua self.db
            if self.db.execute_query(query, (*data, role_var.get())):
                messagebox.showinfo("Thành công", "Đã thêm nhân viên")
                dialog.destroy()
                self.load_employees() # Gọi lại hàm load của chính lớp này
            else: 
                messagebox.showerror("Lỗi", "Thất bại")
            
        tk.Button(dialog, text="💾 Lưu", bg="#28a745", fg="white", command=save).grid(row=len(fields)+1, columnspan=2, pady=20)

    def edit_employee(self):
        """Mở cửa sổ Toplevel để sửa thông tin nhân viên"""
        
        # 1. Lấy nhân viên đang được chọn
        selected = self.view.employee_tree.selection()
        if not selected:
            messagebox.showwarning("Chú ý", "Vui lòng chọn một nhân viên để sửa.")
            return
        
        item = self.view.employee_tree.item(selected[0])
        emp_id = item['values'][0]
        
        # 2. Lấy dữ liệu đầy đủ của nhân viên đó từ CSDL
        query = "SELECT * FROM NguoiDung WHERE MaNguoiDung = %s"
        employee_data = self.db.fetch_one(query, (emp_id,))
        
        if not employee_data:
            messagebox.showerror("Lỗi", "Không tìm thấy dữ liệu nhân viên trong CSDL.")
            return

        # 3. Tạo cửa sổ Toplevel mới
        dialog = tk.Toplevel(self.view.window)
        dialog.title(f"Sửa thông tin nhân viên (ID: {emp_id})")
        dialog.geometry("500x550") # Cao hơn một chút để chứa trường "Trạng thái"
        dialog.grab_set() # Giữ focus
        vcmd = (dialog.register(self._validate_phone), '%P')
        entries = {}
        
        # Tên đăng nhập (Chỉ đọc, không cho sửa)
        tk.Label(dialog, text="Tên đăng nhập:", font=("Arial", 11)).grid(row=0, column=0, padx=20, pady=10, sticky="w")
        username_entry = tk.Entry(dialog, font=("Arial", 11), width=30)
        username_entry.grid(row=0, column=1, padx=20, pady=10)
        username_entry.insert(0, employee_data['TenDangNhap'])
        username_entry.config(state="readonly")
        
        # Mật khẩu mới (để trống nếu không muốn thay đổi)
        tk.Label(dialog, text="Mật khẩu mới (nếu đổi):", font=("Arial", 11)).grid(row=1, column=0, padx=20, pady=10, sticky="w")
        password_entry = tk.Entry(dialog, font=("Arial", 11), width=30, show="*")
        password_entry.grid(row=1, column=1, padx=20, pady=10)
        entries['password'] = password_entry
        
        # Các trường thông tin khác
        fields = [("Họ tên:", "fullname", "HoTen"), 
                  ("Số điện thoại:", "phone", "SoDienThoai"), 
                  ("Email:", "email", "Email"), 
                  ("Địa chỉ:", "address", "DiaChi")]
        
        for i, (label_text, key, db_key) in enumerate(fields, start=2):
            tk.Label(dialog, text=label_text, font=("Arial", 11)).grid(row=i, column=0, padx=20, pady=10, sticky="w")
            entry = tk.Entry(dialog, font=("Arial", 11), width=30)
            if key == "phone":
                entry.config(validate='key', validatecommand=vcmd)
            entry.grid(row=i, column=1, padx=20, pady=10)
            # Dùng .get(db_key) or "" để tránh lỗi nếu giá trị là None
            entry.insert(0, employee_data.get(db_key) or "") 
            entries[key] = entry
            
        # Vai trò (Combobox)
        row_index = len(fields) + 2
        tk.Label(dialog, text="Vai trò:", font=("Arial", 11)).grid(row=row_index, column=0, padx=20, pady=10, sticky="w")
        role_var = tk.StringVar(value=employee_data['VaiTro'])
        role_combo = ttk.Combobox(dialog, textvariable=role_var, values=["Admin", "QuanLy", "NhanVien"], state="readonly", width=28)
        role_combo.grid(row=row_index, column=1, padx=20, pady=10)
        
        # Trạng thái (Combobox)
        row_index += 1
        tk.Label(dialog, text="Trạng thái:", font=("Arial", 11)).grid(row=row_index, column=0, padx=20, pady=10, sticky="w")
        status_var = tk.StringVar(value=employee_data['TrangThai'])
        status_combo = ttk.Combobox(dialog, textvariable=status_var, values=["HoatDong", "KhongHoatDong"], state="readonly", width=28)
        status_combo.grid(row=row_index, column=1, padx=20, pady=10)

        # 4. Hàm lưu thay đổi
        def save_changes():
            # Lấy dữ liệu từ các ô nhập
            data = {
                'fullname': entries['fullname'].get().strip(),
                'phone': entries['phone'].get().strip() or None, # Lưu None nếu rỗng
                'email': entries['email'].get().strip() or None, # Lưu None nếu rỗng
                'address': entries['address'].get().strip() or None, # Lưu None nếu rỗng
                'role': role_var.get(),
                'status': status_var.get()
            }
            new_password = entries['password'].get().strip()

            if not data['fullname']:
                messagebox.showwarning("Cảnh báo", "Họ tên không được để trống!", parent=dialog)
                return

            # Xây dựng câu lệnh UPDATE
            query_parts = [
                "HoTen = %s", "SoDienThoai = %s", "Email = %s", 
                "DiaChi = %s", "VaiTro = %s", "TrangThai = %s"
            ]
            params = [
                data['fullname'], data['phone'], data['email'], 
                data['address'], data['role'], data['status']
            ]
            
            # Chỉ cập nhật mật khẩu nếu người dùng nhập mật khẩu mới
            if new_password:
                query_parts.append("MatKhau = %s")
                params.append(new_password) # Lưu ý: nên mã hóa mật khẩu ở đây
            
            # Thêm MaNguoiDung vào cuối danh sách params cho mệnh đề WHERE
            params.append(emp_id) 
            
            query = f"UPDATE NguoiDung SET {', '.join(query_parts)} WHERE MaNguoiDung = %s"
            
            try:
                if self.db.execute_query(query, tuple(params)):
                    messagebox.showinfo("Thành công", "Đã cập nhật thông tin nhân viên.", parent=dialog)
                    dialog.destroy()
                    self.load_employees() # Tải lại cây danh sách nhân viên
                else:
                    messagebox.showerror("Lỗi", "Cập nhật thất bại.", parent=dialog)
            except Exception as e:
                messagebox.showerror("Lỗi CSDL", f"Lỗi khi cập nhật: {e}", parent=dialog)

        # 5. Nút lưu
        tk.Button(dialog, text="💾 Lưu thay đổi", bg="#007bff", fg="white", font=("Arial", 11, "bold"), command=save_changes).grid(row=row_index+1, columnspan=2, pady=20)
    # --- KẾT THÚC PHẦN ĐƯỢC CẬP NHẬT ---

    def delete_employee(self):
        """Xử lý xóa nhân viên"""
        sel = self.view.employee_tree.selection()
        if not sel: return
        
        id = self.view.employee_tree.item(sel[0])['values'][0]
        if messagebox.askyesno("Xóa", "Xóa nhân viên này?"):
            self.db.execute_query("DELETE FROM NguoiDung WHERE MaNguoiDung = %s", (id,))
            self.load_employees() # Tải lại dữ liệu