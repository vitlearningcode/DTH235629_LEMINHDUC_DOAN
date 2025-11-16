import os
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk, filedialog, messagebox

class QuanLyProductViewLogic:
    def __init__(self, view):
        self.view = view
        self.db = view.db
        self.resource_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "..", "..", "resource", "SanPham"
        ))
        if not os.path.exists(self.resource_path):
            os.makedirs(self.resource_path)
        
        # Lấy đầy đủ mã & tên, tạo dict cho combobox mapping
        hangxe_data = self.db.fetch_all("SELECT MaHangXe, TenHangXe FROM HangXe")
        loaixe_data = self.db.fetch_all("SELECT MaLoaiXe, TenLoaiXe FROM LoaiXe")
        self.hangxe_dict = {row["TenHangXe"]: row["MaHangXe"] for row in hangxe_data}
        self.loaixe_dict = {row["TenLoaiXe"]: row["MaLoaiXe"] for row in loaixe_data}
        self.hangxe_reverse = {v: k for k, v in self.hangxe_dict.items()}
        self.loaixe_reverse = {v: k for k, v in self.loaixe_dict.items()}

        self.original_data = {}
        self.new_image_path = None

    def load_view(self, tree, keyword=None):
        for item in tree.get_children():
            tree.delete(item)
        query = """
        SELECT sp.MaSanPham, sp.TenSanPham, hx.TenHangXe, lx.TenLoaiXe, sp.GiaBan, sp.SoLuongTon
        FROM SanPham sp
        LEFT JOIN HangXe hx ON sp.MaHangXe = hx.MaHangXe
        LEFT JOIN LoaiXe lx ON sp.MaLoaiXe = lx.MaLoaiXe
        """
        params = []
        if keyword is not None and keyword.strip() != "":
            query += " WHERE sp.TenSanPham LIKE %s"
            params.append(f"%{keyword}%")
        query += " ORDER BY sp.MaSanPham"
        records = self.db.fetch_all(query, params)
        if records:
            for rec in records:
                tree.insert(
                    "", tk.END,
                    values=(
                        rec['MaSanPham'],
                        rec['TenSanPham'],
                        rec['TenHangXe'] or "N/A",
                        rec['TenLoaiXe'] or "N/A",
                        f"{rec['GiaBan']:,.0f} VNĐ" if rec['GiaBan'] else "0 VNĐ",
                        rec['SoLuongTon']
                    )
                )

    def on_product_select(self, event):
        try:
            selected_item = self.view.product_tree.selection()[0]
            values = self.view.product_tree.item(selected_item, 'values')
            if not values:
                return
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
            self.view.details_hang.set(self.hangxe_reverse.get(data['MaHangXe'] or "", ""))
            self.view.details_loai.set(self.loaixe_reverse.get(data['MaLoaiXe'] or "", ""))
            self.view.update_button.config(state="disabled")
        except IndexError:
            pass
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải chi tiết: {e}")

    def load_product_image(self, product_id, image_path=None):
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
        try:
            file_path = filedialog.askopenfilename(
                title="Chọn ảnh sản phẩm",
                filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif")]
            )
            if not file_path:
                return
            self.new_image_path = file_path
            self.load_product_image(None, image_path=file_path)
            self.check_for_changes()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở ảnh: {e}")

    def check_for_changes(self, event=None):
        if not self.original_data:
            return
        is_changed = False
        if self.view.details_name.get() != self.original_data.get('TenSanPham', ""):
            is_changed = True
        if self.view.details_price.get() != str(self.original_data.get('GiaBan', "")):
            is_changed = True
        if self.view.details_stock.get() != str(self.original_data.get('SoLuongTon', "")):
            is_changed = True
        if self.hangxe_dict.get(self.view.details_hang.get(), "") != self.original_data.get('MaHangXe', ""):
            is_changed = True
        if self.loaixe_dict.get(self.view.details_loai.get(), "") != self.original_data.get('MaLoaiXe', ""):
            is_changed = True
        if self.new_image_path is not None:
            is_changed = True
        self.view.update_button.config(
            state="normal" if is_changed else "disabled",
            cursor="hand2" if is_changed else ""
        )

    def update_product(self):
        if not self.original_data:
            messagebox.showerror("Lỗi", "Không có sản phẩm nào được chọn.")
            return
        product_id = self.original_data['MaSanPham']
        new_name = self.view.details_name.get().strip()
        # Xử lý giá bán đúng và hợp lệ
        try:
            new_price = int(float(self.view.details_price.get().replace(",", "")))
        except ValueError:
            new_price = 0
        try:
            new_stock = int(self.view.details_stock.get())
        except ValueError:
            new_stock = 0
        new_hang = self.hangxe_dict.get(self.view.details_hang.get(), "")
        new_loai = self.loaixe_dict.get(self.view.details_loai.get(), "")
        if not new_name or not new_hang or not new_loai:
            messagebox.showwarning("Thiếu thông tin", "Các trường không được để trống.")
            return
        if new_price <= 0:
            messagebox.showwarning("Sai giá trị", "Giá bán phải lớn hơn 0!")
            return
        try:
            if self.new_image_path:
                target_path = os.path.join(self.resource_path, f"{product_id}.png")
                img = Image.open(self.new_image_path)
                img.save(target_path, "PNG")
                self.new_image_path = None
        except Exception as e:
            messagebox.showerror("Lỗi Lưu Ảnh", f"Không thể lưu ảnh mới: {e}")
        try:
            query = """
            UPDATE SanPham
            SET TenSanPham = %s, GiaBan = %s, SoLuongTon = %s, MaHangXe = %s, MaLoaiXe = %s
            WHERE MaSanPham = %s
            """
            params = (new_name, new_price, new_stock, new_hang, new_loai, product_id)
            result = self.db.execute_query(query, params)
            if result:
                messagebox.showinfo("Thành công", "Cập nhật thông tin sản phẩm thành công.")
                self.load_view(self.view.product_tree, self.view.search_entry.get())
                self.view.update_button.config(state="disabled")
                self.original_data = self.db.fetch_one("SELECT * FROM SanPham WHERE MaSanPham = %s", (product_id,))
            else:
                messagebox.showerror("Lỗi", "Cập nhật CSDL thất bại.")
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Lỗi: {e}")
            print(f"Lỗi SQL khi update SP: {e}")
