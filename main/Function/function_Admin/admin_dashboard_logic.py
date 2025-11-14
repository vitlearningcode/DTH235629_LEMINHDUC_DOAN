# main/Function/function_Admin/admin_dashboard_logic.py

class AdminDashboardLogic:
    def __init__(self, view):
        self.view = view
        self.db = view.db

    def get_dashboard_stats(self):
        """Lấy thống kê tổng quan (SQL Server Syntax)"""
        stats = {}
        
        result = self.db.fetch_one("SELECT COUNT(*) as total FROM NguoiDung WHERE VaiTro='NhanVien'")
        stats["Tổng nhân viên"] = result['total'] if result else 0
        
        result = self.db.fetch_one("SELECT COUNT(*) as total FROM SanPham")
        stats["Tổng sản phẩm"] = result['total'] if result else 0
        
        result = self.db.fetch_one("SELECT COUNT(*) as total FROM KhachHang")
        stats["Tổng khách hàng"] = result['total'] if result else 0
        
        result = self.db.fetch_one("""
            SELECT COALESCE(SUM(TongThanhToan), 0) as total 
            FROM HoaDon 
            WHERE MONTH(NgayLap) = MONTH(GETDATE()) 
            AND YEAR(NgayLap) = YEAR(GETDATE())
            AND TrangThai != 'Huy'
        """)
        stats["Doanh thu tháng"] = f"{result['total']:,.0f} VNĐ" if result else "0 VNĐ"
        
        return stats