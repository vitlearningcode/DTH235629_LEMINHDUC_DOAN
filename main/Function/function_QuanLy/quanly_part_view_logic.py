import os
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk, filedialog, messagebox

class QuanLyPartViewLogic:
    def __init__(self, view):
        self.view = view
        self.db = view.db
        self.resource_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "..", "..", "resource", "PhuTung"
        ))
        if not os.path.exists(self.resource_path):
            os.makedirs(self.resource_path)
        
        # Nếu có bảng Hãng Phụ Tùng, mapping như sau:
        # hangpt_data = self.db.fetch_all("SELECT MaHangPhuTung, TenHangPhuTung FROM HangPhuTung")
        # self.hangpt_dict = {row["TenHangPhuTung"]: row["MaHangPhuTung"] for row in hangpt_data}
        # self.hangpt_reverse = {v: k for k, v in self.hangpt_dict.items()}
        # Loại phụ tùng
        loaipt_data = self.db.fetch_all("SELECT MaLoaiPhuTung, TenLoaiPhuTung FROM LoaiPhuTung")
        self.loaipt_dict = {row["TenLoaiPhuTung"]: row["MaLoaiPhuTung"] for row in loaipt_data}
        self.loaipt_reverse = {v: k for k, v in self.loaipt_dict.items()}

        self.original_data = {}
        self.new_image_path = None

    def load_view(self, tree, keyword=None):
        for item in tree.get_children():
            tree.delete(item)
        query = """
        SELECT pt.MaPhuTung, pt.TenPhuTung, lpt.TenLoaiPhuTung, pt.GiaBan, pt.SoLuongTon
        FROM PhuTung pt
        LEFT JOIN LoaiPhuTung lpt ON pt.MaLoaiPhuTung = lpt.MaLoaiPhuTung
        """
        params = []
        if keyword is not None and keyword.strip() != "":
            query += " WHERE pt.TenPhuTung LIKE %s"
            params.append(f"%{keyword}%")
        query += " ORDER BY pt.MaPhuTung"
        records = self.db.fetch_all(query, params)
        if records:
            for rec in records:
                tree.insert(
                    "", tk.END,
                    values=(
                        rec['MaPhuTung'],
                        rec['TenPhuTung'],
                        rec['TenLoaiPhuTung'] or "N/A",
                        f"{rec['GiaBan']:,.0f} VNĐ" if rec['GiaBan'] else "0 VNĐ",
                        rec['SoLuongTon']
                    )
                )

    def on_part_select(self, event):
        try:
            selected_item = self.view.part_tree.selection()[0]
            values = self.view.part_tree.item(selected_item, 'values')
            if not values:
                return
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
            self.view.details_loai.set(self.loaipt_reverse.get(data['MaLoaiPhuTung'] or "", ""))
            self.view.update_button.config(state="disabled")
        except IndexError:
            pass
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải chi tiết: {e}")

    def load_part_image(self, part_id, image_path=None):
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
        try:
            file_path = filedialog.askopenfilename(
                title="Chọn ảnh phụ tùng",
                filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif")]
            )
            if not file_path:
                return
            self.new_image_path = file_path
            self.load_part_image(None, image_path=file_path)
            self.check_for_changes()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở ảnh: {e}")

    def check_for_changes(self, event=None):
        if not self.original_data:
            return
        is_changed = False
        if self.view.details_name.get() != self.original_data.get('TenPhuTung', ""):
            is_changed = True
        if self.view.details_price.get() != str(self.original_data.get('GiaBan', "")):
            is_changed = True
        if self.view.details_stock.get() != str(self.original_data.get('SoLuongTon', "")):
            is_changed = True
        if self.loaipt_dict.get(self.view.details_loai.get(), "") != self.original_data.get('MaLoaiPhuTung', ""):
            is_changed = True
        if self.new_image_path is not None:
            is_changed = True
        self.view.update_button.config(
            state="normal" if is_changed else "disabled",
            cursor="hand2" if is_changed else ""
        )

    def update_part(self):
        if not self.original_data:
            messagebox.showerror("Lỗi", "Không có phụ tùng nào được chọn.")
            return
        part_id = self.original_data['MaPhuTung']
        new_name = self.view.details_name.get().strip()
        try:
            new_price = int(float(self.view.details_price.get().replace(",", "")))
        except ValueError:
            new_price = 0
        try:
            new_stock = int(self.view.details_stock.get())
        except ValueError:
            new_stock = 0
        new_loai = self.loaipt_dict.get(self.view.details_loai.get(), "")
        if not new_name or not new_loai:
            messagebox.showwarning("Thiếu thông tin", "Các trường không được để trống.")
            return
        if new_price <= 0:
            messagebox.showwarning("Sai giá trị", "Giá bán phải lớn hơn 0!")
            return
        try:
            if self.new_image_path:
                target_path = os.path.join(self.resource_path, f"{part_id}.png")
                img = Image.open(self.new_image_path)
                img.save(target_path, "PNG")
                self.new_image_path = None
        except Exception as e:
            messagebox.showerror("Lỗi Lưu Ảnh", f"Không thể lưu ảnh mới: {e}")
        try:
            query = """
            UPDATE PhuTung
            SET TenPhuTung = %s, GiaBan = %s, SoLuongTon = %s, MaLoaiPhuTung = %s
            WHERE MaPhuTung = %s
            """
            params = (new_name, new_price, new_stock, new_loai, part_id)
            result = self.db.execute_query(query, params)
            if result:
                messagebox.showinfo("Thành công", "Cập nhật thông tin phụ tùng thành công.")
                self.load_view(self.view.part_tree, self.view.search_entry.get())
                self.view.update_button.config(state="disabled")
                self.original_data = self.db.fetch_one("SELECT * FROM PhuTung WHERE MaPhuTung = %s", (part_id,))
            else:
                messagebox.showerror("Lỗi", "Cập nhật CSDL thất bại.")
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Lỗi: {e}")
            print(f"Lỗi SQL khi update phụ tùng: {e}")
