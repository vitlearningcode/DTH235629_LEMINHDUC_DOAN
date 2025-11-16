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

    def add_to_cart(self):
        """Thêm sản phẩm hoặc phụ tùng vào giỏ"""
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
            
            for cart_item in self.view.cart_items:
                if cart_item['id'] == item_id and cart_item['type'] == item_type:
                    messagebox.showwarning("Thông báo", f"'{name}' đã có trong giỏ hàng.")
                    return

            quantity = tk.simpledialog.askinteger(
                "Số lượng", 
                f"Nhập số lượng cho:\n{name}\n(Tồn kho: {stock})", 
                minvalue=1, 
                maxvalue=stock
            )
            
            if quantity:
                if quantity > stock:
                    messagebox.showwarning("Cảnh báo", "Số lượng vượt quá tồn kho!")
                    return
                
                total = price * quantity
                
                self.view.cart_items.append({
                    'id': item_id,
                    'name': name,
                    'quantity': quantity,
                    'price': price,
                    'total': total,
                    'type': item_type
                })
                
                self.update_cart_display() # Gọi hàm nội bộ
        
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
    
    def process_payment(self):
        """Xử lý thanh toán (Đã cập nhật cho phép Công Nợ)"""
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

            # Thêm chi tiết hóa đơn (giữ nguyên)
            for item in self.view.cart_items:
                if item['type'] == 'SanPham':
                    detail_query = "INSERT INTO ChiTietHoaDonSanPham (MaHoaDon, MaSanPham, SoLuong, DonGia) VALUES (%s, %s, %s, %s)"
                else: # 'PhuTung'
                    detail_query = "INSERT INTO ChiTietHoaDonPhuTung (MaHoaDon, MaPhuTung, SoLuong, DonGia) VALUES (%s, %s, %s, %s)"
                
                params = (invoice_id, item['id'], item['quantity'], item['price'])
                self.db.execute_query(detail_query, params)
            
            messagebox.showinfo("Thành công", f"Tạo hóa đơn thành công!\nMã hóa đơn: {invoice_id}")
            
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