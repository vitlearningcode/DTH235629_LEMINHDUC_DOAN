# main/Function/function_Admin/admin_attendance_logic.py
# (Nội dung được sao chép từ quanly_attendance_logic.py)

import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, date

class AdminAttendanceLogic: # <-- ĐÃ ĐỔI TÊN CLASS
    def __init__(self, view):
        self.view = view
        self.db = view.db

    def load_attendance(self):
        """Tải dữ liệu chấm công"""
        for item in self.view.attendance_tree.get_children():
            self.view.attendance_tree.delete(item)
        
        selected_date = self.view.date_var.get()
        
        query = """
            SELECT nd.MaNguoiDung, nd.HoTen, 
                   cc.GioVao, cc.GioRa, cc.SoGioLam, cc.TrangThai
            FROM NguoiDung nd
            LEFT JOIN ChamCong cc ON nd.MaNguoiDung = cc.MaNguoiDung 
                                  AND cc.NgayChamCong = %s
            WHERE nd.VaiTro IN ('NhanVien', 'QuanLy')
            ORDER BY nd.MaNguoiDung
        """
        records = self.db.fetch_all(query, (selected_date,))
        
        if records:
            for rec in records:
                # --- CHUYỂN ĐỔI TRẠNG THÁI SANG TIẾNG VIỆT ---
                raw_status = rec['TrangThai']
                display_status = "Chưa chấm"
                
                if raw_status == 'DiLam':
                    display_status = "Đi làm"
                elif raw_status == 'VangMat':
                    display_status = "Vắng mặt"
                elif raw_status == 'NghiPhep':
                    display_status = "Nghỉ phép"
                elif raw_status == 'DiTre':
                    display_status = "Đi trễ"
                
                self.view.attendance_tree.insert("", tk.END, values=(
                    rec['MaNguoiDung'],
                    rec['HoTen'],
                    rec['GioVao'] or "",
                    rec['GioRa'] or "",
                    rec['SoGioLam'] or "",
                    display_status
                ))
    
    def add_attendance(self):
        """Mở cửa sổ Toplevel để thêm/sửa chấm công"""
        selected = self.view.attendance_tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn nhân viên!")
            return
        
        emp_id = self.view.attendance_tree.item(selected[0])['values'][0]
        selected_date = self.view.date_var.get()
        
        dialog = tk.Toplevel(self.view.window)
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
            values=["Đi làm", "Vắng mặt", "Nghỉ phép", "Đi trễ"],
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
                
                # --- CHUYỂN ĐỔI TRẠNG THÁI TỪ TIẾNG VIỆT SANG TIẾNG ANH TRƯỚC KHI LƯU ---
                status_text = status_var.get()
                status_db = "DiLam"
                
                if status_text == "Đi làm":
                    status_db = "DiLam"
                elif status_text == "Vắng mặt":
                    status_db = "VangMat"
                elif status_text == "Nghỉ phép":
                    status_db = "NghiPhep"
                elif status_text == "Đi trễ":
                    status_db = "DiTre"
                
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
                        (gio_vao.get(), gio_ra.get(), hours, status_db, self.view.user_info['MaNguoiDung'], emp_id, selected_date)
                    )
                else:
                    insert_query = """
                        INSERT INTO ChamCong (MaNguoiDung, NgayChamCong, GioVao, GioRa, SoGioLam, TrangThai, NguoiChamCong)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                    result = self.db.execute_query(
                        insert_query,
                        (emp_id, selected_date, gio_vao.get(), gio_ra.get(), hours, status_db, self.view.user_info['MaNguoiDung'])
                    )
                
                if result is not None:
                    messagebox.showinfo("Thành công", "Chấm công thành công!")
                    dialog.destroy()
                    self.load_attendance()
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