# main/Function/function_NhanVien/nhanvien_customer_logic.py

import tkinter as tk
from tkinter import messagebox, ttk

class NhanVienCustomerLogic:
    def __init__(self, view):
        self.view = view
        self.db = view.db

    def _validate_phone(self, new_text):
        """Chỉ cho phép nhập số và giới hạn 11 ký tự"""
        if new_text == "":
            return True  # Cho phép xóa (chuỗi rỗng)
        if not new_text.isdigit():
            return False # Từ chối nếu không phải là số
        if len(new_text) > 11:
            return False # Từ chối nếu dài hơn 11 số
        return True
    
    # main/Function/function_NhanVien/nhanvien_customer_logic.py
# ... (bên dưới hàm _validate_phone)

    def on_phone_entry_release(self, event):
        """Tự động tìm kiếm khi SĐT đủ 10 số."""
        phone = event.widget.get().strip()
        
        # Chỉ tự động tìm kiếm khi gõ đủ 10 số
        if len(phone) == 10 and phone.isdigit():
            # Gọi hàm tìm kiếm và báo nó tự động thêm nếu không thấy
            self.search_customer_by_phone(auto_add=True)
        # Nếu gõ < 10 hoặc > 10, xóa tên (nếu có)
        elif len(phone) != 10:
             self.view.customer_name_var.set("")
             if hasattr(self.view, 'current_customer'):
                del self.view.current_customer
                
                
    # main/Function/function_NhanVien/nhanvien_customer_logic.py
# (THAY THẾ HÀM CŨ BẰNG HÀM MỚI NÀY)

    def search_customer_by_phone(self, auto_add=False):
        """
        Tìm khách hàng theo SĐT.
        :param auto_add: Nếu True, tự động mở 'Thêm mới' khi không tìm thấy.
                         Nếu False (default), hỏi người dùng trước.
        """
        phone = self.view.phone_entry.get().strip()
        
        # 1. Kiểm tra SĐT phải là 10 số
        if not (len(phone) == 10 and phone.isdigit()):
            messagebox.showwarning("Cảnh báo", "Số điện thoại hợp lệ phải có 10 chữ số.")
            # Xóa thông tin khách hàng cũ nếu SĐT không hợp lệ
            self.view.customer_name_var.set("")
            if hasattr(self.view, 'current_customer'):
                del self.view.current_customer
            return
        
        # 2. SĐT hợp lệ (10 số), tiến hành tìm kiếm
        query = "SELECT * FROM KhachHang WHERE SoDienThoai = %s"
        customer = self.db.fetch_one(query, (phone,))
        
        if customer:
            # 3. Tìm thấy
            self.view.current_customer = customer
            self.view.customer_name_var.set(customer['HoTen'])
            if not auto_add: # Nếu là bấm nút "Tìm"
                messagebox.showinfo("Thành công", f"Tìm thấy khách hàng: {customer['HoTen']}")
        else:
            # 4. Không tìm thấy
            self.view.customer_name_var.set("")
            if hasattr(self.view, 'current_customer'):
                del self.view.current_customer
            
            if auto_add:
                # Nếu gọi từ <KeyRelease>, tự động thêm
                messagebox.showwarning("Không tìm thấy", f"SĐT {phone} không có trong hệ thống.\nVui lòng thêm khách hàng mới.")
                self.add_new_customer()
            else:
                # Nếu gọi từ nút "Tìm", hỏi người dùng (như logic cũ)
                if messagebox.askyesno("Không tìm thấy", "Khách hàng chưa có trong hệ thống.\nBạn có muốn thêm mới?"):
                    self.add_new_customer()
    
    def add_new_customer(self):
        """Thêm khách hàng mới"""
        dialog = tk.Toplevel(self.view.window)
        dialog.title("Thêm khách hàng")
        dialog.geometry("450x400")
        dialog.resizable(False, False)
        
        vcmd = (dialog.register(self._validate_phone), '%P')
        fields = [
            ("Họ tên:", "fullname"),
            ("Số điện thoại:", "phone"),
            ("Email:", "email"),
            ("Địa chỉ:", "address"),
            ("CMND:", "cmnd")
        ]
        
        entries = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(dialog, text=label, font=("Arial", 11)).grid(row=i, column=0, padx=20, pady=10, sticky="w")
            entry = tk.Entry(dialog, font=("Arial", 11), width=30)
            if key == "phone":
                entry.config(validate='key', validatecommand=vcmd)
            entry.grid(row=i, column=1, padx=20, pady=10)
            entries[key] = entry
        
        tk.Label(dialog, text="Giới tính:", font=("Arial", 11)).grid(row=len(fields), column=0, padx=20, pady=10, sticky="w")
        gender_var = tk.StringVar(value="Nam")
        gender_combo = ttk.Combobox(dialog, textvariable=gender_var, values=["Nam", "Nu", "Khac"], 
                                    font=("Arial", 11), state="readonly", width=28)
        gender_combo.grid(row=len(fields), column=1, padx=20, pady=10)
        
        def save():
            fullname = entries["fullname"].get().strip()
            phone = entries["phone"].get().strip()
            email = entries["email"].get().strip()
            address = entries["address"].get().strip()
            cmnd = entries["cmnd"].get().strip()
            
            if not fullname or not phone:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập họ tên và số điện thoại!")
                return
            
            query = """
                INSERT INTO KhachHang (HoTen, SoDienThoai, Email, DiaChi, CMND, GioiTinh)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            result = self.db.execute_query(query, (fullname, phone, email, address, cmnd, gender_var.get()))
            
            if result:
                messagebox.showinfo("Thành công", "Thêm khách hàng thành công!")
                self.view.phone_entry.delete(0, tk.END)
                self.view.phone_entry.insert(0, phone)
                dialog.destroy()
                self.search_customer_by_phone() # Tự động tìm lại
            else:
                messagebox.showerror("Lỗi", "Không thể thêm khách hàng!")
        
        tk.Button(
            dialog,
            text="💾 Lưu",
            font=("Arial", 12, "bold"),
            bg="#28a745",
            fg="white",
            command=save,
            width=15
        ).grid(row=len(fields)+1, column=0, columnspan=2, pady=20)