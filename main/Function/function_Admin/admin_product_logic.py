# =================================================================
# FILE: main/Function/function_Admin/admin_product_logic.py
# UPDATE: CHẾ ĐỘ ADMIN - CHO PHÉP XÓA CƯỠNG CHẾ DỮ LIỆU CŨ
# =================================================================

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
            
        # Biến đệm
        self.original_data = {}
        self.new_image_path = None

        # Dữ liệu danh mục/hãng
        self.categories = {} 
        self.brands = {}     
        self.categories_inv = {}
        self.brands_inv = {}
        
        # Khởi tạo status_dict
        self.status_dict = self._load_statuses()

        # Tải dữ liệu danh mục/hãng
        self._load_categories_and_brands()
        
        # Bind event
        try:
            if hasattr(self.view, 'details_trangthai'):
                self.view.details_trangthai.bind("<<ComboboxSelected>>", self.check_for_changes)
            if hasattr(self.view, 'details_hang'):
                self.view.details_hang.bind("<<ComboboxSelected>>", self.check_for_changes)
            if hasattr(self.view, 'details_loai'):
                self.view.details_loai.bind("<<ComboboxSelected>>", self.check_for_changes)
        except:
            pass

    def _load_statuses(self):
        """Định nghĩa trạng thái (ConHang / HetHang)"""
        return {
            "Còn Hàng": "ConHang",
            "Hết Hàng": "HetHang"
        }

    def update_combobox_data(self):
        try:
            if hasattr(self.view, 'details_hang'):
                self.view.details_hang.config(values=list(self.brands.keys()))
            if hasattr(self.view, 'details_loai'):
                self.view.details_loai.config(values=list(self.categories.keys()))
            if hasattr(self.view, 'details_trangthai'):
                self.view.details_trangthai.config(values=list(self.status_dict.keys()))
        except Exception as e:
            print(f"Lỗi cập nhật Combobox: {e}")

    def load_products(self, tree, keyword=None):
        for item in tree.get_children(): 
            tree.delete(item)
            
        query = """
            SELECT sp.MaSanPham, sp.TenSanPham, hx.TenHangXe, lx.TenLoaiXe,
                   sp.GiaBan, sp.SoLuongTon, sp.TrangThai
            FROM SanPham sp
            LEFT JOIN HangXe hx ON sp.MaHangXe = hx.MaHangXe
            LEFT JOIN LoaiXe lx ON sp.MaLoaiXe = lx.MaLoaiXe
        """
        params = []
        if keyword:
            query += " WHERE sp.TenSanPham LIKE %s"
            params.append(f"%{keyword}%")
            
        query += " ORDER BY sp.MaSanPham DESC"
        
        products = self.db.fetch_all(query, params)
        if products:
            for p in products:
                db_status = p['TrangThai']
                display_status = next((k for k, v in self.status_dict.items() if v == db_status), db_status)

                tree.insert("", tk.END, values=(
                    p['MaSanPham'], 
                    p['TenSanPham'], 
                    p['TenHangXe'] or "N/A", 
                    p['TenLoaiXe'] or "N/A", 
                    f"{p['GiaBan']:,.0f}", 
                    p['SoLuongTon'],
                    display_status
                ))

    def on_product_select(self, event):
        try:
            selected_item = self.view.product_tree.selection()
            if not selected_item: return
            
            values = self.view.product_tree.item(selected_item[0], 'values')
            product_id = values[0]
            
            data = self.db.fetch_one("SELECT * FROM SanPham WHERE MaSanPham = %s", (product_id,))
            if not data: return
                
            self.original_data = data
            self.new_image_path = None
            
            self.load_product_image(product_id)
            
            self.view.details_product_id.config(text=f"Mã: {data['MaSanPham']}")
            self.view.details_name.delete(0, tk.END)
            self.view.details_name.insert(0, data['TenSanPham'])
            self.view.details_price.delete(0, tk.END)
            self.view.details_price.insert(0, f"{int(data['GiaBan'])}")
            self.view.details_stock.delete(0, tk.END)
            self.view.details_stock.insert(0, str(data['SoLuongTon']))
            
            self.view.details_hang.set(self.brands_inv.get(data['MaHangXe'], ""))
            self.view.details_loai.set(self.categories_inv.get(data['MaLoaiXe'], ""))
            
            current_code = data.get('TrangThai', '')
            status_text = next((k for k, v in self.status_dict.items() if v == current_code), "")
            self.view.details_trangthai.set(status_text)
            
            self.view.update_button.config(state="disabled", bg="#cccccc")

        except Exception as e:
            print(f"Lỗi on_product_select: {e}")

    def load_product_image(self, product_id, image_path=None):
        try:
            # 1. Xác định đường dẫn ảnh
            if image_path is None:
                image_path = os.path.join(self.resource_path, f"{product_id}.png")
            
            # 2. Xử lý ảnh (Tồn tại hoặc tạo ảnh rỗng)
            if not os.path.exists(image_path):
                img = Image.new('RGB', (150, 150), color='#e1e1e1') # Ảnh xám mặc định
            else:
                img = Image.open(image_path)
            
            # 3. Resize ảnh cho đẹp
            img = img.resize((150, 150), Image.Resampling.LANCZOS)
            self.view.product_photo = ImageTk.PhotoImage(img)
            
            # --- [FIX] TỰ ĐỘNG TÌM WIDGET ẢNH TRONG VIEW ---
            # Kiểm tra xem View đang đặt tên Label ảnh là gì để gán cho đúng
            if hasattr(self.view, 'product_image_label'):
                self.view.product_image_label.config(image=self.view.product_photo, text="")
            elif hasattr(self.view, 'image_label'):
                self.view.image_label.config(image=self.view.product_photo, text="")
            else:
                print("⚠️ CẢNH BÁO: Không tìm thấy Label hiển thị ảnh trong View (kiểm tra lại tên biến trong login.py)")
            # ------------------------------------------------
            
        except Exception as e:
            print(f"Lỗi tải ảnh: {e}")

    def upload_image(self):
        try:
            file_path = filedialog.askopenfilename(
                title="Chọn ảnh sản phẩm",
                filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
            )
            if not file_path: return
            
            self.new_image_path = file_path
            self.load_product_image(None, image_path=file_path)
            self.check_for_changes()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở ảnh: {e}")

    def check_for_changes(self, event=None):
        if not self.original_data: return
        is_changed = False
        
        if self.new_image_path: is_changed = True
        if self.view.details_name.get().strip() != str(self.original_data.get('TenSanPham', "")): is_changed = True
        
        current_price = self.view.details_price.get().replace(",", "").replace(".", "")
        if current_price != str(int(self.original_data.get('GiaBan', 0))): is_changed = True
            
        if self.view.details_stock.get().strip() != str(self.original_data.get('SoLuongTon', "")): is_changed = True
        
        current_hang_id = self.brands.get(self.view.details_hang.get().strip())
        if current_hang_id != self.original_data.get('MaHangXe'): is_changed = True
        
        current_loai_id = self.categories.get(self.view.details_loai.get().strip())
        if current_loai_id != self.original_data.get('MaLoaiXe'): is_changed = True
        
        ui_status_text = self.view.details_trangthai.get().strip()
        ui_status_code = self.status_dict.get(ui_status_text)
        if ui_status_code != self.original_data.get('TrangThai'): is_changed = True

        if is_changed:
            self.view.update_button.config(state="normal", bg="#007bff")
        else:
            self.view.update_button.config(state="disabled", bg="#cccccc")

    def update_product(self):
        if not self.original_data: return
        
        product_id = self.original_data['MaSanPham']
        name = self.view.details_name.get().strip()
        price_str = self.view.details_price.get().replace(",", "")
        stock_str = self.view.details_stock.get().strip()
        
        ma_hang = self.brands.get(self.view.details_hang.get().strip())
        ma_loai = self.categories.get(self.view.details_loai.get().strip())
        trang_thai_text = self.view.details_trangthai.get().strip()
        trang_thai_code = self.status_dict.get(trang_thai_text)

        if not name or not ma_hang or not ma_loai or not trang_thai_code:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin.")
            return
            
        try:
            price = float(price_str)
            stock = int(stock_str)
            if price < 0 or stock < 0: raise ValueError()
        except:
            messagebox.showerror("Lỗi nhập liệu", "Giá và Tồn kho phải là số dương.")
            return

        if self.new_image_path:
            try:
                img = Image.open(self.new_image_path)
                save_path = os.path.join(self.resource_path, f"{product_id}.png")
                img.save(save_path, "PNG")
            except Exception as e:
                messagebox.showerror("Lỗi ảnh", f"Không lưu được ảnh: {e}")

        query = """
            UPDATE SanPham
            SET TenSanPham=%s, GiaBan=%s, SoLuongTon=%s, MaHangXe=%s, MaLoaiXe=%s, TrangThai=%s, NgayCapNhat=GETDATE()
            WHERE MaSanPham=%s
        """
        params = (name, price, stock, ma_hang, ma_loai, trang_thai_code, product_id)
        
        if self.db.execute_query(query, params):
            messagebox.showinfo("Thành công", "Đã cập nhật sản phẩm!")
            self.load_products(self.view.product_tree)
            self.view.details_product_id.config(text="Mã: (Chưa chọn)")
            self.view.details_name.delete(0, tk.END)
            self.view.details_price.delete(0, tk.END)
            self.view.details_stock.delete(0, tk.END)
            self.view.update_button.config(state="disabled", bg="#cccccc")
            self.original_data = {}
        else:
            messagebox.showerror("Lỗi", "Cập nhật thất bại.")

    def add_product(self):
        self._show_product_dialog(None)

    def delete_product(self):
        """
        XÓA SẢN PHẨM (Logic An Toàn):
        1. Kiểm tra trạng thái: Phải là 'HetHang' mới cho xóa. Nếu 'ConHang' -> Chặn.
        2. Thực hiện xóa vĩnh viễn (Do Database đã được xử lý để giữ tên sản phẩm trong lịch sử).
        """
        selected = self.view.product_tree.selection()
        if not selected:
            messagebox.showwarning("Chọn dòng", "Vui lòng chọn sản phẩm cần xóa.")
            return
            
        values = self.view.product_tree.item(selected[0], 'values')
        p_id = values[0]
        p_name = values[1]

        # --- BƯỚC 1: KIỂM TRA TRẠNG THÁI TRƯỚC KHI XÓA ---
        curr_db = self.db.fetch_one("SELECT TrangThai FROM SanPham WHERE MaSanPham=%s", (p_id,))
        
        # Nếu không tìm thấy sản phẩm hoặc trạng thái KHÁC 'HetHang' -> Cấm xóa
        if curr_db and curr_db['TrangThai'] != 'HetHang':
            # Dịch mã trạng thái sang tiếng Việt cho dễ hiểu
            status_vn = "Còn Hàng" if curr_db['TrangThai'] == 'ConHang' else curr_db['TrangThai']
            
            messagebox.showwarning("Không thể xóa", 
                                   f"Sản phẩm '{p_name}' đang ở trạng thái: {status_vn}.\n\n"
                                   "Quy định: Bạn phải cập nhật trạng thái về 'Hết Hàng' trước khi muốn xóa nó.")
            return
        # --------------------------------------------------

        # --- BƯỚC 2: XÁC NHẬN VÀ XÓA (Khi đã thỏa điều kiện Hết Hàng) ---
        if messagebox.askyesno("Xác nhận XÓA", 
                               f"Sản phẩm '{p_name}' đã Hết Hàng.\n"
                               f"Bạn có chắc chắn muốn XÓA VĨNH VIỄN khỏi hệ thống?\n\n"
                               "(Lưu ý: Lịch sử hóa đơn và bảo hành cũ vẫn sẽ được giữ lại)"):
            try:
                query = "DELETE FROM SanPham WHERE MaSanPham = %s"
                
                if self.db.execute_query(query, (p_id,)):
                    messagebox.showinfo("Thành công", f"Đã xóa sản phẩm '{p_name}'.")
                    
                    # Xóa ảnh
                    try:
                        img_path = os.path.join(self.resource_path, f"{p_id}.png")
                        if os.path.exists(img_path):
                            os.remove(img_path)
                    except:
                        pass
                        
                    self._reset_ui_after_delete()
                else:
                    messagebox.showerror("Lỗi", "Xóa thất bại. Vui lòng kiểm tra lại kết nối.")
                    
            except Exception as e:
                messagebox.showerror("Lỗi hệ thống", f"Chi tiết lỗi: {e}")

    def _reset_ui_after_delete(self):
        """Làm mới giao diện sau khi xóa"""
        self.load_products(self.view.product_tree)
        self.original_data = {}
        self.view.details_name.delete(0, tk.END)
        self.view.details_price.delete(0, tk.END)
        self.view.details_stock.delete(0, tk.END)
        self.view.details_product_id.config(text="Mã: (Chưa chọn)")
        self.view.update_button.config(state="disabled", bg="#cccccc")

    def _load_categories_and_brands(self):
        try:
            cats = self.db.fetch_all("SELECT MaLoaiXe, TenLoaiXe FROM LoaiXe")
            self.categories = {c['TenLoaiXe']: c['MaLoaiXe'] for c in cats}
            self.categories_inv = {c['MaLoaiXe']: c['TenLoaiXe'] for c in cats}
            
            brs = self.db.fetch_all("SELECT MaHangXe, TenHangXe FROM HangXe")
            self.brands = {b['TenHangXe']: b['MaHangXe'] for b in brs}
            self.brands_inv = {b['MaHangXe']: b['TenHangXe'] for b in brs}
        except:
            pass

    def _show_product_dialog(self, product_data=None):
        # Tạo cửa sổ popup (Toplevel)
        dialog = tk.Toplevel(self.view.window)
        dialog.title("Thêm Sản Phẩm Mới")
        dialog.geometry("600x450")
        dialog.resizable(False, False)
        
        # Biến lưu đường dẫn ảnh tạm thời cho popup
        self.temp_image_path = None

        # --- Bố cục giao diện (Grid Layout) ---
        # Cột 1: Ảnh sản phẩm
        frame_img = tk.Frame(dialog, width=200, height=400)
        frame_img.pack(side="left", fill="y", padx=10, pady=10)
        
        lbl_img = tk.Label(frame_img, text="Chưa có ảnh", bg="#e1e1e1", width=20, height=10)
        lbl_img.pack(pady=10)
        
        btn_choose_img = ttk.Button(frame_img, text="Chọn Ảnh", command=lambda: self._select_image_popup(lbl_img))
        btn_choose_img.pack()

        # Cột 2: Thông tin nhập liệu
        frame_info = tk.Frame(dialog)
        frame_info.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Hàm tạo dòng nhập liệu nhanh
        def create_entry(label_text, row):
            tk.Label(frame_info, text=label_text, font=("Arial", 10, "bold")).grid(row=row, column=0, sticky="w", pady=5)
            entry = ttk.Entry(frame_info, font=("Arial", 10), width=30)
            entry.grid(row=row, column=1, pady=5, padx=5)
            return entry

        def create_combo(label_text, values, row):
            tk.Label(frame_info, text=label_text, font=("Arial", 10, "bold")).grid(row=row, column=0, sticky="w", pady=5)
            combo = ttk.Combobox(frame_info, values=values, font=("Arial", 10), width=28, state="readonly")
            combo.grid(row=row, column=1, pady=5, padx=5)
            return combo

        # Các trường nhập liệu
        entry_name = create_entry("Tên Sản Phẩm:", 0)
        
        cb_hang = create_combo("Hãng Xe:", list(self.brands.keys()), 1)
        cb_loai = create_combo("Loại Xe:", list(self.categories.keys()), 2)
        
        entry_price = create_entry("Giá Bán (VNĐ):", 3)
        entry_stock = create_entry("Tồn Kho:", 4)
        
        # Nút Lưu và Hủy
        frame_btn = tk.Frame(frame_info)
        frame_btn.grid(row=6, column=0, columnspan=2, pady=20)
        
        def save_action():
            # 1. Lấy dữ liệu từ form
            name = entry_name.get().strip()
            brand_name = cb_hang.get()
            cat_name = cb_loai.get()
            price_str = entry_price.get().strip()
            stock_str = entry_stock.get().strip()
            
            # 2. Validate (Kiểm tra dữ liệu)
            if not name or not brand_name or not cat_name or not price_str or not stock_str:
                messagebox.showwarning("Thiếu thông tin", "Vui lòng điền đầy đủ các trường.", parent=dialog)
                return

            try:
                price = float(price_str)
                stock = int(stock_str)
                if price < 0 or stock < 0: raise ValueError
            except:
                messagebox.showerror("Lỗi nhập liệu", "Giá và Tồn kho phải là số dương.", parent=dialog)
                return

            # 3. Lấy ID từ tên Hãng/Loại
            ma_hang = self.brands.get(brand_name)
            ma_loai = self.categories.get(cat_name)

            # 4. Thực hiện Insert vào Database
            try:
                query = """
                    INSERT INTO SanPham (TenSanPham, MaHangXe, MaLoaiXe, GiaBan, SoLuongTon, TrangThai, NgayTao, NgayCapNhat)
                    VALUES (%s, %s, %s, %s, %s, 'ConHang', GETDATE(), GETDATE())
                """
                params = (name, ma_hang, ma_loai, price, stock)
                
                if self.db.execute_query(query, params):
                    # Lấy ID sản phẩm vừa tạo để lưu ảnh
                    new_id_data = self.db.fetch_one("SELECT TOP 1 MaSanPham FROM SanPham ORDER BY MaSanPham DESC")
                    if new_id_data and self.temp_image_path:
                        new_id = new_id_data['MaSanPham']
                        try:
                            # Lưu ảnh vào thư mục resource
                            img = Image.open(self.temp_image_path)
                            save_path = os.path.join(self.resource_path, f"{new_id}.png")
                            img.save(save_path, "PNG")
                        except Exception as e:
                            print(f"Lỗi lưu ảnh: {e}")

                    messagebox.showinfo("Thành công", "Thêm sản phẩm mới thành công!", parent=dialog)
                    self.load_products(self.view.product_tree) # Load lại danh sách
                    dialog.destroy() # Đóng popup
                else:
                    messagebox.showerror("Lỗi", "Thêm thất bại. Lỗi Database.", parent=dialog)
            except Exception as e:
                messagebox.showerror("Lỗi hệ thống", f"Chi tiết: {e}", parent=dialog)

        ttk.Button(frame_btn, text="Lưu Sản Phẩm", command=save_action).pack(side="left", padx=10)
        ttk.Button(frame_btn, text="Hủy Bỏ", command=dialog.destroy).pack(side="left", padx=10)

    def _select_image_popup(self, label_widget):
        """Hàm hỗ trợ chọn ảnh và hiển thị preview trong popup"""
        file_path = filedialog.askopenfilename(
            title="Chọn ảnh sản phẩm",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
        )
        if file_path:
            self.temp_image_path = file_path
            try:
                img = Image.open(file_path)
                img = img.resize((80, 80), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                label_widget.config(image=photo, text="")
                label_widget.image = photo # Giữ tham chiếu để không bị mất ảnh
            except Exception as e:
                messagebox.showerror("Lỗi ảnh", f"Không đọc được ảnh: {e}")