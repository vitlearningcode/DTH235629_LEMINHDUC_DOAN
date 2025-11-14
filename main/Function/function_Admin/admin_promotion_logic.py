# main/Function/function_Admin/admin_promotion_logic.py

class AdminPromotionLogic:
    def __init__(self, view):
        self.view = view
        self.db = view.db

    def load_promotions(self):
        for item in self.view.promo_tree.get_children(): 
            self.view.promo_tree.delete(item)
        
        query = """
            SELECT MaKhuyenMai, TenKhuyenMai, LoaiKhuyenMai, GiaTri,
                   FORMAT(NgayBatDau, 'dd/MM/yyyy') as NgayBatDau,
                   FORMAT(NgayKetThuc, 'dd/MM/yyyy') as NgayKetThuc,
                   TrangThai
            FROM KhuyenMai
            ORDER BY NgayBatDau DESC
        """
        promos = self.db.fetch_all(query)
        for p in promos:
            value = f"{p['GiaTri']:,.0f}%" if p['LoaiKhuyenMai'] == 'PhanTram' else f"{p['GiaTri']:,.0f} VNĐ"
            self.view.promo_tree.insert("", tk.END, values=(
                p['MaKhuyenMai'], p['TenKhuyenMai'], p['LoaiKhuyenMai'], value, 
                p['NgayBatDau'], p['NgayKetThuc'], p['TrangThai']
            ))