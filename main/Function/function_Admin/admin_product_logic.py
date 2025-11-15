# main/Function/function_Admin/admin_product_logic.py

import tkinter as tk
from tkinter import messagebox, ttk # Thêm ttk để dùng Combobox

class AdminProductLogic:
    def __init__(self, view):
        self.view = view
        self.db = view.db
        
        # Biến đệm để lưu trữ danh mục và hãng xe, tránh gọi CSDL liên tục
        self.categories = {} # { 'Xe Số': 1, ... }
        self.brands = {}     # { 'Honda': 1, ... }
        self.categories_inv = {} # { 1: 'Xe Số', ... }
        self.brands_inv = {}     # { 1: 'Honda', ... }

    def load_products(self):
        """Tải danh sách sản phẩm lên treeview"""
        for item in self.view.product_tree.get_children(): 
            self.view.product_tree.delete(item)
        query = """
            SELECT sp.MaSanPham, sp.TenSanPham, hx.TenHangXe, lx.TenLoaiXe,
                   sp.MauSac, sp.GiaBan, sp.SoLuongTon, sp.TrangThai
            FROM SanPham sp
            LEFT JOIN HangXe hx ON sp.MaHangXe = hx.MaHangXe
            LEFT JOIN LoaiXe lx ON sp.MaLoaiXe = lx.MaLoaiXe
            ORDER BY sp.MaSanPham
        """
        products = self.db.fetch_all(query)
        if products:
            for p in products:
                self.view.product_tree.insert("", tk.END, values=(
                    p['MaSanPham'], 
                    p['TenSanPham'], 
                    p['TenHangXe'] or "N/A",  # Hiển thị N/A nếu JOIN bị null
                    p['TenLoaiXe'] or "N/A", 
                    p['MauSac'] or "",
                    f"{p['GiaBan']:,.0f}", # Format tiền tệ
                    p['SoLuongTon'], 
                    p['TrangThai']
                ))

    def _load_categories_and_brands(self):
        """Hàm nội bộ: Tải dữ liệu cho Combobox và lưu vào biến đệm"""
        try:
            # Tải LoaiXe
            cats = self.db.fetch_all("SELECT MaLoaiXe, TenLoaiXe FROM LoaiXe")
            self.categories = {c['TenLoaiXe']: c['MaLoaiXe'] for c in cats}
            self.categories_inv = {c['MaLoaiXe']: c['TenLoaiXe'] for c in cats}
            
            # Tải HangXe
            brs = self.db.fetch_all("SELECT MaHangXe, TenHangXe FROM HangXe")
            self.brands = {b['TenHangXe']: b['MaHangXe'] for b in brs}
            self.brands_inv = {b['MaHangXe']: b['TenHangXe'] for b in brs}
            return True
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Không thể tải danh mục hoặc hãng xe: {e}")
            return False

    # --- BẮT ĐẦU PHẦN ĐƯỢC CẬP NHẬT ---
    def _show_product_dialog(self, product_data=None):
        """Hàm nội bộ: Hiển thị cửa sổ Toplevel cho Thêm hoặc Sửa"""
        
        # Tải dữ liệu hãng/loại xe trước
        if not self._load_categories_and_brands():
            return # Dừng nếu không tải được

        is_edit = product_data is not None
        
        dialog = tk.Toplevel(self.view.window)
        dialog.title("Thêm Sản Phẩm Mới" if not is_edit else f"Cập Nhật Sản Phẩm (ID: {product_data['MaSanPham']})")
        
        # === SỬA LỖI GIAO DIỆN ===
        # dialog.geometry("550x650") # <-- XÓA DÒNG NÀY
        dialog.resizable(False, False) # <-- THÊM DÒNG NÀY
        dialog.grab_set()

        container = tk.Frame(dialog, padx=20, pady=20)
        # container.pack(fill=tk.BOTH, expand=True) # <-- SỬA DÒNG NÀY
        container.pack(fill="none", expand=False) # <-- THÀNH DÒNG NÀY
        # === KẾT THÚC SỬA LỖI ===

        entries = {}
        
        # Định nghĩa các trường
        fields = [
            ("Tên Sản Phẩm:", "TenSanPham", "entry", None),
            ("Hãng Xe:", "MaHangXe", "combo", list(self.brands.keys())),
            ("Loại Xe:", "MaLoaiXe", "combo", list(self.categories.keys())),
            ("Phân Khối (CC):", "PhanKhoi", "entry", None),
            ("Màu Sắc:", "MauSac", "entry", None),
            ("Năm Sản Xuất:", "NamSanXuat", "entry", None),
            ("Giá Bán:", "GiaBan", "entry", None),
            ("Số Lượng Tồn:", "SoLuongTon", "entry", None),
            ("Thời Gian Bảo Hành (tháng):", "ThoiGianBaoHanh", "entry", 12),
            ("Trạng Thái:", "TrangThai", "combo", ['ConHang', 'HetHang', 'NgungKinhDoanh']),
            ("Mô Tả:", "MoTa", "text", None)
        ]

        # Tạo các widget
        for i, (text, key, widget_type, default) in enumerate(fields):
            tk.Label(container, text=text, font=("Arial", 11)).grid(row=i, column=0, padx=10, pady=10, sticky="e")
            
            if widget_type == "entry":
                val = ""
                if is_edit:
                    val = product_data.get(key) or ""
                elif default:
                    val = default
                    
                entry = tk.Entry(container, font=("Arial", 11), width=40)
                entry.grid(row=i, column=1, padx=10, pady=10)
                entry.insert(0, str(val))
                entries[key] = entry
                
            elif widget_type == "combo":
                val = tk.StringVar()
                if is_edit:
                    # Chuyển ID (ví dụ: 1) thành Tên (ví dụ: 'Honda')
                    if key == "MaHangXe":
                        val.set(self.brands_inv.get(product_data.get(key), ""))
                    elif key == "MaLoaiXe":
                        val.set(self.categories_inv.get(product_data.get(key), ""))
                    elif key == "TrangThai":
                        val.set(product_data.get(key))
                elif default:
                    val.set(default[0]) # Lấy giá trị đầu tiên

                combo = ttk.Combobox(container, textvariable=val, values=default, state="readonly", width=38, font=("Arial", 11))
                combo.grid(row=i, column=1, padx=10, pady=10)
                entries[key] = combo
                
            elif widget_type == "text":
                val = ""
                if is_edit:
                    val = product_data.get(key) or ""
                
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
                if not data['TenSanPham'] or not data['GiaBan'] or not data['SoLuongTon']:
                    messagebox.showwarning("Thiếu thông tin", "Tên, Giá Bán, và Số Lượng Tồn là bắt buộc.", parent=dialog)
                    return
                
                # Chuyển đổi giá trị Combobox từ Tên về ID
                ma_hang_xe = self.brands.get(data['MaHangXe'])
                ma_loai_xe = self.categories.get(data['MaLoaiXe'])
                
                # Chuyển đổi số
                gia_ban = float(data['GiaBan'])
                so_luong_ton = int(data['SoLuongTon'])
                phan_khoi = int(data['PhanKhoi']) if data['PhanKhoi'] else None
                nam_sx = int(data['NamSanXuat']) if data['NamSanXuat'] else None
                bao_hanh = int(data['ThoiGianBaoHanh']) if data['ThoiGianBaoHanh'] else 12

                # Chuẩn bị query
                if is_edit:
                    query = """
                        UPDATE SanPham SET 
                        TenSanPham=%s, MaLoaiXe=%s, MaHangXe=%s, PhanKhoi=%s, MauSac=%s, NamSanXuat=%s,
                        GiaBan=%s, SoLuongTon=%s, MoTa=%s, ThoiGianBaoHanh=%s, TrangThai=%s, NgayCapNhat=GETDATE()
                        WHERE MaSanPham=%s
                    """
                    params = (
                        data['TenSanPham'], ma_loai_xe, ma_hang_xe, phan_khoi, data['MauSac'] or None, nam_sx,
                        gia_ban, so_luong_ton, data['MoTa'], bao_hanh, data['TrangThai'],
                        product_data['MaSanPham'] # ID cho WHERE
                    )
                else:
                    query = """
                        INSERT INTO SanPham 
                        (TenSanPham, MaLoaiXe, MaHangXe, PhanKhoi, MauSac, NamSanXuat, GiaBan, SoLuongTon, MoTa, ThoiGianBaoHanh, TrangThai)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    params = (
                        data['TenSanPham'], ma_loai_xe, ma_hang_xe, phan_khoi, data['MauSac'] or None, nam_sx,
                        gia_ban, so_luong_ton, data['MoTa'], bao_hanh, data['TrangThai']
                    )
                
                # Thực thi
                if self.db.execute_query(query, params):
                    messagebox.showinfo("Thành công", "Lưu sản phẩm thành công!", parent=dialog)
                    dialog.destroy()
                    self.load_products()
                else:
                    messagebox.showerror("Lỗi CSDL", "Không thể lưu sản phẩm.", parent=dialog)
                    
            except ValueError:
                messagebox.showerror("Lỗi nhập liệu", "Giá bán, Số lượng, Năm, Phân khối, Bảo hành phải là SỐ.", parent=dialog)
            except Exception as e:
                messagebox.showerror("Lỗi không xác định", f"{e}", parent=dialog)

        btn_text = "💾 Lưu Thay Đổi" if is_edit else "💾 Thêm Sản Phẩm"
        btn_color = "#007bff" if is_edit else "#28a745"
        
        tk.Button(container, text=btn_text, font=("Arial", 12, "bold"), bg=btn_color, fg="white", command=save, width=20, height=2).grid(row=len(fields), column=0, columnspan=2, pady=20)


    # --- CHỨC NĂNG THÊM MỚI ---
    def add_product(self):
        self._show_product_dialog(None) # Gọi hàm nội bộ với dữ liệu rỗng
    
    # --- CHỨC NĂNG SỬA ---
    def edit_product(self):
        selected = self.view.product_tree.selection()
        if not selected:
            messagebox.showwarning("Chú ý", "Vui lòng chọn một sản phẩm để sửa.")
            return
        
        sp_id = self.view.product_tree.item(selected[0])['values'][0]
        
        # Lấy dữ liệu GỐC từ CSDL (không phải dữ liệu đã format trên cây)
        product_data = self.db.fetch_one("SELECT * FROM SanPham WHERE MaSanPham = %s", (sp_id,))
        
        if product_data:
            self._show_product_dialog(product_data) # Gọi hàm nội bộ với dữ liệu đã tải
        else:
            messagebox.showerror("Lỗi", "Không tìm thấy dữ liệu sản phẩm này.")

    # --- CHỨC NĂNG XÓA ---
    def delete_product(self):
        selected = self.view.product_tree.selection()
        if not selected:
            messagebox.showwarning("Chú ý", "Vui lòng chọn một sản phẩm để xóa.")
            return

        item = self.view.product_tree.item(selected[0])
        sp_id = item['values'][0]
        sp_name = item['values'][1]

        if messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc muốn XÓA VĨNH VIỄN sản phẩm:\n\n{sp_name} (ID: {sp_id})\n\nLưu ý: Hành động này sẽ thất bại nếu sản phẩm đã tồn tại trong hóa đơn hoặc phiếu nhập kho."):
            try:
                # Xóa sản phẩm
                result = self.db.execute_query("DELETE FROM SanPham WHERE MaSanPham = %s", (sp_id,))
                
                if result:
                    messagebox.showinfo("Thành công", f"Đã xóa sản phẩm '{sp_name}'.")
                    self.load_products()
                else:
                    messagebox.showerror("Lỗi", "Xóa thất bại.")
            except Exception as e:
                messagebox.showerror("Lỗi CSDL (Ràng buộc khóa ngoại)", 
                                     f"Không thể xóa sản phẩm: {e}\n\n"
                                     "Điều này thường xảy ra do sản phẩm đã được liên kết với một Hóa Đơn hoặc Phiếu Nhập Kho.")