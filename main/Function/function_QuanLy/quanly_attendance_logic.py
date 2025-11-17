    # main/Function/function_QuanLy/quanly_attendance_logic.py
# (File này TRƯỚC ĐÂY là quanly_logic.py)

import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, date

class QuanLyAttendanceLogic:
    def __init__(self, view):
        self.view = view
        self.db = view.db

        # Ánh xạ trạng thái CSDL -> Tiếng Việt
        self.STATUS_MAPPING = {
            "DiLam": "Đi làm",
            "VangMat": "Vắng mặt",
            "NghiPhep": "Nghỉ phép",
            "DiTre": "Đi trễ",
            "ChuaCham": "Chưa chấm"
        }
        self.INVERSE_STATUS_MAPPING = {v: k for k, v in self.STATUS_MAPPING.items()}

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
            WHERE nd.VaiTro = 'NhanVien'
            ORDER BY nd.MaNguoiDung
        """
        records = self.db.fetch_all(query, (selected_date,))
        
        if records:
            for rec in records:
                trang_thai_db = rec.get('TrangThai')
                trang_thai_hien_thi = self.STATUS_MAPPING.get(trang_thai_db, self.STATUS_MAPPING['ChuaCham'])

                self.view.attendance_tree.insert("", tk.END, values=(
                    rec['MaNguoiDung'],
                    rec['HoTen'],
                    rec['GioVao'] or "",
                    rec['GioRa'] or "",
                    rec['SoGioLam'] or "",
                    trang_thai_hien_thi
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
        # Sử dụng danh sách tiếng Việt cho combobox
        status_options_vn = [v for k, v in self.STATUS_MAPPING.items() if k != 'ChuaCham']
        status_var = tk.StringVar(value=self.STATUS_MAPPING['DiLam'])
        status_combo = ttk.Combobox(
            dialog,
            textvariable=status_var,
            values=status_options_vn,
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
                
                # Chuyển từ hiển thị (Tiếng Việt) về mã CSDL khi lưu
                trang_thai_db = self.INVERSE_STATUS_MAPPING.get(status_var.get(), status_var.get())

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
                        (gio_vao.get(), gio_ra.get(), hours, trang_thai_db, self.view.user_info['MaNguoiDung'], emp_id, selected_date)
                    )
                else:
                    insert_query = """
                        INSERT INTO ChamCong (MaNguoiDung, NgayChamCong, GioVao, GioRa, SoGioLam, TrangThai, NguoiChamCong)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                    result = self.db.execute_query(
                        insert_query,
                        (emp_id, selected_date, gio_vao.get(), gio_ra.get(), hours, trang_thai_db, self.view.user_info['MaNguoiDung'])
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