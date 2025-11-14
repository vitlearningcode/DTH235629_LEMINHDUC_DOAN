# main/Function/function_QuanLy/quanly_dashboard_logic.py
from datetime import date

class QuanLyDashboardLogic:
    def __init__(self, view):
        """
        Khởi tạo logic cho Dashboard của Quản lý.
        """
        self.view = view
        self.db = view.db

    def get_dashboard_stats(self):
        """Lấy thống kê tổng quan cho Quản lý (SQL Server Syntax)"""
        stats = {}
        today = date.today().strftime('%Y-%m-%d')

        # 1. Tổng số nhân viên (lấy từ NguoiDung)
        result = self.db.fetch_one("SELECT COUNT(*) as total FROM NguoiDung WHERE VaiTro='NhanVien'")
        stats["Tổng nhân viên"] = result['total'] if result else 0
        
        # 2. Tổng khách hàng (lấy từ KhachHang)
        result = self.db.fetch_one("SELECT COUNT(*) as total FROM KhachHang")
        stats["Tổng khách hàng"] = result['total'] if result else 0
        
        # 3. Chấm công hôm nay (lấy từ ChamCong)
        # Sử dụng tham số ? mà pyodbc yêu cầu
        query_chamcong = "SELECT COUNT(*) as total FROM ChamCong WHERE NgayChamCong = ? AND TrangThai = 'DiLam'"
        result = self.db.fetch_one(query_chamcong, (today,))
        stats["Nhân viên có mặt"] = result['total'] if result else 0
        
        # 4. Doanh thu hôm nay (lấy từ HoaDon, dùng GETDATE() của SQL Server)
        result = self.db.fetch_one("""
            SELECT COALESCE(SUM(TongThanhToan), 0) as total 
            FROM HoaDon 
            WHERE CONVERT(date, NgayLap) = CONVERT(date, GETDATE())
            AND TrangThai != 'Huy'
        """)
        stats["Doanh thu hôm nay"] = f"{result['total']:,.0f} VNĐ" if result else "0 VNĐ"
        
        return stats