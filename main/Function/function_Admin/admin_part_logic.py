# main/Function/function_Admin/admin_part_logic.py

import tkinter as tk
from tkinter import messagebox, ttk

class AdminPartLogic:
    def __init__(self, view):
        self.view = view
        self.db = view.db
        
        # Biến đệm để lưu trữ loại phụ tùng
        self.part_types = {} # { 'Nhớt': 1, ... }
        self.part_types_inv = {} # { 1: 'Nhớt', ... }

    def load_parts(self):
        """Tải danh sách phụ tùng lên treeview"""
        for item in self.view.part_tree.get_children(): 
            self.view.part_tree.delete(item)
        query = """
            SELECT pt.MaPhuTung, pt.TenPhuTung, lpt.TenLoaiPhuTung, pt.DonViTinh, 
                   pt.GiaNhap, pt.GiaBan, pt.SoLuongTon, pt.TrangThai
            FROM PhuTung pt
            LEFT JOIN LoaiPhuTung lpt ON pt.MaLoaiPhuTung = lpt.MaLoaiPhuTung
            ORDER BY pt.MaPhuTung
        """
        parts = self.db.fetch_all(query)
        if parts:
            for p in parts:
                self.view.part_tree.insert("", tk.END, values=(
                    p['MaPhuTung'], 
                    p['TenPhuTung'], 
                    p['TenLoaiPhuTung'] or "N/A", 
                    p['DonViTinh'], 
                    f"{p['GiaNhap']:,.0f}", 
                    f"{p['GiaBan']:,.0f}", 
                    p['SoLuongTon'],
                    p['TrangThai'] or "ConHang"
                ))

    def _load_part_types(self):
        """Hàm nội bộ: Tải dữ liệu LoaiPhuTung cho Combobox"""
        try:
            # Tải LoaiPhuTung
            types = self.db.fetch_all("SELECT MaLoaiPhuTung, TenLoaiPhuTung FROM LoaiPhuTung")
            self.part_types = {t['TenLoaiPhuTung']: t['MaLoaiPhuTung'] for t in types}
            self.part_types_inv = {t['MaLoaiPhuTung']: t['TenLoaiPhuTung'] for t in types}
            return True
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Không thể tải danh sách loại phụ tùng: {e}")
            return False

    def _show_part_dialog(self, part_data=None):
        """Hàm nội bộ: Hiển thị cửa sổ Toplevel cho Thêm hoặc Sửa Phụ tùng"""
        
        if not self._load_part_types():
            return # Dừng nếu không tải được

        is_edit = part_data is not None
        
        dialog = tk.Toplevel(self.view.window)
        dialog.title("Thêm Phụ Tùng Mới" if not is_edit else f"Cập Nhật Phụ Tùng (ID: {part_data['MaPhuTung']})")
        dialog.resizable(False, False)
        dialog.grab_set()

        container = tk.Frame(dialog, padx=20, pady=20)
        container.pack(fill="none", expand=False)

        entries = {}
        
        # Định nghĩa các trường
        fields = [
            ("Tên Phụ Tùng:", "TenPhuTung", "entry", None),
            ("Loại Phụ Tùng:", "MaLoaiPhuTung", "combo", list(self.part_types.keys())),
            ("Đơn Vị Tính:", "DonViTinh", "entry", "Cái"),
            ("Giá Nhập:", "GiaNhap", "entry", None),
            ("Giá Bán:", "GiaBan", "entry", None),
            ("Số Lượng Tồn:", "SoLuongTon", "entry", 0),
            ("Trạng Thái:", "TrangThai", "combo", ['ConHang', 'HetHang', 'NgungKinhDoanh']),
            ("Mô Tả:", "MoTa", "text", None)
        ]

        # Tạo các widget
        for i, (text, key, widget_type, default) in enumerate(fields):
            tk.Label(container, text=text, font=("Arial", 11)).grid(row=i, column=0, padx=10, pady=10, sticky="e")
            
            if widget_type == "entry":
                val = ""
                if is_edit:
                    val = part_data.get(key) or ""
                elif default:
                    val = default
                    
                entry = tk.Entry(container, font=("Arial", 11), width=40)
                entry.grid(row=i, column=1, padx=10, pady=10)
                entry.insert(0, str(val))
                entries[key] = entry
                
            elif widget_type == "combo":
                val = tk.StringVar()
                if is_edit:
                    if key == "MaLoaiPhuTung":
                        val.set(self.part_types_inv.get(part_data.get(key), ""))
                    elif key == "TrangThai":
                        val.set(part_data.get(key))
                elif key == "TrangThai":
                    val.set(default[0]) # 'ConHang'
                
                combo = ttk.Combobox(container, textvariable=val, values=default, state="readonly", width=38, font=("Arial", 11))
                combo.grid(row=i, column=1, padx=10, pady=10)
                entries[key] = combo
                
            elif widget_type == "text":
                val = ""
                if is_edit:
                    val = part_data.get(key) or ""
                
                text_widget = tk.Text(container, font=("Arial", 11), width=40, height=4, relief="solid", borderwidth=1)
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
                if not data['TenPhuTung'] or not data['GiaNhap'] or not data['GiaBan'] or not data['SoLuongTon']:
                    messagebox.showwarning("Thiếu thông tin", "Tên, Giá Nhập, Giá Bán, và Số Lượng Tồn là bắt buộc.", parent=dialog)
                    return
                
                # Chuyển đổi giá trị Combobox từ Tên về ID
                ma_loai_phu_tung = self.part_types.get(data['MaLoaiPhuTung'])
                
                # Chuyển đổi số
                gia_nhap = float(data['GiaNhap'])
                gia_ban = float(data['GiaBan'])
                so_luong_ton = int(data['SoLuongTon'])

                # Chuẩn bị query
                if is_edit:
                    query = """
                        UPDATE PhuTung SET 
                        TenPhuTung=%s, MaLoaiPhuTung=%s, DonViTinh=%s, GiaNhap=%s, GiaBan=%s, 
                        SoLuongTon=%s, MoTa=%s, TrangThai=%s, NgayCapNhat=GETDATE()
                        WHERE MaPhuTung=%s
                    """
                    params = (
                        data['TenPhuTung'], ma_loai_phu_tung, data['DonViTinh'], gia_nhap, gia_ban,
                        so_luong_ton, data['MoTa'], data['TrangThai'],
                        part_data['MaPhuTung'] # ID cho WHERE
                    )
                else:
                    query = """
                        INSERT INTO PhuTung 
                        (TenPhuTung, MaLoaiPhuTung, DonViTinh, GiaNhap, GiaBan, SoLuongTon, MoTa, TrangThai)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    params = (
                        data['TenPhuTung'], ma_loai_phu_tung, data['DonViTinh'], gia_nhap, gia_ban,
                        so_luong_ton, data['MoTa'], data['TrangThai']
                    )
                
                # Thực thi
                if self.db.execute_query(query, params):
                    messagebox.showinfo("Thành công", "Lưu phụ tùng thành công!", parent=dialog)
                    dialog.destroy()
                    self.load_parts()
                else:
                    messagebox.showerror("Lỗi CSDL", "Không thể lưu phụ tùng.", parent=dialog)
                    
            except ValueError:
                messagebox.showerror("Lỗi nhập liệu", "Giá Nhập, Giá Bán, Số Lượng Tồn phải là SỐ.", parent=dialog)
            except Exception as e:
                messagebox.showerror("Lỗi không xác định", f"{e}", parent=dialog)

        btn_text = "💾 Lưu Thay Đổi" if is_edit else "💾 Thêm Phụ Tùng"
        btn_color = "#007bff" if is_edit else "#28a745"
        
        tk.Button(container, text=btn_text, font=("Arial", 12, "bold"), bg=btn_color, fg="white", command=save, width=20, height=2).grid(row=len(fields), column=0, columnspan=2, pady=20)

    # --- CHỨC NĂNG THÊM MỚI ---
    def add_part(self): 
        self._show_part_dialog(None)
    
    # --- CHỨC NĂNG SỬA ---
    def edit_part(self): 
        selected = self.view.part_tree.selection()
        if not selected:
            messagebox.showwarning("Chú ý", "Vui lòng chọn một phụ tùng để sửa.")
            return
        
        pt_id = self.view.part_tree.item(selected[0])['values'][0]
        
        # Lấy dữ liệu GỐC từ CSDL
        part_data = self.db.fetch_one("SELECT * FROM PhuTung WHERE MaPhuTung = %s", (pt_id,))
        
        if part_data:
            self._show_part_dialog(part_data)
        else:
            messagebox.showerror("Lỗi", "Không tìm thấy dữ liệu phụ tùng này.")

    # --- CHỨC NĂNG XÓA ---
    def delete_part(self): 
        selected = self.view.part_tree.selection()
        if not selected:
            messagebox.showwarning("Chú ý", "Vui lòng chọn một phụ tùng để xóa.")
            return

        item = self.view.part_tree.item(selected[0])
        pt_id = item['values'][0]
        pt_name = item['values'][1]

        if messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc muốn XÓA VĨNH VIỄN phụ tùng:\n\n{pt_name} (ID: {pt_id})\n\nLưu ý: Hành động này sẽ thất bại nếu phụ tùng đã tồn tại trong hóa đơn hoặc phiếu nhập kho."):
            try:
                result = self.db.execute_query("DELETE FROM PhuTung WHERE MaPhuTung = %s", (pt_id,))
                
                if result:
                    messagebox.showinfo("Thành công", f"Đã xóa phụ tùng '{pt_name}'.")
                    self.load_parts()
                else:
                    messagebox.showerror("Lỗi", "Xóa thất bại.")
            except Exception as e:
                messagebox.showerror("Lỗi CSDL (Ràng buộc khóa ngoại)", 
                                     f"Không thể xóa phụ tùng: {e}\n\n"
                                     "Điều này thường xảy ra do phụ tùng đã được liên kết với một Hóa Đơn hoặc Phiếu Nhập Kho.")