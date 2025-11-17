# main/Function/function_NhanVien/nhanvien_service_logic.py

import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from datetime import datetime

class NhanVienServiceLogic:
    def __init__(self, view):
        """Khởi tạo logic cho màn hình dịch vụ/bảo hành"""
        self.view = view
        self.db = view.db
        self.current_customer_id = None

    # --- HÀM MỚI THÊM: Xử lý sự kiện khi nhập phím ---
    def on_service_phone_change(self, event):
        """Tự động tìm kiếm khi nhập đủ 10 số"""
        phone = self.view.service_phone_entry.get().strip()
        
        # Nếu đủ 10 số thì tìm
        if len(phone) == 10 and phone.isdigit():
            self.search_customer_by_phone()
        # Nếu khác 10 số (đang xóa hoặc nhập chưa xong) thì reset thông tin
        elif len(phone) != 10:
            self.current_customer_id = None
            self.view.service_customer_name_var.set("Vui lòng nhập SĐT...")
            # Xóa dữ liệu trên 2 bảng
            for item in self.view.warranty_tree.get_children():
                self.view.warranty_tree.delete(item)
            for item in self.view.history_tree.get_children():
                self.view.history_tree.delete(item)

    def search_customer_by_phone(self):
        """Tìm khách hàng bằng SĐT và tải danh sách bảo hành của họ"""
        phone = self.view.service_phone_entry.get().strip()
        if not phone:
            return # Không làm gì nếu rỗng

        query = "SELECT MaKhachHang, HoTen FROM KhachHang WHERE SoDienThoai = %s"
        customer = self.db.fetch_one(query, (phone,))
        
        # Xóa các cây dữ liệu cũ
        for item in self.view.warranty_tree.get_children():
            self.view.warranty_tree.delete(item)
        for item in self.view.history_tree.get_children():
            self.view.history_tree.delete(item)

        if customer:
            self.current_customer_id = customer['MaKhachHang']
            self.view.service_customer_name_var.set(customer['HoTen'])
            
            # Đã xóa messagebox.showinfo("Thành công"...) để trải nghiệm mượt hơn
            self.load_customer_warranties()
        else:
            self.current_customer_id = None
            self.view.service_customer_name_var.set("Không tìm thấy khách hàng.")
            # Có thể hiện cảnh báo hoặc không, tùy bạn. Ở đây tôi bỏ qua để không ngắt quãng việc nhập liệu.

    def load_customer_warranties(self):
        """Tải các phiếu bảo hành (xe đã mua) của khách hàng"""
        if not self.current_customer_id:
            return
            
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
            ORDER BY pb.NgayKetThuc ASC
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

    # ... (Giữ nguyên các hàm on_warranty_select, load_warranty_history, add_warranty_history_entry ở phía dưới không thay đổi) ...
    def on_warranty_select(self, event=None):
        try:
            selected = self.view.warranty_tree.selection()
            if not selected: return
            item = self.view.warranty_tree.item(selected[0])
            warranty_id = item['values'][0]
            if not warranty_id: return
            self.load_warranty_history(warranty_id)
        except Exception: pass

    def load_warranty_history(self, warranty_id):
        query = """
            SELECT FORMAT(ls.NgaySuaChua, 'dd/MM/yyyy') as NgaySuaChua, ls.MoTaLoi, 
                nd.HoTen AS NguoiXuLy, ls.ChiPhiPhatSinh, ls.TrangThai
            FROM LichSuBaoHanh ls
            JOIN NguoiDung nd ON ls.NguoiXuLy = nd.MaNguoiDung
            WHERE ls.MaPhieuBaoHanh = %s
            ORDER BY ls.NgaySuaChua ASC
        """
        records = self.db.fetch_all(query, (warranty_id,))
        for item in self.view.history_tree.get_children():
            self.view.history_tree.delete(item)
        if records:
            for rec in records:
                self.view.history_tree.insert("", tk.END, values=(
                    rec['NgaySuaChua'], rec['MoTaLoi'], rec['NguoiXuLy'],
                    f"{rec['ChiPhiPhatSinh']:,.0f} VNĐ", rec['TrangThai']
                ))
        else:
            self.view.history_tree.insert("", tk.END, values=("", "Phiếu này chưa có lịch sử sửa chữa.", "", "", ""))

    def add_warranty_history_entry(self):
        # (Giữ nguyên code hàm này như cũ)
        selected = self.view.warranty_tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một Phiếu Bảo Hành trước.")
            return
        item = self.view.warranty_tree.item(selected[0])
        warranty_id = item['values'][0]
        product_name = item['values'][1]
        if not warranty_id: return

        dialog = tk.Toplevel(self.view.window)
        dialog.title("Thêm Lịch Sử Sửa Chữa")
        dialog.geometry("450x400")
        
        tk.Label(dialog, text=f"Lập phiếu cho xe: {product_name}", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(dialog, text="Mô tả lỗi/dịch vụ (*):").pack()
        desc_entry = tk.Text(dialog, height=5, width=50); desc_entry.pack()
        tk.Label(dialog, text="Chi phí phát sinh:").pack()
        cost_entry = tk.Entry(dialog); cost_entry.insert(0, "0"); cost_entry.pack()
        tk.Label(dialog, text="Trạng thái:").pack()
        status_combo = ttk.Combobox(dialog, values=["DangXuLy", "HoanThanh"]); status_combo.set("HoanThanh"); status_combo.pack()

        def save():
            desc = desc_entry.get("1.0", tk.END).strip()
            try: cost = float(cost_entry.get())
            except: messagebox.showerror("Lỗi", "Chi phí phải là số"); return
            if not desc: messagebox.showwarning("Thiếu", "Nhập mô tả"); return
            
            self.db.execute_query("INSERT INTO LichSuBaoHanh (MaPhieuBaoHanh, NgaySuaChua, MoTaLoi, ChiPhiPhatSinh, NguoiXuLy, TrangThai) VALUES (%s, GETDATE(), %s, %s, %s, %s)", 
                                  (warranty_id, desc, cost, self.view.user_info['MaNguoiDung'], status_combo.get()))
            messagebox.showinfo("OK", "Đã lưu!"); dialog.destroy(); self.load_warranty_history(warranty_id)
            
        tk.Button(dialog, text="Lưu", command=save, bg="#28a745", fg="white").pack(pady=20)