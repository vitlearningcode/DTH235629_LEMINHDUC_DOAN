# main/Function/function_Admin/admin_promotion_logic.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class AdminPromotionLogic:
    def __init__(self, view):
        self.view = view
        self.db = view.db

    def load_promotions(self):
        """Tải danh sách khuyến mãi lên Treeview"""
        for item in self.view.promo_tree.get_children(): 
            self.view.promo_tree.delete(item)
        
        query = """
            SELECT MaKhuyenMai, TenKhuyenMai, LoaiKhuyenMai, GiaTri,
                   FORMAT(NgayBatDau, 'dd/MM/yyyy') as NgayBatDau,
                   FORMAT(NgayKetThuc, 'dd/MM/yyyy') as NgayKetThuc,
                   TrangThai
            FROM KhuyenMai
            ORDER BY NgayBatDau DESC
        """
        promos = self.db.fetch_all(query)
        for p in promos:
            # Format giá trị
            value = f"{p['GiaTri']:,.0f}%" if p['LoaiKhuyenMai'] == 'PhanTram' else f"{p['GiaTri']:,.0f} VNĐ"
            
            # --- 1. CHUYỂN ĐỔI HIỂN THỊ TRẠNG THÁI (Data -> Tiếng Việt) ---
            trang_thai_vn = "Hoạt động" if p['TrangThai'] == 'HoatDong' else "Không hoạt động"

            self.view.promo_tree.insert("", tk.END, values=(
                p['MaKhuyenMai'], 
                p['TenKhuyenMai'], 
                p['LoaiKhuyenMai'], 
                value, 
                p['NgayBatDau'], 
                p['NgayKetThuc'], 
                trang_thai_vn # Hiển thị tiếng Việt
            ))

    def _show_promo_dialog(self, promo_data=None):
        """Hàm nội bộ: Hiển thị cửa sổ Toplevel cho Thêm hoặc Sửa Khuyến mãi"""
        
        is_edit = promo_data is not None
        
        dialog = tk.Toplevel(self.view.window)
        dialog.title("Thêm Khuyến Mãi Mới" if not is_edit else f"Cập Nhật Khuyến Mãi (ID: {promo_data['MaKhuyenMai']})")
        dialog.resizable(False, False)
        dialog.grab_set()

        container = tk.Frame(dialog, padx=20, pady=20)
        container.pack(fill="none", expand=False)

        entries = {}
        
        # Định nghĩa các trường
        # Lưu ý: Combobox 'TrangThai' dùng Tiếng Việt
        fields = [
            ("Tên Khuyến Mãi:", "TenKhuyenMai", "entry", None),
            ("Loại Khuyến Mãi:", "LoaiKhuyenMai", "combo", ['PhanTram', 'TienMat']),
            ("Giá Trị (VNĐ hoặc %):", "GiaTri", "entry", None),
            ("Ngày Bắt Đầu (YYYY-MM-DD):", "NgayBatDau", "entry", None),
            ("Ngày Kết Thúc (YYYY-MM-DD):", "NgayKetThuc", "entry", None),
            ("Điều Kiện:", "DieuKien", "text", None),
            ("Trạng Thái:", "TrangThai", "combo", ['Hoạt động', 'Không hoạt động']) 
        ]

        # Tạo các widget
        for i, (text, key, widget_type, default) in enumerate(fields):
            tk.Label(container, text=text, font=("Arial", 11)).grid(row=i, column=0, padx=10, pady=10, sticky="e")
            
            if widget_type == "entry":
                val = ""
                if is_edit:
                    val = promo_data.get(key) or ""
                    if key in ["NgayBatDau", "NgayKetThuc"] and val:
                        val = str(val).split(" ")[0]
                elif default:
                    val = default
                    
                entry = tk.Entry(container, font=("Arial", 11), width=40)
                entry.grid(row=i, column=1, padx=10, pady=10)
                entry.insert(0, str(val))
                entries[key] = entry
                
            elif widget_type == "combo":
                val = tk.StringVar()
                if is_edit:
                    db_val = promo_data.get(key)
                    
                    # --- 2. CHUYỂN ĐỔI KHI EDIT (Data -> Tiếng Việt cho Combobox) ---
                    if key == "TrangThai":
                        val.set("Hoạt động" if db_val == 'HoatDong' else "Không hoạt động")
                    else:
                        val.set(db_val)
                        
                elif default:
                    val.set(default[0]) 

                combo = ttk.Combobox(container, textvariable=val, values=default, state="readonly", width=38, font=("Arial", 11))
                combo.grid(row=i, column=1, padx=10, pady=10)
                entries[key] = combo
                
            elif widget_type == "text":
                val = ""
                if is_edit:
                    val = promo_data.get(key) or ""
                
                text_widget = tk.Text(container, font=("Arial", 11), width=40, height=3, relief="solid", borderwidth=1)
                text_widget.grid(row=i, column=1, padx=10, pady=10)
                text_widget.insert("1.0", val)
                entries[key] = text_widget

        def save():
            try:
                # Lấy dữ liệu
                data = {}
                for key, widget in entries.items():
                    if isinstance(widget, tk.Text):
                        data[key] = widget.get("1.0", tk.END).strip() or None
                    else:
                        data[key] = widget.get().strip()
                
                # Xác thực
                if not data['TenKhuyenMai'] or not data['GiaTri'] or not data['NgayBatDau'] or not data['NgayKetThuc']:
                    messagebox.showwarning("Thiếu thông tin", "Tên, Giá Trị, Ngày Bắt Đầu và Ngày Kết Thúc là bắt buộc.", parent=dialog)
                    return
                
                # Chuyển đổi số và kiểm tra ngày
                gia_tri = float(data['GiaTri'])
                ngay_bd = datetime.strptime(data['NgayBatDau'], '%Y-%m-%d').date()
                ngay_kt = datetime.strptime(data['NgayKetThuc'], '%Y-%m-%d').date()

                if ngay_kt < ngay_bd:
                    messagebox.showwarning("Lỗi logic", "Ngày kết thúc không được sớm hơn ngày bắt đầu.", parent=dialog)
                    return

                # --- 3. CHUYỂN ĐỔI TRƯỚC KHI LƯU (Tiếng Việt -> Data) ---
                trang_thai_db = "HoatDong" if data['TrangThai'] == "Hoạt động" else "KhongHoatDong"

                # Chuẩn bị query
                if is_edit:
                    query = """
                        UPDATE KhuyenMai SET 
                        TenKhuyenMai=%s, LoaiKhuyenMai=%s, GiaTri=%s, NgayBatDau=%s, NgayKetThuc=%s,
                        DieuKien=%s, TrangThai=%s
                        WHERE MaKhuyenMai=%s
                    """
                    params = (
                        data['TenKhuyenMai'], data['LoaiKhuyenMai'], gia_tri, ngay_bd, ngay_kt,
                        data['DieuKien'], trang_thai_db, # Dùng biến đã convert
                        promo_data['MaKhuyenMai']
                    )
                else:
                    query = """
                        INSERT INTO KhuyenMai 
                        (TenKhuyenMai, LoaiKhuyenMai, GiaTri, NgayBatDau, NgayKetThuc, DieuKien, TrangThai)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                    params = (
                        data['TenKhuyenMai'], data['LoaiKhuyenMai'], gia_tri, ngay_bd, ngay_kt,
                        data['DieuKien'], trang_thai_db # Dùng biến đã convert
                    )
                
                # Thực thi
                if self.db.execute_query(query, params):
                    messagebox.showinfo("Thành công", "Lưu khuyến mãi thành công!", parent=dialog)
                    dialog.destroy()
                    self.load_promotions()
                else:
                    messagebox.showerror("Lỗi CSDL", "Không thể lưu khuyến mãi.", parent=dialog)
                    
            except ValueError:
                messagebox.showerror("Lỗi nhập liệu", "Giá trị phải là SỐ.\nNgày tháng phải đúng định dạng YYYY-MM-DD.", parent=dialog)
            except Exception as e:
                messagebox.showerror("Lỗi không xác định", f"{e}", parent=dialog)

        btn_text = "💾 Lưu Thay Đổi" if is_edit else "💾 Thêm Khuyến Mãi"
        btn_color = "#007bff" if is_edit else "#28a745"
        
        tk.Button(container, text=btn_text, font=("Arial", 12, "bold"), bg=btn_color, fg="white", command=save, width=20, height=2).grid(row=len(fields), column=0, columnspan=2, pady=20)

    def add_promotion(self):
        self._show_promo_dialog(None)
    
    def edit_promotion(self):
        selected = self.view.promo_tree.selection()
        if not selected:
            messagebox.showwarning("Chú ý", "Vui lòng chọn một khuyến mãi để sửa.")
            return
        
        promo_id = self.view.promo_tree.item(selected[0])['values'][0]
        promo_data = self.db.fetch_one("SELECT * FROM KhuyenMai WHERE MaKhuyenMai = %s", (promo_id,))
        
        if promo_data:
            self._show_promo_dialog(promo_data)
        else:
            messagebox.showerror("Lỗi", "Không tìm thấy dữ liệu khuyến mãi này.")

    def delete_promotion(self):
        selected = self.view.promo_tree.selection()
        if not selected:
            messagebox.showwarning("Chú ý", "Vui lòng chọn một khuyến mãi để xóa.")
            return

        item = self.view.promo_tree.item(selected[0])
        promo_id = item['values'][0]
        promo_name = item['values'][1]

        check_query = "SELECT COUNT(*) as total FROM HoaDon WHERE MaKhuyenMai = %s"
        usage = self.db.fetch_one(check_query, (promo_id,))

        if usage and usage['total'] > 0:
            messagebox.showerror("Lỗi Ràng Buộc", 
                                 f"Không thể xóa khuyến mãi '{promo_name}'.\n"
                                 f"Khuyến mãi này đã được áp dụng cho {usage['total']} hóa đơn.")
            return

        if messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc muốn XÓA VĨNH VIỄN khuyến mãi:\n\n{promo_name} (ID: {promo_id})"):
            try:
                result = self.db.execute_query("DELETE FROM KhuyenMai WHERE MaKhuyenMai = %s", (promo_id,))
                
                if result:
                    messagebox.showinfo("Thành công", f"Đã xóa khuyến mãi '{promo_name}'.")
                    self.load_promotions()
                else:
                    messagebox.showerror("Lỗi", "Xóa thất bại.")
            except Exception as e:
                messagebox.showerror("Lỗi CSDL", f"Không thể xóa: {e}")