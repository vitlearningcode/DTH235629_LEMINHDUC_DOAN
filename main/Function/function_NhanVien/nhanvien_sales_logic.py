# main/Function/function_NhanVien/nhanvien_sales_logic.py

import tkinter as tk
from tkinter import messagebox, simpledialog

class NhanVienSalesLogic:
    def __init__(self, view):
        self.view = view
        self.db = view.db

    def load_products(self):
        """Tải danh sách sản phẩm còn hàng"""
        for item in self.view.product_tree.get_children():
            self.view.product_tree.delete(item)
        
        query = """
            SELECT sp.MaSanPham, sp.TenSanPham, hx.TenHangXe, sp.GiaBan, sp.SoLuongTon
            FROM SanPham sp
            JOIN HangXe hx ON sp.MaHangXe = hx.MaHangXe
            WHERE sp.TrangThai = 'ConHang' AND sp.SoLuongTon > 0
            ORDER BY sp.TenSanPham
        """
        products = self.db.fetch_all(query)
        
        if products:
            for p in products:
                self.view.product_tree.insert("", tk.END, values=(
                    p['MaSanPham'],
                    p['TenSanPham'],
                    p['TenHangXe'],
                    f"{p['GiaBan']:,.0f}",
                    p['SoLuongTon']
                ))
    
    def load_parts(self):
        """Tải danh sách phụ tùng còn hàng"""
        for item in self.view.part_tree.get_children():
            self.view.part_tree.delete(item)
        
        query = """
            SELECT pt.MaPhuTung, pt.TenPhuTung, lpt.TenLoaiPhuTung, pt.GiaBan, pt.SoLuongTon
            FROM PhuTung pt
            LEFT JOIN LoaiPhuTung lpt ON pt.MaLoaiPhuTung = lpt.MaLoaiPhuTung
            WHERE pt.TrangThai = 'ConHang' AND pt.SoLuongTon > 0
            ORDER BY pt.TenPhuTung
        """
        parts = self.db.fetch_all(query)
        
        if parts:
            for p in parts:
                self.view.part_tree.insert("", tk.END, values=(
                    p['MaPhuTung'],
                    p['TenPhuTung'],
                    p['TenLoaiPhuTung'] or "N/A",
                    f"{p['GiaBan']:,.0f}",
                    p['SoLuongTon']
                ))

    # main/Function/function_NhanVien/nhanvien_sales_logic.py
# (SAO CHÉP VÀ THAY THẾ HÀM NÀY)

    def add_to_cart(self):
        """Thêm sản phẩm hoặc phụ tùng vào giỏ (Đã sửa để CỘNG DỒN số lượng)"""
        try:
            current_tab = self.view.tab_control.index(self.view.tab_control.select())
            
            if current_tab == 0:
                tree = self.view.product_tree
                item_type = 'SanPham'
                selected = tree.selection()
                if not selected:
                    messagebox.showwarning("Cảnh báo", "Vui lòng chọn một SẢN PHẨM (XE MÁY)!")
                    return
            elif current_tab == 1:
                tree = self.view.part_tree
                item_type = 'PhuTung'
                selected = tree.selection()
                if not selected:
                    messagebox.showwarning("Cảnh báo", "Vui lòng chọn một PHỤ TÙNG!")
                    return
            else:
                return

            item = tree.item(selected[0])
            values = item['values']
            
            item_id = values[0]
            name = values[1]
            price = float(values[3].replace(',', ''))
            stock = int(values[4])
            
            # --- BẮT ĐẦU SỬA ĐỔI ---

            # 1. Hỏi số lượng muốn THÊM
            quantity_to_add = tk.simpledialog.askinteger(
                "Số lượng", 
                f"Nhập số lượng MUỐN THÊM cho:\n{name}\n(Tồn kho: {stock})", 
                minvalue=1, 
                maxvalue=stock # Giới hạn tối đa 1 lần thêm là tồn kho
            )
            
            if not quantity_to_add:
                return # Người dùng nhấn Cancel

            # 2. Tìm trong giỏ hàng xem đã có chưa
            for cart_item in self.view.cart_items:
                if cart_item['id'] == item_id and cart_item['type'] == item_type:
                    
                    # --- ĐÃ TÌM THẤY: Cập nhật số lượng ---
                    new_quantity = cart_item['quantity'] + quantity_to_add
                    
                    # Kiểm tra xem tổng số lượng mới có vượt tồn kho không
                    if new_quantity > stock:
                        messagebox.showwarning("Cảnh báo", 
                                             f"Không đủ tồn kho!\n\n"
                                             f"Đã có trong giỏ: {cart_item['quantity']}\n"
                                             f"Muốn thêm: {quantity_to_add}\n"
                                             f"Tổng: {new_quantity} (Vượt tồn kho: {stock})")
                        return
                    
                    # Cập nhật lại giỏ hàng
                    cart_item['quantity'] = new_quantity
                    cart_item['total'] = cart_item['price'] * new_quantity
                    
                    self.update_cart_display() # Cập nhật UI
                    return # --- Thoát hàm sau khi cập nhật
            
            # 3. CHƯA CÓ TRONG GIỎ: Thêm mới (Code này chỉ chạy nếu vòng lặp for ở trên không tìm thấy)
            
            # (Kiểm tra này thực ra đã được thực hiện bởi maxvalue, nhưng để an toàn)
            if quantity_to_add > stock:
                messagebox.showwarning("Cảnh báo", "Số lượng vượt quá tồn kho!")
                return
            
            total = price * quantity_to_add
            
            self.view.cart_items.append({
                'id': item_id,
                'name': name,
                'quantity': quantity_to_add, # Thêm số lượng vừa nhập
                'price': price,
                'total': total,
                'type': item_type
            })
            
            self.update_cart_display() # Cập nhật UI
            
            # --- KẾT THÚC SỬA ĐỔI ---
        
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra khi thêm vào giỏ: {e}")
    
    def remove_from_cart(self):
        """Xóa sản phẩm khỏi giỏ"""
        selected = self.view.cart_tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sản phẩm cần xóa!")
            return
        
        index = self.view.cart_tree.index(selected[0])
        del self.view.cart_items[index]
        self.update_cart_display() # Gọi hàm nội bộ
    
    def update_cart_display(self):
        """Cập nhật hiển thị giỏ hàng (chỉ được gọi bởi các hàm trong lớp này)"""
        for item in self.view.cart_tree.get_children():
            self.view.cart_tree.delete(item)
        
        total = 0
        for item in self.view.cart_items:
            self.view.cart_tree.insert("", tk.END, values=(
                item['name'],
                item['quantity'],
                f"{item['price']:,.0f}",
                f"{item['total']:,.0f}"
            ))
            total += item['total']
        
        self.view.total_label.config(text=f"{total:,.0f} VNĐ")
    
   # main/Function/function_NhanVien/nhanvien_sales_logic.py
# (SAO CHÉP VÀ THAY THẾ TOÀN BỘ HÀM NÀY)

    def process_payment(self):
        """Xử lý thanh toán (Đã cập nhật cho phép Công Nợ VÀ TỰ TẠO BẢO HÀNH)"""
        if not self.view.cart_items:
            messagebox.showwarning("Cảnh báo", "Giỏ hàng trống!")
            return
        
        if not hasattr(self.view, 'current_customer'):
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn khách hàng!")
            return
        
        # Lấy tổng tiền từ giỏ hàng
        total = sum(item['total'] for item in self.view.cart_items)
        
        # Lấy số tiền khách trả từ Entry
        try:
            paid_str = self.view.payment_entry.get().strip()
            if not paid_str:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập số tiền khách trả!")
                return
            
            tien_da_tra = float(paid_str)
            if tien_da_tra < 0:
                raise ValueError("Số tiền không được âm")
            
            if tien_da_tra > total:
                messagebox.showwarning("Cảnh báo", 
                                      f"Số tiền trả ({tien_da_tra:,.0f}) không được lớn hơn số tiền phải trả({total:,.0f})!")
                return
                
        except ValueError:
            messagebox.showerror("Lỗi", "Số tiền khách trả không hợp lệ! Vui lòng chỉ nhập số.")
            return

       # Tự động quyết định trạng thái dựa trên số tiền
        trang_thai = 'DaThanhToan' # Mặc định là đã thanh toán
        
        if tien_da_tra < total:
            # Nếu tiền trả < tổng tiền, ĐỔI trạng thái thành 'ConNo'
            trang_thai = 'ConNo' 
            
            # Hiển thị xác nhận công nợ
            if not messagebox.askyesno("Xác nhận Công Nợ", 
                                       f"Tổng tiền: {total:,.0f} VNĐ\n"
                                       f"Khách trả: {tien_da_tra:,.0f} VNĐ\n"
                                       f"Còn nợ: {(total - tien_da_tra):,.0f} VNĐ\n\n"
                                       f"Hóa đơn này sẽ được ghi nhận là 'Còn Nợ'. Bạn có chắc chắn?"):
                return # Hủy nếu Nhân viên không xác nhận

        # Sửa: Thêm cột TrangThai vào câu query
        query_hd = """
            INSERT INTO HoaDon (MaKhachHang, MaNguoiDung, TongTien, TongThanhToan, TienDaTra, PhuongThucThanhToan, TrangThai)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        try:
            # Sửa: Truyền biến 'trang_thai' vào tham số
            invoice_id = self.db.execute_query(
                query_hd,
                (self.view.current_customer['MaKhachHang'], self.view.user_info['MaNguoiDung'], 
                 total, total, tien_da_tra, 'TienMat', trang_thai) # Thêm 'trang_thai' ở cuối
            )
            
            if not invoice_id:
                messagebox.showerror("Lỗi", "Không thể tạo hóa đơn! (ID trả về null)")
                return

            # --- BẮT ĐẦU SỬA ĐỔI (NHIỆM VỤ 4) ---
            
            # Biến đếm số phiếu bảo hành đã tạo
            total_warranties_created = 0

            # Thêm chi tiết hóa đơn VÀ tạo phiếu bảo hành
            for item in self.view.cart_items:
                if item['type'] == 'SanPham':
                    # 1. Thêm chi tiết hóa đơn sản phẩm
                    detail_query = "INSERT INTO ChiTietHoaDonSanPham (MaHoaDon, MaSanPham, SoLuong, DonGia) VALUES (%s, %s, %s, %s)"
                    params = (invoice_id, item['id'], item['quantity'], item['price'])
                    self.db.execute_query(detail_query, params)
                    
                    # 2. Tự động tạo phiếu bảo hành cho sản phẩm này
                    try:
                        # Lấy thời hạn bảo hành (tính bằng tháng) từ bảng SanPham
                        sp_query = "SELECT ThoiGianBaoHanh FROM SanPham WHERE MaSanPham = %s"
                        product_data = self.db.fetch_one(sp_query, (item['id'],))
                        
                        thoi_gian_bao_hanh = 12 # Mặc định 12 tháng nếu không tìm thấy
                        if product_data and product_data['ThoiGianBaoHanh']:
                            thoi_gian_bao_hanh = int(product_data['ThoiGianBaoHanh'])
                        
                        # Query để tạo phiếu bảo hành
                        query_bh = """
                            INSERT INTO PhieuBaoHanh (MaHoaDon, MaSanPham, MaKhachHang, NgayBatDau, NgayKetThuc, TrangThai)
                            VALUES (%s, %s, %s, GETDATE(), DATEADD(month, %s, GETDATE()), 'ConHieuLuc')
                        """
                        params_bh = (
                            invoice_id,
                            item['id'], # MaSanPham
                            self.view.current_customer['MaKhachHang'],
                            thoi_gian_bao_hanh
                        )
                        
                        # Lặp N lần (N = số lượng xe) để tạo N phiếu bảo hành
                        for _ in range(item['quantity']):
                            self.db.execute_query(query_bh, params_bh)
                            total_warranties_created += 1
                            
                    except Exception as e_bh:
                        # Nếu tạo bảo hành lỗi, không dừng cả quy trình, chỉ thông báo
                        print(f"Lỗi khi tạo phiếu bảo hành cho SP {item['id']}: {e_bh}")
                        messagebox.showwarning("Lỗi Phụ", f"Tạo hóa đơn thành công, NHƯNG tạo phiếu bảo hành cho {item['name']} thất bại.\nLỗi: {e_bh}")
                
                else: # 'PhuTung'
                    # 1. Thêm chi tiết hóa đơn phụ tùng (không tạo bảo hành)
                    detail_query = "INSERT INTO ChiTietHoaDonPhuTung (MaHoaDon, MaPhuTung, SoLuong, DonGia) VALUES (%s, %s, %s, %s)"
                    params = (invoice_id, item['id'], item['quantity'], item['price'])
                    self.db.execute_query(detail_query, params)
            
            # Sửa thông báo thành công
            messagebox.showinfo("Thành công", 
                                f"Tạo hóa đơn thành công! (Mã hóa đơn: {invoice_id})\n"
                                f"Đã tự động tạo {total_warranties_created} phiếu bảo hành cho xe.")
            
            # --- KẾT THÚC SỬA ĐỔI ---

            # Reset
            self.view.cart_items = []
            self.update_cart_display()
            self.view.customer_name_var.set("")
            self.view.phone_entry.delete(0, tk.END)
            self.view.payment_entry.delete(0, tk.END) # Xóa ô nhập tiền
            delattr(self.view, 'current_customer')
            
            # Tải lại danh sách vì tồn kho đã thay đổi
            self.load_products()
            self.load_parts()
        
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tạo hóa đơn! \n(Lỗi trigger hoặc CSDL)\n{e}")
    # (Bạn hãy dán 2 hàm này vào bên trong class NhanVienSalesLogic)

    def update_cart_treeview(self):
        """
        (HÀM MỚI)
        Vẽ lại toàn bộ giỏ hàng (Treeview) từ dữ liệu self.view.cart_items.
        """
        # 1. Xóa tất cả item cũ
        for item in self.view.cart_tree.get_children():
            self.view.cart_tree.delete(item)
        
        # 2. Thêm item mới từ danh sách cart_items
        if not self.view.cart_items:
            return
            
        for item in self.view.cart_items:
            try:
                name = item['name']
                quantity = item['quantity']
                price = item['price']
                total = quantity * price
                
                self.view.cart_tree.insert("", tk.END, values=(
                    name,
                    quantity,
                    f"{price:,.0f}",
                    f"{total:,.0f}"
                ))
            except Exception as e:
                print(f"Lỗi khi thêm item vào cart_tree: {e}")

    def update_total_price(self):
        """
        (HÀM MỚI)
        Tính toán và cập nhật lại nhãn tổng tiền từ self.view.cart_items.
        """
        total = 0
        for item in self.view.cart_items:
            try:
                total += item['quantity'] * item['price']
            except Exception as e:
                print(f"Lỗi khi tính tổng tiền: {e}")
                
        # Cập nhật nhãn total_label trên giao diện
        self.view.total_label.config(text=f"{total:,.0f} VNĐ")        