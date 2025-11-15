# Mở file mới: main/Function/function_NhanVien/nhanvien_service_logic.py

import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from datetime import datetime

class NhanVienServiceLogic:
    def __init__(self, view):
        """Khởi tạo logic cho màn hình dịch vụ/bảo hành"""
        self.view = view
        self.db = view.db
        self.current_customer_id = None

    def search_customer_by_phone(self):
        """Tìm khách hàng bằng SĐT và tải danh sách bảo hành của họ"""
        phone = self.view.service_phone_entry.get().strip()
        if not phone:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập số điện thoại!")
            return

        query = "SELECT MaKhachHang, HoTen FROM KhachHang WHERE SoDienThoai = %s"
        customer = self.db.fetch_one(query, (phone,))
        
        # Xóa các cây
        for item in self.view.warranty_tree.get_children():
            self.view.warranty_tree.delete(item)
        for item in self.view.history_tree.get_children():
            self.view.history_tree.delete(item)

        if customer:
            self.current_customer_id = customer['MaKhachHang']
            self.view.service_customer_name_var.set(customer['HoTen'])
            messagebox.showinfo("Thành công", f"Tìm thấy khách hàng: {customer['HoTen']}.\nĐang tải danh sách bảo hành...")
            self.load_customer_warranties()
        else:
            self.current_customer_id = None
            self.view.service_customer_name_var.set("Không tìm thấy khách hàng này.")
            messagebox.showwarning("Không tìm thấy", "Không tìm thấy khách hàng với SĐT này.")

    def load_customer_warranties(self):
        """Tải các phiếu bảo hành (xe đã mua) của khách hàng"""
        if not self.current_customer_id:
            return
            
        #
        query = """
            SELECT 
                pb.MaPhieuBaoHanh, 
                sp.TenSanPham, 
                FORMAT(pb.NgayBatDau, 'dd/MM/yyyy') as NgayBatDau, 
                FORMAT(pb.NgayKetThuc, 'dd/MM/yyyy') as NgayKetThuc,
                pb.TrangThai
            FROM PhieuBaoHanh pb
            JOIN SanPham sp ON pb.MaSanPham = sp.MaSanPham
            WHERE pb.MaKhachHang = %s
            ORDER BY pb.NgayKetThuc DESC
        """
        records = self.db.fetch_all(query, (self.current_customer_id,))
        
        for item in self.view.warranty_tree.get_children():
            self.view.warranty_tree.delete(item)
            
        if records:
            for rec in records:
                self.view.warranty_tree.insert("", tk.END, values=(
                    rec['MaPhieuBaoHanh'],
                    rec['TenSanPham'],
                    rec['NgayBatDau'],
                    rec['NgayKetThuc'],
                    rec['TrangThai']
                ))
        else:
            self.view.warranty_tree.insert("", tk.END, values=("", "Khách hàng này chưa có phiếu bảo hành nào.", "", "", ""))

    def on_warranty_select(self, event=None):
        """Khi nhân viên click vào một phiếu bảo hành, tải lịch sử của phiếu đó"""
        try:
            selected = self.view.warranty_tree.selection()
            if not selected:
                return
            
            item = self.view.warranty_tree.item(selected[0])
            warranty_id = item['values'][0]
            if not warranty_id: # Xử lý trường hợp "Không tìm thấy"
                return

            self.load_warranty_history(warranty_id)
        except Exception as e:
            pass # Bỏ qua lỗi khi click linh tinh

    def load_warranty_history(self, warranty_id):
        """Tải lịch sử sửa chữa của một phiếu bảo hành cụ thể"""
        #
        query = """
            SELECT 
                FORMAT(ls.NgaySuaChua, 'dd/MM/yyyy') as NgaySuaChua, 
                ls.MoTaLoi, 
                nd.HoTen AS NguoiXuLy, 
                ls.ChiPhiPhatSinh,
                ls.TrangThai
            FROM LichSuBaoHanh ls
            JOIN NguoiDung nd ON ls.NguoiXuLy = nd.MaNguoiDung
            WHERE ls.MaPhieuBaoHanh = %s
            ORDER BY ls.NgaySuaChua DESC
        """
        records = self.db.fetch_all(query, (warranty_id,))
        
        for item in self.view.history_tree.get_children():
            self.view.history_tree.delete(item)
            
        if records:
            for rec in records:
                self.view.history_tree.insert("", tk.END, values=(
                    rec['NgaySuaChua'],
                    rec['MoTaLoi'],
                    rec['NguoiXuLy'],
                    f"{rec['ChiPhiPhatSinh']:,.0f} VNĐ",
                    rec['TrangThai']
                ))
        else:
            self.view.history_tree.insert("", tk.END, values=("", "Phiếu này chưa có lịch sử sửa chữa.", "", "", ""))

    def add_warranty_history_entry(self):
        """Mở popup để Thêm Lịch Sử Sửa Chữa Mới"""
        selected = self.view.warranty_tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một Phiếu Bảo Hành (ở bảng bên trái) trước.")
            return

        item = self.view.warranty_tree.item(selected[0])
        warranty_id = item['values'][0]
        product_name = item['values'][1]
        
        if not warranty_id:
            return

        # Tạo cửa sổ Toplevel
        dialog = tk.Toplevel(self.view.window)
        dialog.title("Thêm Lịch Sử Sửa Chữa")
        dialog.geometry("450x400")
        dialog.resizable(False, False)
        dialog.grab_set()

        tk.Label(dialog, text=f"Lập phiếu cho xe: {product_name}", font=("Arial", 12, "bold")).pack(pady=10)

        tk.Label(dialog, text="Mô tả lỗi hoặc dịch vụ (*):", font=("Arial", 11)).pack(pady=(10,0))
        desc_entry = tk.Text(dialog, font=("Arial", 11), width=50, height=5, relief="solid", borderwidth=1)
        desc_entry.pack(pady=5, padx=10)

        tk.Label(dialog, text="Chi phí phát sinh (nếu có):", font=("Arial", 11)).pack(pady=(10,0))
        cost_entry = tk.Entry(dialog, font=("Arial", 11), width=30)
        cost_entry.insert(0, "0")
        cost_entry.pack(pady=5)
        
        tk.Label(dialog, text="Trạng thái:", font=("Arial", 11)).pack(pady=(10,0))
        status_var = tk.StringVar(value="HoanThanh")
        status_combo = ttk.Combobox(
            dialog, textvariable=status_var, 
            values=["DangXuLy", "HoanThanh"], 
            state="readonly", font=("Arial", 11), width=28
        )
        status_combo.pack(pady=5)

        def save_history():
            description = desc_entry.get("1.0", tk.END).strip()
            cost_str = cost_entry.get().strip()
            status = status_var.get()
            
            if not description:
                messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập Mô tả lỗi.", parent=dialog)
                return

            try:
                cost = float(cost_str)
            except ValueError:
                messagebox.showerror("Lỗi", "Chi phí phát sinh phải là một con số.", parent=dialog)
                return

            try:
                #
                query = """
                    INSERT INTO LichSuBaoHanh 
                    (MaPhieuBaoHanh, NgaySuaChua, MoTaLoi, ChiPhiPhatSinh, NguoiXuLy, TrangThai)
                    VALUES (%s, GETDATE(), %s, %s, %s, %s)
                """
                params = (
                    warranty_id, 
                    description, 
                    cost, 
                    self.view.user_info['MaNguoiDung'], # ID của nhân viên đang đăng nhập
                    status
                )
                
                result = self.db.execute_query(query, params)
                
                if result:
                    messagebox.showinfo("Thành công", "Đã thêm lịch sử sửa chữa thành công!", parent=dialog)
                    dialog.destroy()
                    self.load_warranty_history(warranty_id) # Tải lại bảng lịch sử
                else:
                    messagebox.showerror("Lỗi", "Không thể lưu lịch sử sửa chữa.", parent=dialog)
            except Exception as e:
                messagebox.showerror("Lỗi CSDL", f"Đã xảy ra lỗi: {e}", parent=dialog)

        tk.Button(
            dialog, text="💾 Lưu Lịch Sử", 
            font=("Arial", 12, "bold"), bg="#28a745", fg="white", 
            command=save_history
        ).pack(pady=20)