# main/Function/function_NhanVien/nhanvien_customer_logic.py

import tkinter as tk
from tkinter import messagebox, ttk

class NhanVienCustomerLogic:
    def __init__(self, view):
        self.view = view
        self.db = view.db

    def search_customer_by_phone(self):
        """Tìm khách hàng theo SĐT"""
        phone = self.view.phone_entry.get().strip()
        if not phone:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập số điện thoại!")
            return
        
        query = "SELECT * FROM KhachHang WHERE SoDienThoai = %s"
        customer = self.db.fetch_one(query, (phone,))
        
        if customer:
            self.view.current_customer = customer
            self.view.customer_name_var.set(customer['HoTen'])
            messagebox.showinfo("Thành công", f"Tìm thấy khách hàng: {customer['HoTen']}")
        else:
            self.view.customer_name_var.set("")
            if messagebox.askyesno("Không tìm thấy", "Khách hàng chưa có trong hệ thống.\nBạn có muốn thêm mới?"):
                self.add_new_customer() # Gọi hàm nội bộ
    
    def add_new_customer(self):
        """Thêm khách hàng mới"""
        dialog = tk.Toplevel(self.view.window)
        dialog.title("Thêm khách hàng")
        dialog.geometry("450x400")
        dialog.resizable(False, False)
        
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