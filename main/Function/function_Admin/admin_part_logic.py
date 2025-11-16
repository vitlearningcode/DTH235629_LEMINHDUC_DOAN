# main/Function/function_Admin/admin_part_logic.py
# PHIÊN BẢN NÂNG CẤP: Kết hợp logic CRUD của Admin và logic Panel của QuanLy

import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from PIL import Image, ImageTk
import os

class AdminPartLogic:
    def __init__(self, view):
        self.view = view
        self.db = view.db
        
        # Đường dẫn thư mục tài nguyên
        self.resource_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "..", "..", "resource", "PhuTung"
        ))
        if not os.path.exists(self.resource_path):
            os.makedirs(self.resource_path)
            
        # Biến đệm (Lấy từ logic của QuanLy)
        self.original_data = {}
        self.new_image_path = None

        # Biến đệm (Lấy từ logic gốc của Admin, dùng cho popup Thêm)
        self.part_types = {} 
        self.part_types_inv = {}
        
        # Tải dữ liệu cho combobox (cả panel và popup)
        self._load_part_types()
        
        # Cập nhật combobox trên panel (nếu chúng đã được vẽ)
        try:
            self.view.details_loai.config(values=list(self.part_types.keys()))
        except:
            pass # Lỗi nếu UI chưa được vẽ

    def load_parts(self, tree, keyword=None):
        """Tải danh sách phụ tùng (Logic từ QuanLy, đổi tên load_view)"""
        for item in tree.get_children(): 
            tree.delete(item)
            
        query = """
            SELECT pt.MaPhuTung, pt.TenPhuTung, lpt.TenLoaiPhuTung, pt.GiaBan, pt.SoLuongTon
            FROM PhuTung pt
            LEFT JOIN LoaiPhuTung lpt ON pt.MaLoaiPhuTung = lpt.MaLoaiPhuTung
        """
        params = []
        if keyword:
            query += " WHERE pt.TenPhuTung LIKE %s"
            params.append(f"%{keyword}%")
            
        query += " ORDER BY pt.MaPhuTung"
        
        parts = self.db.fetch_all(query, params)
        if parts:
            for p in parts:
                tree.insert("", tk.END, values=(
                    p['MaPhuTung'], 
                    p['TenPhuTung'], 
                    p['TenLoaiPhuTung'] or "N/A", 
                    f"{p['GiaBan']:,.0f} VNĐ", # Format tiền
                    p['SoLuongTon']
                ))

    # --- CÁC HÀM LOGIC CHO PANEL (LẤY TỪ QUANLY_PART_VIEW_LOGIC) ---

    def on_part_select(self, event):
        """Khi click vào phụ tùng, hiển thị chi tiết lên panel"""
        try:
            selected_item = self.view.part_tree.selection()[0]
            values = self.view.part_tree.item(selected_item, 'values')
            if not values: return
            
            part_id = values[0]
            data = self.db.fetch_one("SELECT * FROM PhuTung WHERE MaPhuTung = %s", (part_id,))
            if not data:
                messagebox.showerror("Lỗi", "Không tìm thấy phụ tùng.")
                return
                
            self.original_data = data
            self.new_image_path = None
            
            self.load_part_image(part_id)
            self.view.details_part_id.config(text=f"Mã: {data['MaPhuTung']}")
            self.view.details_name.delete(0, tk.END)
            self.view.details_name.insert(0, data['TenPhuTung'])
            self.view.details_price.delete(0, tk.END)
            self.view.details_price.insert(0, str(data['GiaBan'] or 0))
            self.view.details_stock.delete(0, tk.END)
            self.view.details_stock.insert(0, str(data['SoLuongTon'] or 0))
            
            self.view.details_loai.set(self.part_types_inv.get(data['MaLoaiPhuTung'], ""))
            
            self.view.update_button.config(state="disabled")
        except IndexError:
            pass
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải chi tiết: {e}")

    def load_part_image(self, part_id, image_path=None):
        """Tải ảnh cho panel"""
        try:
            if image_path is None:
                image_path = os.path.join(self.resource_path, f"{part_id}.png")
            if not os.path.exists(image_path):
                image_path = os.path.join(self.resource_path, "default_part.png")
            if not os.path.exists(image_path):
                img = Image.new('RGB', (150, 150), color='grey')
                img.save(image_path)
                
            img = Image.open(image_path)
            img = img.resize((150, 150), Image.Resampling.LANCZOS)
            self.view.part_photo = ImageTk.PhotoImage(img)
            self.view.part_image_label.config(image=self.view.part_photo)
        except Exception as e:
            print(f"Lỗi tải ảnh phụ tùng: {e}")

    def upload_image(self):
        """Tải ảnh lên cho panel"""
        try:
            file_path = filedialog.askopenfilename(
                title="Chọn ảnh phụ tùng",
                filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif")]
            )
            if not file_path: return
            
            self.new_image_path = file_path
            self.load_part_image(None, image_path=file_path)
            self.check_for_changes()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở ảnh: {e}")

    def check_for_changes(self, event=None):
        """Kiểm tra thay đổi trên panel để bật/tắt nút Cập Nhật"""
        if not self.original_data: return
        is_changed = False
        
        if self.new_image_path is not None: is_changed = True
        if self.view.details_name.get() != self.original_data.get('TenPhuTung', ""): is_changed = True
        if self.view.details_price.get() != str(self.original_data.get('GiaBan', "")): is_changed = True
        if self.view.details_stock.get() != str(self.original_data.get('SoLuongTon', "")): is_changed = True
        if self.part_types.get(self.view.details_loai.get()) != self.original_data.get('MaLoaiPhuTung', ""): is_changed = True
            
        self.view.update_button.config(
            state="normal" if is_changed else "disabled",
            cursor="hand2" if is_changed else ""
        )

    def update_part(self):
        """Cập nhật phụ tùng từ panel (Thay thế cho edit_product)"""
        if not self.original_data:
            messagebox.showerror("Lỗi", "Không có phụ tùng nào được chọn.")
            return
            
        part_id = self.original_data['MaPhuTung']
        
        new_name = self.view.details_name.get().strip()
        new_price_str = self.view.details_price.get().replace(",", "")
        new_stock_str = self.view.details_stock.get()
        new_loai_id = self.part_types.get(self.view.details_loai.get())

        if not new_name or not new_loai_id:
            messagebox.showwarning("Thiếu thông tin", "Tên và Loại không được để trống.")
            return
            
        try:
            new_price = float(new_price_str)
            new_stock = int(new_stock_str)
            if new_price <= 0: raise ValueError("Giá bán phải dương")
        except ValueError:
            messagebox.showerror("Lỗi nhập liệu", "Giá bán và Tồn kho phải là SỐ hợp lệ (Giá > 0).")
            return
            
        # 1. Lưu ảnh
        try:
            if self.new_image_path:
                target_path = os.path.join(self.resource_path, f"{part_id}.png")
                img = Image.open(self.new_image_path)
                img.save(target_path, "PNG")
                self.new_image_path = None
        except Exception as e:
            messagebox.showerror("Lỗi Lưu Ảnh", f"Không thể lưu ảnh mới: {e}")
            
        # 2. Cập nhật CSDL
        try:
            # CHỈ CẬP NHẬT CÁC TRƯỜNG CÓ TRÊN PANEL
            query = """
                UPDATE PhuTung
                SET TenPhuTung = %s, GiaBan = %s, SoLuongTon = %s, MaLoaiPhuTung = %s, NgayCapNhat = GETDATE()
                WHERE MaPhuTung = %s
            """
            params = (new_name, new_price, new_stock, new_loai_id, part_id)
            result = self.db.execute_query(query, params)
            
            if result:
                messagebox.showinfo("Thành công", "Cập nhật thông tin phụ tùng thành công.")
                self.load_parts(self.view.part_tree, self.view.search_entry.get())
                self.view.update_button.config(state="disabled")
                self.original_data = self.db.fetch_one("SELECT * FROM PhuTung WHERE MaPhuTung = %s", (part_id,))
            else:
                messagebox.showerror("Lỗi", "Cập nhật CSDL thất bại.")
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Lỗi: {e}")

    # --- CÁC HÀM LOGIC GỐC CỦA ADMIN (THÊM, XÓA, POPUP) ---

    def _load_part_types(self):
        """Hàm nội bộ: Tải dữ liệu LoaiPhuTung (Dùng cho cả panel và popup)"""
        try:
            types = self.db.fetch_all("SELECT MaLoaiPhuTung, TenLoaiPhuTung FROM LoaiPhuTung")
            self.part_types = {t['TenLoaiPhuTung']: t['MaLoaiPhuTung'] for t in types}
            self.part_types_inv = {t['MaLoaiPhuTung']: t['TenLoaiPhuTung'] for t in types}
            return True
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Không thể tải danh sách loại phụ tùng: {e}")
            return False

    def _show_part_dialog(self, part_data=None):
        """Hàm nội bộ: Hiển thị cửa sổ Toplevel (CHỈ DÙNG CHO THÊM MỚI)"""
        
        is_edit = part_data is not None # Logic này giờ chỉ dùng cho Thêm (is_edit=False)
        
        dialog = tk.Toplevel(self.view.window)
        dialog.title("Thêm Phụ Tùng Mới")
        dialog.resizable(False, False)
        dialog.grab_set()

        container = tk.Frame(dialog, padx=20, pady=20)
        container.pack(fill="none", expand=False)

        entries = {}
        
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

        for i, (text, key, widget_type, default) in enumerate(fields):
            tk.Label(container, text=text, font=("Arial", 11)).grid(row=i, column=0, padx=10, pady=10, sticky="e")
            
            if widget_type == "entry":
                val = default if default is not None else ""
                entry = tk.Entry(container, font=("Arial", 11), width=40)
                entry.grid(row=i, column=1, padx=10, pady=10)
                entry.insert(0, str(val))
                entries[key] = entry
                
            elif widget_type == "combo":
                val = tk.StringVar()
                val.set(default[0]) # Lấy giá trị đầu tiên
                combo = ttk.Combobox(container, textvariable=val, values=default, state="readonly", width=38, font=("Arial", 11))
                combo.grid(row=i, column=1, padx=10, pady=10)
                entries[key] = combo
                
            elif widget_type == "text":
                val = ""
                text_widget = tk.Text(container, font=("Arial", 11), width=40, height=4, relief="solid", borderwidth=1)
                text_widget.grid(row=i, column=1, padx=10, pady=10)
                text_widget.insert("1.0", val)
                entries[key] = text_widget

        def save():
            try:
                data = {}
                for key, widget in entries.items():
                    if isinstance(widget, tk.Text):
                        data[key] = widget.get("1.0", tk.END).strip() or None
                    else:
                        data[key] = widget.get().strip()
                
                if not data['TenPhuTung'] or not data['GiaNhap'] or not data['GiaBan'] or not data['SoLuongTon']:
                    messagebox.showwarning("Thiếu thông tin", "Tên, Giá Nhập, Giá Bán, và Số Lượng Tồn là bắt buộc.", parent=dialog)
                    return
                
                ma_loai_phu_tung = self.part_types.get(data['MaLoaiPhuTung'])
                
                gia_nhap = float(data['GiaNhap'])
                gia_ban = float(data['GiaBan'])
                so_luong_ton = int(data['SoLuongTon'])

                # CHỈ CÓ LOGIC INSERT
                query = """
                    INSERT INTO PhuTung 
                    (TenPhuTung, MaLoaiPhuTung, DonViTinh, GiaNhap, GiaBan, SoLuongTon, MoTa, TrangThai)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                params = (
                    data['TenPhuTung'], ma_loai_phu_tung, data['DonViTinh'], gia_nhap, gia_ban,
                    so_luong_ton, data['MoTa'], data['TrangThai']
                )
                
                if self.db.execute_query(query, params):
                    messagebox.showinfo("Thành công", "Lưu phụ tùng thành công!", parent=dialog)
                    dialog.destroy()
                    self.load_parts(self.view.part_tree)
                else:
                    messagebox.showerror("Lỗi CSDL", "Không thể lưu phụ tùng.", parent=dialog)
                    
            except ValueError:
                messagebox.showerror("Lỗi nhập liệu", "Giá Nhập, Giá Bán, Số Lượng Tồn phải là SỐ.", parent=dialog)
            except Exception as e:
                messagebox.showerror("Lỗi không xác định", f"{e}", parent=dialog)

        btn_text = "💾 Thêm Phụ Tùng"
        btn_color = "#28a745"
        
        tk.Button(container, text=btn_text, font=("Arial", 12, "bold"), bg=btn_color, fg="white", command=save, width=20, height=2).grid(row=len(fields), column=0, columnspan=2, pady=20)

    def add_part(self): 
        """Hàm public: Gọi popup Thêm"""
        self._show_part_dialog(None)
    
    def edit_part(self): 
        """Hàm cũ (Không còn dùng)"""
        messagebox.showinfo("Thông báo", "Vui lòng chọn phụ tùng từ danh sách và cập nhật trong panel chi tiết.")

    def delete_part(self): 
        """Hàm public: Xóa phụ tùng"""
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
                    self.load_parts(self.view.part_tree)
                    # Reset panel
                    self.original_data = {}
                    self.view.details_part_id.config(text="Mã: (Chưa chọn)")
                    self.view.details_name.delete(0, tk.END)
                    self.view.details_price.delete(0, tk.END)
                    self.view.details_stock.delete(0, tk.END)
                    self.view.details_loai.set("")
                    self.view.part_image_label.config(image=None)
                else:
                    messagebox.showerror("Lỗi", "Xóa thất bại.")
            except Exception as e:
                messagebox.showerror("Lỗi CSDL (Ràng buộc khóa ngoại)", 
                                     f"Không thể xóa phụ tùng: {e}\n\n"
                                     "Điều này thường xảy ra do phụ tùng đã được liên kết với một Hóa Đơn hoặc Phiếu Nhập Kho.")