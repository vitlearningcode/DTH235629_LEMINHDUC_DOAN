import tkinter as tk
from tkinter import messagebox, ttk, Toplevel, Label, Entry, Button
from datetime import datetime  # Thêm thư viện xử lý ngày tháng

class AdminWarrantyLogic:
    def __init__(self, view):
        """Khởi tạo logic cho màn hình Quản lý Bảo hành (Admin)"""
        self.view = view
        self.db = view.db

    def load_all_warranties(self, keyword=None):
        """Tải TẤT CẢ các phiếu bảo hành, tính toán trạng thái Hiệu lực"""
        
        # Xóa dữ liệu cũ trên bảng
        for item in self.view.warranty_tree.get_children():
            self.view.warranty_tree.delete(item)
        
        # Query lấy dữ liệu (bỏ cột TrangThai gốc, ta sẽ tự tính toán)
        query = """
            SELECT TOP 200
                pb.MaPhieuBaoHanh, 
                kh.HoTen AS TenKhachHang,
                kh.SoDienThoai,
                sp.TenSanPham, 
                FORMAT(pb.NgayBatDau, 'dd/MM/yyyy') as NgayBatDau, 
                FORMAT(pb.NgayKetThuc, 'dd/MM/yyyy') as NgayKetThuc
            FROM PhieuBaoHanh pb
            JOIN SanPham sp ON pb.MaSanPham = sp.MaSanPham
            JOIN KhachHang kh ON pb.MaKhachHang = kh.MaKhachHang
        """
        params = []
        
        if keyword:
            query += " WHERE kh.HoTen LIKE %s OR kh.SoDienThoai LIKE %s OR sp.TenSanPham LIKE %s"
            params.extend([f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"])
            
        query += " ORDER BY pb.MaPhieuBaoHanh ASC"
        
        try:
            records = self.db.fetch_all(query, params)
            if records:
                today = datetime.now() # Lấy thời gian hiện tại
                
                for rec in records:
                    # Logic tính toán trạng thái: So sánh ngày kết thúc với hôm nay
                    try:
                        # Chuyển chuỗi ngày về đối tượng datetime để so sánh
                        end_date_obj = datetime.strptime(rec['NgayKetThuc'], '%d/%m/%Y')
                        
                        # Nếu ngày kết thúc >= hôm nay -> Còn hiệu lực
                        # (Dùng date() để chỉ so sánh ngày, bỏ qua giờ phút giây)
                        if end_date_obj.date() >= today.date():
                            status_display = "Còn hiệu lực"
                        else:
                            status_display = "Hết hiệu lực"
                    except Exception:
                        status_display = "Lỗi ngày tháng"

                    self.view.warranty_tree.insert("", tk.END, values=(
                        rec['MaPhieuBaoHanh'],
                        rec['TenKhachHang'],
                        rec['SoDienThoai'],
                        rec['TenSanPham'],
                        rec['NgayBatDau'],
                        rec['NgayKetThuc'],
                        status_display # Hiển thị trạng thái đã tính
                    ))
            else:
                self.view.warranty_tree.insert("", tk.END, values=("", "Không tìm thấy phiếu.", "", "", "", "", ""))
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Không thể tải danh sách bảo hành: {e}")

    def on_warranty_select(self, event=None):
        """Khi Admin click vào một phiếu bảo hành, tải lịch sử của phiếu đó"""
        for item in self.view.history_tree.get_children():
            self.view.history_tree.delete(item)
            
        try:
            selected = self.view.warranty_tree.selection()
            if not selected:
                return
            
            item = self.view.warranty_tree.item(selected[0])
            warranty_id = item['values'][0]
            if not warranty_id:
                return

            self.load_warranty_history(warranty_id)
        except Exception as e:
            pass 

    def load_warranty_history(self, warranty_id):
        """Tải lịch sử sửa chữa của một phiếu bảo hành cụ thể"""
        query = """
            SELECT 
                ls.MaLichSu,
                FORMAT(ls.NgaySuaChua, 'dd/MM/yyyy') as NgaySuaChua, 
                ls.MoTaLoi, 
                nd.HoTen AS NguoiXuLy, 
                ls.ChiPhiPhatSinh,
                ls.TrangThai
            FROM LichSuBaoHanh ls
            LEFT JOIN NguoiDung nd ON ls.NguoiXuLy = nd.MaNguoiDung
            WHERE ls.MaPhieuBaoHanh = %s
            ORDER BY ls.NgaySuaChua DESC
        """
        records = self.db.fetch_all(query, (warranty_id,))
        
        if records:
            for rec in records:
                self.view.history_tree.insert("", tk.END, values=(
                    rec['MaLichSu'],
                    rec['NgaySuaChua'],
                    rec['MoTaLoi'],
                    rec['NguoiXuLy'] or "Không rõ",
                    f"{rec['ChiPhiPhatSinh']:,.0f} VNĐ",
                    rec['TrangThai']
                ))
        else:
            self.view.history_tree.insert("", tk.END, values=("", "Phiếu này chưa có lịch sử sửa chữa.", "", "", "", ""))

    # --- CHỨC NĂNG MỚI: SỬA PHIẾU BẢO HÀNH ---
    def edit_warranty(self):
        """Mở cửa sổ chỉnh sửa ngày bảo hành"""
        selected = self.view.warranty_tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một 'Phiếu Bảo Hành' (bên trái) để sửa.")
            return

        item = self.view.warranty_tree.item(selected[0])
        values = item['values']
        
        # Lấy dữ liệu hiện tại từ dòng đã chọn
        # values[0]: ID, values[4]: NgayBatDau, values[5]: NgayKetThuc
        w_id = values[0]
        if not w_id: return
        
        current_start = values[4]
        current_end = values[5]

        # Tạo cửa sổ Popup (Toplevel)
        self.edit_window = Toplevel(self.view.window)
        self.edit_window.title(f"Sửa Bảo Hành - ID: {w_id}")
        self.edit_window.geometry("400x280")
        
        # UI trong Popup
        Label(self.edit_window, text=f"Cập nhật phiếu: {w_id}", font=("Arial", 12, "bold")).pack(pady=10)

        Label(self.edit_window, text="Ngày Bắt Đầu (dd/mm/yyyy):", font=("Arial", 10)).pack(pady=5)
        entry_start = Entry(self.edit_window, font=("Arial", 12), justify="center")
        entry_start.insert(0, current_start)
        entry_start.pack(pady=5)

        Label(self.edit_window, text="Ngày Kết Thúc (dd/mm/yyyy):", font=("Arial", 10)).pack(pady=5)
        entry_end = Entry(self.edit_window, font=("Arial", 12), justify="center")
        entry_end.insert(0, current_end)
        entry_end.pack(pady=5)
        
        Label(self.edit_window, text="(Lưu ý: Nhập đúng định dạng ngày)", font=("Arial", 9, "italic"), fg="grey").pack(pady=5)

        # Nút Lưu
        Button(self.edit_window, text="Lưu Thay Đổi", bg="#007bff", fg="white", font=("Arial", 10, "bold"),
               command=lambda: self.save_edited_warranty(w_id, entry_start.get(), entry_end.get())).pack(pady=15)

    def save_edited_warranty(self, w_id, start_str, end_str):
        """Lưu thông tin đã sửa vào CSDL"""
        try:
            # Chuyển đổi định dạng từ dd/mm/yyyy (User nhập) sang YYYY-MM-DD (SQL cần)
            d_start = datetime.strptime(start_str, '%d/%m/%Y').strftime('%Y-%m-%d')
            d_end = datetime.strptime(end_str, '%d/%m/%Y').strftime('%Y-%m-%d')
            
            # Thực hiện Update
            query = "UPDATE PhieuBaoHanh SET NgayBatDau = %s, NgayKetThuc = %s WHERE MaPhieuBaoHanh = %s"
            result = self.db.execute_query(query, (d_start, d_end, w_id))
            
            if result:
                messagebox.showinfo("Thành công", "Đã cập nhật thời gian bảo hành.")
                self.edit_window.destroy() # Đóng popup
                self.load_all_warranties() # Tải lại danh sách để cập nhật trạng thái
            else:
                messagebox.showerror("Lỗi", "Cập nhật thất bại.")
            
        except ValueError:
            messagebox.showerror("Lỗi định dạng", "Vui lòng nhập ngày đúng định dạng: dd/mm/yyyy (Ví dụ: 17/11/2025)")
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Không thể cập nhật: {e}")

    def delete_history_entry(self):
        """Xóa một mục LỊCH SỬ SỬA CHỮA"""
        selected = self.view.history_tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một mục trong bảng 'Lịch Sử Sửa Chữa' (bên phải) để xóa.")
            return

        item = self.view.history_tree.item(selected[0])
        history_id = item['values'][0]
        history_desc = item['values'][2]
        
        if not history_id: return

        if messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc muốn XÓA mục lịch sử:\n\n'{history_desc}' (ID: {history_id})"):
            try:
                query = "DELETE FROM LichSuBaoHanh WHERE MaLichSu = %s"
                result = self.db.execute_query(query, (history_id,))
                
                if result:
                    messagebox.showinfo("Thành công", "Đã xóa mục lịch sử sửa chữa.")
                    self.on_warranty_select() # Tải lại lịch sử
                else:
                    messagebox.showerror("Lỗi", "Xóa thất bại.")
            except Exception as e:
                messagebox.showerror("Lỗi CSDL", f"Không thể xóa: {e}")

    def delete_warranty_entry(self):
        """Xóa toàn bộ PHIẾU BẢO HÀNH (và các lịch sử liên quan)"""
        selected = self.view.warranty_tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một 'Phiếu Bảo Hành' (bên trái) để xóa.")
            return

        item = self.view.warranty_tree.item(selected[0])
        warranty_id = item['values'][0]
        warranty_desc = item['values'][3] # Tên xe
        
        if not warranty_id: return

        if messagebox.askyesno("Xác nhận xóa", 
            f"BẠN CÓ CHẮC MUỐN XÓA TOÀN BỘ PHIẾU BẢO HÀNH?\n\n"
            f"Xe: {warranty_desc} (ID Phiếu: {warranty_id})\n\n"
            f"CẢNH BÁO: Toàn bộ lịch sử sửa chữa liên quan đến phiếu này cũng sẽ bị XÓA VĨNH VIỄN.",
            icon='warning'):
            
            try:
                # Phải xóa lịch sử trước do ràng buộc khóa ngoại
                query_history = "DELETE FROM LichSuBaoHanh WHERE MaPhieuBaoHanh = %s"
                self.db.execute_query(query_history, (warranty_id,))
                
                # Xóa phiếu bảo hành
                query_warranty = "DELETE FROM PhieuBaoHanh WHERE MaPhieuBaoHanh = %s"
                result = self.db.execute_query(query_warranty, (warranty_id,))

                if result:
                    messagebox.showinfo("Thành công", "Đã xóa toàn bộ phiếu bảo hành và lịch sử liên quan.")
                    self.load_all_warranties() 
                    # Xóa cây lịch sử
                    for item in self.view.history_tree.get_children():
                        self.view.history_tree.delete(item)
                else:
                    messagebox.showerror("Lỗi", "Xóa thất bại (bước xóa Phiếu Bảo Hành).")
            except Exception as e:
                messagebox.showerror("Lỗi CSDL", f"Không thể xóa: {e}")