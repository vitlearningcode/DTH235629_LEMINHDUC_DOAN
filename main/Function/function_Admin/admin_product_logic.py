# main/Function/function_Admin/admin_product_logic.py
# PHIÊN BẢN NÂNG CẤP: Kết hợp logic CRUD của Admin và logic Panel của QuanLy

import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from PIL import Image, ImageTk
import os

class AdminProductLogic:
    def __init__(self, view):
        self.view = view
        self.db = view.db
        
        # Đường dẫn thư mục tài nguyên
        self.resource_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "..", "..", "resource", "SanPham"
        ))
        if not os.path.exists(self.resource_path):
            os.makedirs(self.resource_path)
            
        # Biến đệm (Lấy từ logic của QuanLy)
        self.original_data = {}
        self.new_image_path = None

        # Biến đệm (Lấy từ logic gốc của Admin, dùng cho popup Thêm)
        self.categories = {} 
        self.brands = {}     
        self.categories_inv = {}
        self.brands_inv = {}
        
        # Tải dữ liệu cho combobox (cả panel và popup)
        self._load_categories_and_brands()
        
        # Cập nhật combobox trên panel (nếu chúng đã được vẽ)
        try:
            self.view.details_hang.config(values=list(self.brands.keys()))
            self.view.details_loai.config(values=list(self.categories.keys()))
        except:
            pass # Lỗi nếu UI chưa được vẽ

    def load_products(self, tree, keyword=None):
        """Tải danh sách sản phẩm (Logic từ QuanLy, đổi tên load_view -> load_products)"""
        for item in tree.get_children(): 
            tree.delete(item)
            
        query = """
            SELECT sp.MaSanPham, sp.TenSanPham, hx.TenHangXe, lx.TenLoaiXe,
                   sp.GiaBan, sp.SoLuongTon
            FROM SanPham sp
            LEFT JOIN HangXe hx ON sp.MaHangXe = hx.MaHangXe
            LEFT JOIN LoaiXe lx ON sp.MaLoaiXe = lx.MaLoaiXe
        """
        params = []
        if keyword:
            query += " WHERE sp.TenSanPham LIKE %s"
            params.append(f"%{keyword}%")
            
        query += " ORDER BY sp.MaSanPham"
        
        products = self.db.fetch_all(query, params)
        if products:
            for p in products:
                tree.insert("", tk.END, values=(
                    p['MaSanPham'], 
                    p['TenSanPham'], 
                    p['TenHangXe'] or "N/A", 
                    p['TenLoaiXe'] or "N/A", 
                    f"{p['GiaBan']:,.0f} VNĐ", # Format tiền
                    p['SoLuongTon']
                ))

    # --- CÁC HÀM LOGIC CHO PANEL (LẤY TỪ QUANLY_PRODUCT_VIEW_LOGIC) ---

    def on_product_select(self, event):
        """Khi click vào sản phẩm trên cây, hiển thị chi tiết lên panel"""
        try:
            selected_item = self.view.product_tree.selection()[0]
            values = self.view.product_tree.item(selected_item, 'values')
            if not values: return
            
            product_id = values[0]
            data = self.db.fetch_one("SELECT * FROM SanPham WHERE MaSanPham = %s", (product_id,))
            if not data:
                messagebox.showerror("Lỗi", "Không tìm thấy sản phẩm.")
                return
                
            self.original_data = data
            self.new_image_path = None
            
            self.load_product_image(product_id)
            self.view.details_product_id.config(text=f"Mã: {data['MaSanPham']}")
            self.view.details_name.delete(0, tk.END)
            self.view.details_name.insert(0, data['TenSanPham'])
            self.view.details_price.delete(0, tk.END)
            self.view.details_price.insert(0, str(data['GiaBan'] or 0))
            self.view.details_stock.delete(0, tk.END)
            self.view.details_stock.insert(0, str(data['SoLuongTon'] or 0))
            
            # Dùng dict đã tải trong __init__ để set giá trị
            self.view.details_hang.set(self.brands_inv.get(data['MaHangXe'], ""))
            self.view.details_loai.set(self.categories_inv.get(data['MaLoaiXe'], ""))
            
            self.view.update_button.config(state="disabled")
        except IndexError:
            pass
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải chi tiết: {e}")

    def load_product_image(self, product_id, image_path=None):
        """Tải ảnh cho panel"""
        try:
            if image_path is None:
                image_path = os.path.join(self.resource_path, f"{product_id}.png")
            if not os.path.exists(image_path):
                image_path = os.path.join(self.resource_path, "default_product.png")
            if not os.path.exists(image_path):
                img = Image.new('RGB', (150, 150), color='grey')
                img.save(image_path)
                
            img = Image.open(image_path)
            img = img.resize((150, 150), Image.Resampling.LANCZOS)
            self.view.product_photo = ImageTk.PhotoImage(img)
            self.view.product_image_label.config(image=self.view.product_photo)
        except Exception as e:
            print(f"Lỗi tải ảnh sản phẩm: {e}")

    def upload_image(self):
        """Tải ảnh lên cho panel"""
        try:
            file_path = filedialog.askopenfilename(
                title="Chọn ảnh sản phẩm",
                filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif")]
            )
            if not file_path: return
            
            self.new_image_path = file_path
            self.load_product_image(None, image_path=file_path)
            self.check_for_changes()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở ảnh: {e}")

    def check_for_changes(self, event=None):
        """Kiểm tra thay đổi trên panel để bật/tắt nút Cập Nhật"""
        if not self.original_data: return
        is_changed = False
        
        if self.new_image_path is not None: is_changed = True
        if self.view.details_name.get() != self.original_data.get('TenSanPham', ""): is_changed = True
        if self.view.details_price.get() != str(self.original_data.get('GiaBan', "")): is_changed = True
        if self.view.details_stock.get() != str(self.original_data.get('SoLuongTon', "")): is_changed = True
        if self.brands.get(self.view.details_hang.get()) != self.original_data.get('MaHangXe', ""): is_changed = True
        if self.categories.get(self.view.details_loai.get()) != self.original_data.get('MaLoaiXe', ""): is_changed = True
            
        self.view.update_button.config(
            state="normal" if is_changed else "disabled",
            cursor="hand2" if is_changed else ""
        )

    def update_product(self):
        """Cập nhật sản phẩm từ panel (Thay thế cho edit_product)"""
        if not self.original_data:
            messagebox.showerror("Lỗi", "Không có sản phẩm nào được chọn.")
            return
            
        product_id = self.original_data['MaSanPham']
        
        # Lấy dữ liệu từ panel
        new_name = self.view.details_name.get().strip()
        new_price_str = self.view.details_price.get().replace(",", "")
        new_stock_str = self.view.details_stock.get()
        new_hang_id = self.brands.get(self.view.details_hang.get())
        new_loai_id = self.categories.get(self.view.details_loai.get())

        if not new_name or not new_hang_id or not new_loai_id:
            messagebox.showwarning("Thiếu thông tin", "Tên, Hãng, và Loại không được để trống.")
            return
            
        try:
            new_price = float(new_price_str)
            new_stock = int(new_stock_str)
            if new_price <= 0: raise ValueError("Giá bán phải dương")
        except ValueError:
            messagebox.showerror("Lỗi nhập liệu", "Giá bán và Tồn kho phải là SỐ hợp lệ (Giá > 0).")
            return
            
        # 1. Lưu ảnh (nếu có ảnh mới)
        try:
            if self.new_image_path:
                target_path = os.path.join(self.resource_path, f"{product_id}.png")
                img = Image.open(self.new_image_path)
                img.save(target_path, "PNG")
                self.new_image_path = None
        except Exception as e:
            messagebox.showerror("Lỗi Lưu Ảnh", f"Không thể lưu ảnh mới: {e}")
            
        # 2. Cập nhật CSDL
        try:
            query = """
                UPDATE SanPham
                SET TenSanPham = %s, GiaBan = %s, SoLuongTon = %s, MaHangXe = %s, MaLoaiXe = %s, NgayCapNhat = GETDATE()
                WHERE MaSanPham = %s
            """
            params = (new_name, new_price, new_stock, new_hang_id, new_loai_id, product_id)
            result = self.db.execute_query(query, params)
            
            if result:
                messagebox.showinfo("Thành công", "Cập nhật thông tin sản phẩm thành công.")
                self.load_products(self.view.product_tree, self.view.search_entry.get())
                self.view.update_button.config(state="disabled")
                # Tải lại dữ liệu gốc
                self.original_data = self.db.fetch_one("SELECT * FROM SanPham WHERE MaSanPham = %s", (product_id,))
            else:
                messagebox.showerror("Lỗi", "Cập nhật CSDL thất bại.")
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Lỗi: {e}")

    # --- CÁC HÀM LOGIC GỐC CỦA ADMIN (THÊM, XÓA, POPUP) ---

    def _load_categories_and_brands(self):
        """Hàm nội bộ: Tải dữ liệu cho Combobox (Dùng cho cả panel và popup)"""
        try:
            cats = self.db.fetch_all("SELECT MaLoaiXe, TenLoaiXe FROM LoaiXe")
            self.categories = {c['TenLoaiXe']: c['MaLoaiXe'] for c in cats}
            self.categories_inv = {c['MaLoaiXe']: c['TenLoaiXe'] for c in cats}
            
            brs = self.db.fetch_all("SELECT MaHangXe, TenHangXe FROM HangXe")
            self.brands = {b['TenHangXe']: b['MaHangXe'] for b in brs}
            self.brands_inv = {b['MaHangXe']: b['TenHangXe'] for b in brs}
            return True
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Không thể tải danh mục hoặc hãng xe: {e}")
            return False

    def _show_product_dialog(self, product_data=None):
        """Hàm nội bộ: Hiển thị cửa sổ Toplevel (CHỈ DÙNG CHO THÊM MỚI)"""
        
        # (Không cần tải lại categories/brands vì đã tải trong __init__)

        is_edit = product_data is not None # Logic này giờ chỉ dùng cho Thêm (is_edit=False)
        
        dialog = tk.Toplevel(self.view.window)
        dialog.title("Thêm Sản Phẩm Mới")
        dialog.resizable(False, False)
        dialog.grab_set()

        container = tk.Frame(dialog, padx=20, pady=20)
        container.pack(fill="none", expand=False)

        entries = {}
        
        fields = [
            ("Tên Sản Phẩm:", "TenSanPham", "entry", None),
            ("Hãng Xe:", "MaHangXe", "combo", list(self.brands.keys())),
            ("Loại Xe:", "MaLoaiXe", "combo", list(self.categories.keys())),
            ("Phân Khối (CC):", "PhanKhoi", "entry", None),
            ("Màu Sắc:", "MauSac", "entry", None),
            ("Năm Sản Xuất:", "NamSanXuat", "entry", None),
            ("Giá Bán:", "GiaBan", "entry", None),
            ("Số Lượng Tồn:", "SoLuongTon", "entry", 0), # Mặc định là 0
            ("Thời Gian Bảo Hành (tháng):", "ThoiGianBaoHanh", "entry", 12),
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
                
                if not data['TenSanPham'] or not data['GiaBan'] or not data['SoLuongTon']:
                    messagebox.showwarning("Thiếu thông tin", "Tên, Giá Bán, và Số Lượng Tồn là bắt buộc.", parent=dialog)
                    return
                
                ma_hang_xe = self.brands.get(data['MaHangXe'])
                ma_loai_xe = self.categories.get(data['MaLoaiXe'])
                
                gia_ban = float(data['GiaBan'])
                so_luong_ton = int(data['SoLuongTon'])
                phan_khoi = int(data['PhanKhoi']) if data['PhanKhoi'] else None
                nam_sx = int(data['NamSanXuat']) if data['NamSanXuat'] else None
                bao_hanh = int(data['ThoiGianBaoHanh']) if data['ThoiGianBaoHanh'] else 12

                # CHỈ CÓ LOGIC INSERT (VÌ EDIT ĐÃ CHUYỂN QUA PANEL)
                query = """
                    INSERT INTO SanPham 
                    (TenSanPham, MaLoaiXe, MaHangXe, PhanKhoi, MauSac, NamSanXuat, GiaBan, SoLuongTon, MoTa, ThoiGianBaoHanh, TrangThai)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                params = (
                    data['TenSanPham'], ma_loai_xe, ma_hang_xe, phan_khoi, data['MauSac'] or None, nam_sx,
                    gia_ban, so_luong_ton, data['MoTa'], bao_hanh, data['TrangThai']
                )
                
                if self.db.execute_query(query, params):
                    messagebox.showinfo("Thành công", "Thêm sản phẩm thành công!", parent=dialog)
                    dialog.destroy()
                    self.load_products(self.view.product_tree)
                else:
                    messagebox.showerror("Lỗi CSDL", "Không thể lưu sản phẩm.", parent=dialog)
                    
            except ValueError:
                messagebox.showerror("Lỗi nhập liệu", "Giá bán, Số lượng, Năm, Phân khối, Bảo hành phải là SỐ.", parent=dialog)
            except Exception as e:
                messagebox.showerror("Lỗi không xác định", f"{e}", parent=dialog)

        btn_text = "💾 Thêm Sản Phẩm"
        btn_color = "#28a745"
        
        tk.Button(container, text=btn_text, font=("Arial", 12, "bold"), bg=btn_color, fg="white", command=save, width=20, height=2).grid(row=len(fields), column=0, columnspan=2, pady=20)


    def add_product(self):
        """Hàm public: Gọi popup Thêm"""
        self._show_product_dialog(None)
    
    def edit_product(self):
        """Hàm cũ (Không còn dùng) - Giờ chúng ta dùng update_product từ panel"""
        messagebox.showinfo("Thông báo", "Vui lòng chọn sản phẩm từ danh sách và cập nhật trong panel chi tiết.")

    def delete_product(self):
        """Hàm public: Xóa sản phẩm"""
        selected = self.view.product_tree.selection()
        if not selected:
            messagebox.showwarning("Chú ý", "Vui lòng chọn một sản phẩm để xóa.")
            return

        item = self.view.product_tree.item(selected[0])
        sp_id = item['values'][0]
        sp_name = item['values'][1]

        if messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc muốn XÓA VĨNH VIỄN sản phẩm:\n\n{sp_name} (ID: {sp_id})\n\nLưu ý: Hành động này sẽ thất bại nếu sản phẩm đã tồn tại trong hóa đơn hoặc phiếu nhập kho."):
            try:
                result = self.db.execute_query("DELETE FROM SanPham WHERE MaSanPham = %s", (sp_id,))
                
                if result:
                    messagebox.showinfo("Thành công", f"Đã xóa sản phẩm '{sp_name}'.")
                    self.load_products(self.view.product_tree)
                    # Reset panel
                    self.original_data = {}
                    self.view.details_product_id.config(text="Mã: (Chưa chọn)")
                    self.view.details_name.delete(0, tk.END)
                    self.view.details_price.delete(0, tk.END)
                    self.view.details_stock.delete(0, tk.END)
                    self.view.details_hang.set("")
                    self.view.details_loai.set("")
                    self.view.product_image_label.config(image=None)
                else:
                    messagebox.showerror("Lỗi", "Xóa thất bại.")
            except Exception as e:
                messagebox.showerror("Lỗi CSDL (Ràng buộc khóa ngoại)", 
                                     f"Không thể xóa sản phẩm: {e}\n\n"
                                     "Điều này thường xảy ra do sản phẩm đã được liên kết với một Hóa Đơn hoặc Phiếu Nhập Kho.")