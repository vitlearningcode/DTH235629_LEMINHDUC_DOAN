-- =====================================================
-- HỆ THỐNG QUẢN LÝ CỬA HÀNG XE MÁY
-- Database: QUANLYCUAHANGXEMAY
-- =====================================================

CREATE DATABASE IF NOT EXISTS QUANLYCUAHANGXEMAY;
USE QUANLYCUAHANGXEMAY;

-- =====================================================
-- BẢNG NGƯỜI DÙNG VÀ PHÂN QUYỀN
-- =====================================================

-- Bảng Người Dùng (Users)
CREATE TABLE NguoiDung (
    MaNguoiDung INT PRIMARY KEY AUTO_INCREMENT,
    TenDangNhap VARCHAR(50) UNIQUE NOT NULL,
    MatKhau VARCHAR(255) NOT NULL,
    HoTen NVARCHAR(100) NOT NULL,
    SoDienThoai VARCHAR(15),
    Email VARCHAR(100),
    DiaChi NVARCHAR(255),
    VaiTro ENUM('Admin', 'QuanLy', 'NhanVien') NOT NULL,
    TrangThai ENUM('HoatDong', 'KhongHoatDong') DEFAULT 'HoatDong',
    NgayTao DATETIME DEFAULT CURRENT_TIMESTAMP,
    NgayCapNhat DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- =====================================================
-- BẢNG QUẢN LÝ SẢN PHẨM
-- =====================================================

-- Bảng Loại Xe
CREATE TABLE LoaiXe (
    MaLoaiXe INT PRIMARY KEY AUTO_INCREMENT,
    TenLoaiXe NVARCHAR(100) NOT NULL,
    MoTa NVARCHAR(255)
);

-- Bảng Hãng Xe
CREATE TABLE HangXe (
    MaHangXe INT PRIMARY KEY AUTO_INCREMENT,
    TenHangXe NVARCHAR(100) NOT NULL,
    QuocGia NVARCHAR(50),
    Website VARCHAR(255)
);

-- Bảng Sản Phẩm (Xe)
CREATE TABLE SanPham (
    MaSanPham INT PRIMARY KEY AUTO_INCREMENT,
    TenSanPham NVARCHAR(150) NOT NULL,
    MaLoaiXe INT,
    MaHangXe INT,
    PhanKhoi INT,
    MauSac NVARCHAR(50),
    NamSanXuat INT,
    GiaBan DECIMAL(15, 2) NOT NULL,
    SoLuongTon INT DEFAULT 0,
    MoTa NVARCHAR(500),
    ThoiGianBaoHanh INT DEFAULT 12, -- Tháng
    TrangThai ENUM('ConHang', 'HetHang', 'NgungKinhDoanh') DEFAULT 'ConHang',
    NgayTao DATETIME DEFAULT CURRENT_TIMESTAMP,
    NgayCapNhat DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (MaLoaiXe) REFERENCES LoaiXe(MaLoaiXe),
    FOREIGN KEY (MaHangXe) REFERENCES HangXe(MaHangXe),
    CONSTRAINT CHK_SoLuongTon CHECK (SoLuongTon >= 0),
    CONSTRAINT CHK_GiaBan CHECK (GiaBan > 0)
);

-- =====================================================
-- BẢNG QUẢN LÝ PHỤ TÙNG
-- =====================================================

-- Bảng Loại Phụ Tùng
CREATE TABLE LoaiPhuTung (
    MaLoaiPhuTung INT PRIMARY KEY AUTO_INCREMENT,
    TenLoaiPhuTung NVARCHAR(100) NOT NULL,
    MoTa NVARCHAR(255)
);

-- Bảng Phụ Tùng
CREATE TABLE PhuTung (
    MaPhuTung INT PRIMARY KEY AUTO_INCREMENT,
    TenPhuTung NVARCHAR(150) NOT NULL,
    MaLoaiPhuTung INT,
    DonViTinh NVARCHAR(20) DEFAULT N'Cái',
    GiaNhap DECIMAL(15, 2) NOT NULL,
    GiaBan DECIMAL(15, 2) NOT NULL,
    SoLuongTon INT DEFAULT 0,
    MoTa NVARCHAR(500),
    TrangThai ENUM('ConHang', 'HetHang', 'NgungKinhDoanh') DEFAULT 'ConHang',
    NgayTao DATETIME DEFAULT CURRENT_TIMESTAMP,
    NgayCapNhat DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (MaLoaiPhuTung) REFERENCES LoaiPhuTung(MaLoaiPhuTung),
    CONSTRAINT CHK_PhuTung_SoLuongTon CHECK (SoLuongTon >= 0),
    CONSTRAINT CHK_PhuTung_GiaBan CHECK (GiaBan > 0),
    CONSTRAINT CHK_PhuTung_GiaNhap CHECK (GiaNhap > 0)
);

-- =====================================================
-- BẢNG QUẢN LÝ KHO
-- =====================================================

-- Bảng Nhà Cung Cấp
CREATE TABLE NhaCungCap (
    MaNhaCungCap INT PRIMARY KEY AUTO_INCREMENT,
    TenNhaCungCap NVARCHAR(150) NOT NULL,
    SoDienThoai VARCHAR(15),
    Email VARCHAR(100),
    DiaChi NVARCHAR(255),
    NguoiLienHe NVARCHAR(100),
    TrangThai ENUM('HoatDong', 'NgungHopTac') DEFAULT 'HoatDong',
    NgayTao DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Bảng Phiếu Nhập Kho
CREATE TABLE PhieuNhapKho (
    MaPhieuNhap INT PRIMARY KEY AUTO_INCREMENT,
    MaNhaCungCap INT,
    MaNguoiDung INT, -- Người tạo phiếu
    NgayNhap DATETIME DEFAULT CURRENT_TIMESTAMP,
    TongTien DECIMAL(15, 2) DEFAULT 0,
    TrangThai ENUM('ChoXacNhan', 'DaXacNhan', 'Huy') DEFAULT 'ChoXacNhan',
    GhiChu NVARCHAR(500),
    FOREIGN KEY (MaNhaCungCap) REFERENCES NhaCungCap(MaNhaCungCap),
    FOREIGN KEY (MaNguoiDung) REFERENCES NguoiDung(MaNguoiDung)
);

-- Bảng Chi Tiết Phiếu Nhập Kho (Sản Phẩm)
CREATE TABLE ChiTietPhieuNhapSanPham (
    MaChiTiet INT PRIMARY KEY AUTO_INCREMENT,
    MaPhieuNhap INT,
    MaSanPham INT,
    SoLuong INT NOT NULL,
    DonGia DECIMAL(15, 2) NOT NULL,
    ThanhTien DECIMAL(15, 2) AS (SoLuong * DonGia) STORED,
    FOREIGN KEY (MaPhieuNhap) REFERENCES PhieuNhapKho(MaPhieuNhap),
    FOREIGN KEY (MaSanPham) REFERENCES SanPham(MaSanPham),
    CONSTRAINT CHK_CTPN_SoLuong CHECK (SoLuong > 0)
);

-- Bảng Chi Tiết Phiếu Nhập Kho (Phụ Tùng)
CREATE TABLE ChiTietPhieuNhapPhuTung (
    MaChiTiet INT PRIMARY KEY AUTO_INCREMENT,
    MaPhieuNhap INT,
    MaPhuTung INT,
    SoLuong INT NOT NULL,
    DonGia DECIMAL(15, 2) NOT NULL,
    ThanhTien DECIMAL(15, 2) AS (SoLuong * DonGia) STORED,
    FOREIGN KEY (MaPhieuNhap) REFERENCES PhieuNhapKho(MaPhieuNhap),
    FOREIGN KEY (MaPhuTung) REFERENCES PhuTung(MaPhuTung),
    CONSTRAINT CHK_CTPNPT_SoLuong CHECK (SoLuong > 0)
);

-- =====================================================
-- BẢNG QUẢN LÝ KHÁCH HÀNG
-- =====================================================

-- Bảng Khách Hàng
CREATE TABLE KhachHang (
    MaKhachHang INT PRIMARY KEY AUTO_INCREMENT,
    HoTen NVARCHAR(100) NOT NULL,
    SoDienThoai VARCHAR(15) NOT NULL,
    Email VARCHAR(100),
    DiaChi NVARCHAR(255),
    CMND VARCHAR(20),
    NgaySinh DATE,
    GioiTinh ENUM('Nam', 'Nu', 'Khac'),
    LoaiKhachHang ENUM('ThanThiet', 'TiemNang', 'ThongThuong') DEFAULT 'ThongThuong',
    NgayTao DATETIME DEFAULT CURRENT_TIMESTAMP,
    NgayCapNhat DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- =====================================================
-- BẢNG KHUYẾN MÃI
-- =====================================================

-- Bảng Khuyến Mãi
CREATE TABLE KhuyenMai (
    MaKhuyenMai INT PRIMARY KEY AUTO_INCREMENT,
    TenKhuyenMai NVARCHAR(150) NOT NULL,
    LoaiKhuyenMai ENUM('PhanTram', 'TienMat') NOT NULL,
    GiaTri DECIMAL(15, 2) NOT NULL,
    NgayBatDau DATE NOT NULL,
    NgayKetThuc DATE NOT NULL,
    DieuKien NVARCHAR(500), -- Điều kiện áp dụng
    TrangThai ENUM('HoatDong', 'KhongHoatDong') DEFAULT 'HoatDong',
    NgayTao DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT CHK_NgayKhuyenMai CHECK (NgayKetThuc >= NgayBatDau)
);

-- =====================================================
-- BẢNG HÓA ĐƠN BÁN HÀNG
-- =====================================================

-- Bảng Hóa Đơn
CREATE TABLE HoaDon (
    MaHoaDon INT PRIMARY KEY AUTO_INCREMENT,
    MaKhachHang INT,
    MaNguoiDung INT, -- Nhân viên lập hóa đơn
    NgayLap DATETIME DEFAULT CURRENT_TIMESTAMP,
    TongTien DECIMAL(15, 2) DEFAULT 0,
    TienKhuyenMai DECIMAL(15, 2) DEFAULT 0,
    TongThanhToan DECIMAL(15, 2) DEFAULT 0,
    TienDaTra DECIMAL(15, 2) DEFAULT 0,
    TienConNo DECIMAL(15, 2) AS (TongThanhToan - TienDaTra) STORED,
    MaKhuyenMai INT,
    PhuongThucThanhToan ENUM('TienMat', 'ChuyenKhoan', 'TraGop') DEFAULT 'TienMat',
    TrangThai ENUM('ChoXuLy', 'DaThanhToan', 'ConNo', 'Huy') DEFAULT 'ChoXuLy',
    GhiChu NVARCHAR(500),
    FOREIGN KEY (MaKhachHang) REFERENCES KhachHang(MaKhachHang),
    FOREIGN KEY (MaNguoiDung) REFERENCES NguoiDung(MaNguoiDung),
    FOREIGN KEY (MaKhuyenMai) REFERENCES KhuyenMai(MaKhuyenMai)
);

-- Bảng Chi Tiết Hóa Đơn (Sản Phẩm)
CREATE TABLE ChiTietHoaDonSanPham (
    MaChiTiet INT PRIMARY KEY AUTO_INCREMENT,
    MaHoaDon INT,
    MaSanPham INT,
    SoLuong INT NOT NULL,
    DonGia DECIMAL(15, 2) NOT NULL,
    ThanhTien DECIMAL(15, 2) AS (SoLuong * DonGia) STORED,
    FOREIGN KEY (MaHoaDon) REFERENCES HoaDon(MaHoaDon),
    FOREIGN KEY (MaSanPham) REFERENCES SanPham(MaSanPham),
    CONSTRAINT CHK_CTHD_SoLuong CHECK (SoLuong > 0)
);

-- Bảng Chi Tiết Hóa Đơn (Phụ Tùng và Dịch Vụ Sửa Chữa)
CREATE TABLE ChiTietHoaDonPhuTung (
    MaChiTiet INT PRIMARY KEY AUTO_INCREMENT,
    MaHoaDon INT,
    MaPhuTung INT,
    SoLuong INT NOT NULL,
    DonGia DECIMAL(15, 2) NOT NULL,
    ThanhTien DECIMAL(15, 2) AS (SoLuong * DonGia) STORED,
    FOREIGN KEY (MaHoaDon) REFERENCES HoaDon(MaHoaDon),
    FOREIGN KEY (MaPhuTung) REFERENCES PhuTung(MaPhuTung),
    CONSTRAINT CHK_CTHDPT_SoLuong CHECK (SoLuong > 0)
);

-- =====================================================
-- BẢNG BẢO HÀNH
-- =====================================================

-- Bảng Phiếu Bảo Hành
CREATE TABLE PhieuBaoHanh (
    MaPhieuBaoHanh INT PRIMARY KEY AUTO_INCREMENT,
    MaHoaDon INT,
    MaSanPham INT,
    MaKhachHang INT,
    NgayBatDau DATE NOT NULL,
    NgayKetThuc DATE NOT NULL,
    TrangThai ENUM('ConHieuLuc', 'HetHieuLuc', 'DaSuDung') DEFAULT 'ConHieuLuc',
    GhiChu NVARCHAR(500),
    NgayTao DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (MaHoaDon) REFERENCES HoaDon(MaHoaDon),
    FOREIGN KEY (MaSanPham) REFERENCES SanPham(MaSanPham),
    FOREIGN KEY (MaKhachHang) REFERENCES KhachHang(MaKhachHang),
    CONSTRAINT CHK_NgayBaoHanh CHECK (NgayKetThuc > NgayBatDau)
);

-- Bảng Lịch Sử Bảo Hành
CREATE TABLE LichSuBaoHanh (
    MaLichSu INT PRIMARY KEY AUTO_INCREMENT,
    MaPhieuBaoHanh INT,
    NgaySuaChua DATE NOT NULL,
    MoTaLoi NVARCHAR(500),
    ChiPhiPhatSinh DECIMAL(15, 2) DEFAULT 0,
    NguoiXuLy INT, -- Mã nhân viên
    TrangThai ENUM('DangXuLy', 'HoanThanh') DEFAULT 'DangXuLy',
    GhiChu NVARCHAR(500),
    NgayTao DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (MaPhieuBaoHanh) REFERENCES PhieuBaoHanh(MaPhieuBaoHanh),
    FOREIGN KEY (NguoiXuLy) REFERENCES NguoiDung(MaNguoiDung)
);

-- =====================================================
-- BẢNG CHẤM CÔNG
-- =====================================================

-- Bảng Chấm Công
CREATE TABLE ChamCong (
    MaChamCong INT PRIMARY KEY AUTO_INCREMENT,
    MaNguoiDung INT,
    NgayChamCong DATE NOT NULL,
    GioVao TIME,
    GioRa TIME,
    SoGioLam DECIMAL(5, 2),
    TrangThai ENUM('DiLam', 'VangMat', 'NghiPhep', 'DiTre') DEFAULT 'DiLam',
    GhiChu NVARCHAR(255),
    NguoiChamCong INT, -- Quản lý chấm công
    NgayTao DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (MaNguoiDung) REFERENCES NguoiDung(MaNguoiDung),
    FOREIGN KEY (NguoiChamCong) REFERENCES NguoiDung(MaNguoiDung),
    UNIQUE KEY unique_chamcong (MaNguoiDung, NgayChamCong)
);

-- =====================================================
-- TRIGGERS ĐỂ TỰ ĐỘNG CẬP NHẬT
-- =====================================================

-- Trigger: Cập nhật tồn kho khi nhập hàng (Sản phẩm)
DELIMITER //
CREATE TRIGGER after_insert_nhapsanpham
AFTER INSERT ON ChiTietPhieuNhapSanPham
FOR EACH ROW
BEGIN
    UPDATE SanPham 
    SET SoLuongTon = SoLuongTon + NEW.SoLuong
    WHERE MaSanPham = NEW.MaSanPham;
END//
DELIMITER ;

-- Trigger: Cập nhật tồn kho khi nhập hàng (Phụ tùng)
DELIMITER //
CREATE TRIGGER after_insert_nhapphutung
AFTER INSERT ON ChiTietPhieuNhapPhuTung
FOR EACH ROW
BEGIN
    UPDATE PhuTung 
    SET SoLuongTon = SoLuongTon + NEW.SoLuong
    WHERE MaPhuTung = NEW.MaPhuTung;
END//
DELIMITER ;

-- Trigger: Kiểm tra và giảm tồn kho khi bán hàng (Sản phẩm)
DELIMITER //
CREATE TRIGGER before_insert_bansanpham
BEFORE INSERT ON ChiTietHoaDonSanPham
FOR EACH ROW
BEGIN
    DECLARE ton_kho INT;
    SELECT SoLuongTon INTO ton_kho FROM SanPham WHERE MaSanPham = NEW.MaSanPham;
    
    IF ton_kho < NEW.SoLuong THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Số lượng tồn kho không đủ để bán!';
    END IF;
    
    UPDATE SanPham 
    SET SoLuongTon = SoLuongTon - NEW.SoLuong
    WHERE MaSanPham = NEW.MaSanPham;
END//
DELIMITER ;

-- Trigger: Kiểm tra và giảm tồn kho khi bán phụ tùng
DELIMITER //
CREATE TRIGGER before_insert_banphutung
BEFORE INSERT ON ChiTietHoaDonPhuTung
FOR EACH ROW
BEGIN
    DECLARE ton_kho INT;
    SELECT SoLuongTon INTO ton_kho FROM PhuTung WHERE MaPhuTung = NEW.MaPhuTung;
    
    IF ton_kho < NEW.SoLuong THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Số lượng phụ tùng tồn kho không đủ!';
    END IF;
    
    UPDATE PhuTung 
    SET SoLuongTon = SoLuongTon - NEW.SoLuong
    WHERE MaPhuTung = NEW.MaPhuTung;
END//
DELIMITER ;

-- Trigger: Tự động tính tổng tiền phiếu nhập
DELIMITER //
CREATE TRIGGER after_insert_chitiet_phieunhap
AFTER INSERT ON ChiTietPhieuNhapSanPham
FOR EACH ROW
BEGIN
    UPDATE PhieuNhapKho
    SET TongTien = (
        SELECT COALESCE(SUM(ThanhTien), 0) 
        FROM ChiTietPhieuNhapSanPham 
        WHERE MaPhieuNhap = NEW.MaPhieuNhap
    ) + (
        SELECT COALESCE(SUM(ThanhTien), 0) 
        FROM ChiTietPhieuNhapPhuTung 
        WHERE MaPhieuNhap = NEW.MaPhieuNhap
    )
    WHERE MaPhieuNhap = NEW.MaPhieuNhap;
END//
DELIMITER ;

-- Trigger: Tự động tính tổng tiền hóa đơn
DELIMITER //
CREATE TRIGGER after_insert_chitiet_hoadon
AFTER INSERT ON ChiTietHoaDonSanPham
FOR EACH ROW
BEGIN
    UPDATE HoaDon
    SET TongTien = (
        SELECT COALESCE(SUM(ThanhTien), 0) 
        FROM ChiTietHoaDonSanPham 
        WHERE MaHoaDon = NEW.MaHoaDon
    ) + (
        SELECT COALESCE(SUM(ThanhTien), 0) 
        FROM ChiTietHoaDonPhuTung 
        WHERE MaHoaDon = NEW.MaHoaDon
    )
    WHERE MaHoaDon = NEW.MaHoaDon;
    
    -- Tính tổng thanh toán sau khuyến mãi
    UPDATE HoaDon
    SET TongThanhToan = TongTien - TienKhuyenMai
    WHERE MaHoaDon = NEW.MaHoaDon;
END//
DELIMITER ;

-- =====================================================
-- DỮ LIỆU MẪU
-- =====================================================

-- Thêm người dùng mặc định
INSERT INTO NguoiDung (TenDangNhap, MatKhau, HoTen, SoDienThoai, Email, VaiTro) VALUES
('admin', '123456', N'Nguyễn Văn Admin', '0901234567', 'admin@cuahangxe.com', 'Admin'),
('quanly01', '123456', N'Trần Thị Quản Lý', '0902345678', 'quanly@cuahangxe.com', 'QuanLy'),
('nhanvien01', '123456', N'Lê Văn Nhân Viên', '0903456789', 'nhanvien@cuahangxe.com', 'NhanVien');

-- Thêm Loại Xe
INSERT INTO LoaiXe (TenLoaiXe, MoTa) VALUES
(N'Xe Số', N'Xe số tay truyền thống'),
(N'Xe Tay Ga', N'Xe tay ga tự động'),
(N'Xe Côn Tay', N'Xe côn tay thể thao');

-- Thêm Hãng Xe
INSERT INTO HangXe (TenHangXe, QuocGia, Website) VALUES
(N'Honda', N'Nhật Bản', 'www.honda.com.vn'),
(N'Yamaha', N'Nhật Bản', 'www.yamaha-motor.com.vn'),
(N'SYM', N'Đài Loan', 'www.sym.com.vn');

-- Thêm Sản Phẩm
INSERT INTO SanPham (TenSanPham, MaLoaiXe, MaHangXe, PhanKhoi, MauSac, NamSanXuat, GiaBan, SoLuongTon) VALUES
(N'Honda Vision 2024', 2, 1, 125, N'Đỏ', 2024, 30000000, 10),
(N'Honda Future 2024', 1, 1, 125, N'Đen', 2024, 28000000, 15),
(N'Yamaha Exciter 155', 3, 2, 155, N'Xanh', 2024, 47000000, 8),
(N'Yamaha Sirius', 1, 2, 110, N'Đen', 2024, 21000000, 20);

-- Thêm Loại Phụ Tùng
INSERT INTO LoaiPhuTung (TenLoaiPhuTung, MoTa) VALUES
(N'Nhớt', N'Dầu nhớt xe máy'),
(N'Lốp xe', N'Lốp xe các loại'),
(N'Phanh', N'Hệ thống phanh'),
(N'Đèn', N'Đèn chiếu sáng');

-- Thêm Phụ Tùng
INSERT INTO PhuTung (TenPhuTung, MaLoaiPhuTung, DonViTinh, GiaNhap, GiaBan, SoLuongTon) VALUES
(N'Nhớt Castrol 10W40', 1, N'Chai', 80000, 120000, 50),
(N'Lốp Michelin 80/90-17', 2, N'Cái', 250000, 350000, 30),
(N'Má phanh Honda', 3, N'Bộ', 80000, 150000, 40),
(N'Đèn LED H4', 4, N'Cái', 150000, 250000, 25);

-- Thêm Nhà Cung Cấp
INSERT INTO NhaCungCap (TenNhaCungCap, SoDienThoai, Email, DiaChi, NguoiLienHe) VALUES
(N'Công ty Honda Việt Nam', '0281234567', 'contact@honda.vn', N'TP. Hồ Chí Minh', N'Nguyễn Văn A'),
(N'Yamaha Motor Việt Nam', '0281234568', 'info@yamaha.vn', N'Hà Nội', N'Trần Thị B');

-- Thêm Khách Hàng Mẫu
INSERT INTO KhachHang (HoTen, SoDienThoai, Email, DiaChi, CMND, GioiTinh) VALUES
(N'Phạm Văn Khách', '0912345678', 'khach1@gmail.com', N'123 Đường ABC, Quận 1, TP.HCM', '123456789', 'Nam'),
(N'Nguyễn Thị Lan', '0923456789', 'lan@gmail.com', N'456 Đường XYZ, Quận 2, TP.HCM', '987654321', 'Nu');

-- =====================================================
-- CÁC STORED PROCEDURES HỮU ÍCH
-- =====================================================

-- Procedure: Lấy thông tin tồn kho sản phẩm
DELIMITER //
CREATE PROCEDURE sp_ThongKeTonKhoSanPham()
BEGIN
    SELECT 
        sp.MaSanPham,
        sp.TenSanPham,
        hx.TenHangXe,
        lx.TenLoaiXe,
        sp.SoLuongTon,
        sp.GiaBan,
        (sp.SoLuongTon * sp.GiaBan) AS GiaTriTonKho,
        sp.TrangThai
    FROM SanPham sp
    JOIN HangXe hx ON sp.MaHangXe = hx.MaHangXe
    JOIN LoaiXe lx ON sp.MaLoaiXe = lx.MaLoaiXe
    ORDER BY sp.SoLuongTon ASC;
END//
DELIMITER ;

-- Procedure: Thống kê doanh thu theo tháng
DELIMITER //
CREATE PROCEDURE sp_ThongKeDoanhThuTheoThang(IN nam INT, IN thang INT)
BEGIN
    SELECT 
        DATE(NgayLap) AS Ngay,
        COUNT(*) AS SoHoaDon,
        SUM(TongThanhToan) AS DoanhThu,
        SUM(TienKhuyenMai) AS TongKhuyenMai
    FROM HoaDon
    WHERE YEAR(NgayLap) = nam 
        AND MONTH(NgayLap) = thang
        AND TrangThai != 'Huy'
    GROUP BY DATE(NgayLap)
    ORDER BY Ngay;
END//
DELIMITER ;

-- Procedure: Lấy danh sách sản phẩm sắp hết hàng
DELIMITER //
CREATE PROCEDURE sp_SanPhamSapHetHang(IN nguong INT)
BEGIN
    SELECT 
        sp.MaSanPham,
        sp.TenSanPham,
        hx.TenHangXe,
        sp.SoLuongTon,
        sp.GiaBan
    FROM SanPham sp
    JOIN HangXe hx ON sp.MaHangXe = hx.MaHangXe
    WHERE sp.SoLuongTon <= nguong
        AND sp.TrangThai = 'ConHang'
    ORDER BY sp.SoLuongTon ASC;
END//
DELIMITER ;

-- =====================================================
-- VIEW HỮU ÍCH
-- =====================================================

-- View: Thông tin chi tiết hóa đơn
CREATE VIEW v_ChiTietHoaDon AS
SELECT 
    hd.MaHoaDon,
    hd.NgayLap,
    kh.HoTen AS TenKhachHang,
    kh.SoDienThoai,
    nd.HoTen AS NhanVienLap,
    hd.TongTien,
    hd.TienKhuyenMai,
    hd.TongThanhToan,
    hd.TienDaTra,
    hd.TienConNo,
    hd.PhuongThucThanhToan,
    hd.TrangThai
FROM HoaDon hd
JOIN KhachHang kh ON hd.MaKhachHang = kh.MaKhachHang
JOIN NguoiDung nd ON hd.MaNguoiDung = nd.MaNguoiDung;

-- View: Thống kê nhân viên
CREATE VIEW v_ThongKeNhanVien AS
SELECT 
    nd.MaNguoiDung,
    nd.HoTen,
    nd.VaiTro,
    COUNT(DISTINCT hd.MaHoaDon) AS SoHoaDonLap,
    COALESCE(SUM(hd.TongThanhToan), 0) AS TongDoanhThu,
    COUNT(DISTINCT cc.MaChamCong) AS SoNgayLam
FROM NguoiDung nd
LEFT JOIN HoaDon hd ON nd.MaNguoiDung = hd.MaNguoiDung
LEFT JOIN ChamCong cc ON nd.MaNguoiDung = cc.MaNguoiDung AND cc.TrangThai = 'DiLam'
WHERE nd.VaiTro = 'NhanVien'
GROUP BY nd.MaNguoiDung;

-- =====================================================
-- INDEXES ĐỂ TỐI ƯU HIỆU SUẤT
-- =====================================================

CREATE INDEX idx_sanpham_loai ON SanPham(MaLoaiXe);
CREATE INDEX idx_sanpham_hang ON SanPham(MaHangXe);
CREATE INDEX idx_hoadon_khachhang ON HoaDon(MaKhachHang);
CREATE INDEX idx_hoadon_ngaylap ON HoaDon(NgayLap);
CREATE INDEX idx_chamcong_ngay ON ChamCong(NgayChamCong);
CREATE INDEX idx_phieubaohanh_khachhang ON PhieuBaoHanh(MaKhachHang);

-- =====================================================
-- KẾT THÚC SCRIPT
-- =====================================================
