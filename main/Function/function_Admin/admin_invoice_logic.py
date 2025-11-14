# main/Function/function_Admin/admin_invoice_logic.py

class AdminInvoiceLogic:
    def __init__(self, view):
        self.view = view
        self.db = view.db

    def load_invoices(self):
        for item in self.view.invoice_tree.get_children(): 
            self.view.invoice_tree.delete(item)
        
        query = """
            SELECT TOP 100 hd.MaHoaDon, kh.HoTen as KhachHang, nd.HoTen as NhanVien,
                   FORMAT(hd.NgayLap, 'dd/MM/yyyy HH:mm') as NgayLap,
                   hd.TongTien, hd.TongThanhToan, hd.TienConNo, hd.TrangThai
            FROM HoaDon hd
            JOIN KhachHang kh ON hd.MaKhachHang = kh.MaKhachHang
            JOIN NguoiDung nd ON hd.MaNguoiDung = nd.MaNguoiDung
            ORDER BY hd.MaHoaDon DESC
        """
        invoices = self.db.fetch_all(query)
        for inv in invoices:
            self.view.invoice_tree.insert("", tk.END, values=(
                inv['MaHoaDon'], inv['KhachHang'], inv['NhanVien'], inv['NgayLap'],
                f"{inv['TongTien']:,.0f}", f"{inv['TongThanhToan']:,.0f}",
                f"{inv['TienConNo']:,.0f}", inv['TrangThai']
            ))