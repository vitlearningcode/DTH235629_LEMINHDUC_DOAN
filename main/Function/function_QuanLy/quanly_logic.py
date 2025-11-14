# main/Function/function_QuanLy/quanly_logic.py

import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, date

# 1. KHÔNG IMPORT LOGIN Ở ĐÂY
# from login import Login  <-- XÓA DÒNG NÀY

class QuanLyLogic:
    def __init__(self, view):
        """
        Khởi tạo lớp logic cho Quản Lý.
        :param view: Thể hiện của lớp QuanLy (quanly_window.py)
        """
        self.view = view
        self.db = view.db # Lấy kết nối CSDL từ view

    def load_attendance(self):
        """Tải dữ liệu chấm công"""
        # Truy cập treeview qua self.view.attendance_tree
        for item in self.view.attendance_tree.get_children():
            self.view.attendance_tree.delete(item)
        
        # Truy cập biến ngày qua self.view.date_var
        selected_date = self.view.date_var.get()
        
        query = """
            SELECT nd.MaNguoiDung, nd.HoTen, 
                   cc.GioVao, cc.GioRa, cc.SoGioLam, cc.TrangThai
            FROM NguoiDung nd
            LEFT JOIN ChamCong cc ON nd.MaNguoiDung = cc.MaNguoiDung 
                                  AND cc.NgayChamCong = %s
            WHERE nd.VaiTro = 'NhanVien'
            ORDER BY nd.MaNguoiDung
        """
        records = self.db.fetch_all(query, (selected_date,))
        
        if records:
            for rec in records:
                self.view.attendance_tree.insert("", tk.END, values=(
                    rec['MaNguoiDung'],
                    rec['HoTen'],
                    rec['GioVao'] or "",
                    rec['GioRa'] or "",
                    rec['SoGioLam'] or "",
                    rec['TrangThai'] or "Chưa chấm"
                ))
    
    def add_attendance(self):
        """Mở cửa sổ Toplevel để thêm/sửa chấm công"""
        selected = self.view.attendance_tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn nhân viên!")
            return
        
        emp_id = self.view.attendance_tree.item(selected[0])['values'][0]
        selected_date = self.view.date_var.get()
        
        # Dialog chấm công
        dialog = tk.Toplevel(self.view.window) # Dùng self.view.window làm cha
        dialog.title("Chấm công")
        dialog.geometry("400x350")
        dialog.resizable(False, False)
        
        tk.Label(dialog, text="CHẤM CÔNG NHÂN VIÊN", font=("Arial", 14, "bold")).pack(pady=20)
        
        tk.Label(dialog, text="Giờ vào (HH:MM):", font=("Arial", 11)).pack(pady=5)
        gio_vao = tk.Entry(dialog, font=("Arial", 11), width=20)
        gio_vao.pack(pady=5)
        gio_vao.insert(0, "08:00")
        
        tk.Label(dialog, text="Giờ ra (HH:MM):", font=("Arial", 11)).pack(pady=5)
        gio_ra = tk.Entry(dialog, font=("Arial", 11), width=20)
        gio_ra.pack(pady=5)
        gio_ra.insert(0, "17:00")
        
        tk.Label(dialog, text="Trạng thái:", font=("Arial", 11)).pack(pady=5)
        status_var = tk.StringVar(value="DiLam")
        status_combo = ttk.Combobox(
            dialog,
            textvariable=status_var,
            values=["DiLam", "VangMat", "NghiPhep", "DiTre"],
            font=("Arial", 11),
            state="readonly",
            width=18
        )
        status_combo.pack(pady=5)
        
        def save():
            try:
                h1, m1 = map(int, gio_vao.get().split(':'))
                h2, m2 = map(int, gio_ra.get().split(':'))
                hours = (h2 * 60 + m2 - h1 * 60 - m1) / 60
                
                # --- SỬA LỖI TƯƠNG THÍCH SQL SERVER ---
                check_query = "SELECT MaChamCong FROM ChamCong WHERE MaNguoiDung = %s AND NgayChamCong = %s"
                existing = self.db.fetch_one(check_query, (emp_id, selected_date))
                
                result = None
                
                if existing:
                    update_query = """
                        UPDATE ChamCong 
                        SET GioVao = %s, GioRa = %s, SoGioLam = %s, TrangThai = %s, NguoiChamCong = %s
                        WHERE MaNguoiDung = %s AND NgayChamCong = %s
                    """
                    result = self.db.execute_query(
                        update_query,
                        (gio_vao.get(), gio_ra.get(), hours, status_var.get(), self.view.user_info['MaNguoiDung'], emp_id, selected_date)
                    )
                else:
                    insert_query = """
                        INSERT INTO ChamCong (MaNguoiDung, NgayChamCong, GioVao, GioRa, SoGioLam, TrangThai, NguoiChamCong)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                    result = self.db.execute_query(
                        insert_query,
                        (emp_id, selected_date, gio_vao.get(), gio_ra.get(), hours, status_var.get(), self.view.user_info['MaNguoiDung'])
                    )
                
                if result is not None:
                    messagebox.showinfo("Thành công", "Chấm công thành công!")
                    dialog.destroy()
                    self.load_attendance() # Tải lại danh sách
                else:
                    messagebox.showerror("Lỗi", "Không thể chấm công!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Định dạng giờ không đúng hoặc có lỗi khác!\n{e}")
        
        tk.Button(
            dialog,
            text="💾 Lưu",
            font=("Arial", 12, "bold"),
            bg="#28a745",
            fg="white",
            command=save,
            width=15
        ).pack(pady=20)

    def logout(self):
        """Đăng xuất"""
        # 2. IMPORT LOGIN TẠI ĐÂY
        from login import Login 

        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn đăng xuất?"):
            self.db.disconnect()
            self.view.window.destroy()
            Login().run() # Khởi tạo và chạy lại cửa sổ Login
    
    def on_closing(self):
        """Xử lý đóng cửa sổ"""
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn thoát?"):
            self.db.disconnect()
            self.view.window.destroy()  