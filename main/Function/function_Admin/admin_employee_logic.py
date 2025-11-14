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
    
    def add_employee(self):
        """Mở cửa sổ Toplevel để thêm nhân viên mới"""
        dialog = tk.Toplevel(self.view.window) # Dùng self.view.window làm cha
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
            
            # Gọi CSDL qua self.db
            if self.db.execute_query(query, (*data, role_var.get())):
                messagebox.showinfo("Thành công", "Đã thêm nhân viên")
                dialog.destroy()
                self.load_employees() # Gọi lại hàm load của chính lớp này
            else: 
                messagebox.showerror("Lỗi", "Thất bại")
            
        tk.Button(dialog, text="💾 Lưu", bg="#28a745", fg="white", command=save).grid(row=len(fields)+1, columnspan=2, pady=20)

    def edit_employee(self):
        """Xử lý sửa nhân viên (Placeholder)"""
        # Truy cập treeview qua self.view.employee_tree
        if not self.view.employee_tree.selection():
            messagebox.showwarning("Chú ý", "Chọn nhân viên cần sửa")
            return
        messagebox.showinfo("Info", "Tính năng sửa nhân viên (chưa implement)")

    def delete_employee(self):
        """Xử lý xóa nhân viên"""
        sel = self.view.employee_tree.selection()
        if not sel: return
        
        id = self.view.employee_tree.item(sel[0])['values'][0]
        if messagebox.askyesno("Xóa", "Xóa nhân viên này?"):
            self.db.execute_query("DELETE FROM NguoiDung WHERE MaNguoiDung = %s", (id,))
            self.load_employees() # Tải lại dữ liệu