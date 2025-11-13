-- =====================================================
-- HỆ THỐNG QUẢN LÝ CỬA HÀNG XE MÁY
-- Database: QUANLYCUAHANGXEMAY (SQL Server Version)
-- =====================================================

USE master;
GO

IF NOT EXISTS (SELECT	 * FROM sys.databases WHERE name = 'QUANLYCUAHANGXEMAY')
BEGIN
    CREATE DATABASE QUANLYCUAHANGXEMAY;
END
GO

USE QUANLYCUAHANGXEMAY;
GO

-- =====================================================
-- BẢNG NGƯỜI DÙNG VÀ PHÂN QUYỀN
-- =====================================================

CREATE TABLE NguoiDung (
    MaNguoiDung INT PRIMARY KEY IDENTITY(1,1),
    TenDangNhap VARCHAR(50) UNIQUE NOT NULL,
    MatKhau VARCHAR(255) NOT NULL,
    HoTen NVARCHAR(100) NOT NULL,
    SoDienThoai VARCHAR(15),
    Email VARCHAR(100),
    DiaChi NVARCHAR(255),
    VaiTro VARCHAR(20) NOT NULL CHECK (VaiTro IN ('Admin', 'QuanLy', 'NhanVien')),
    TrangThai VARCHAR(20) DEFAULT 'HoatDong' CHECK (TrangThai IN ('HoatDong', 'KhongHoatDong')),
    NgayTao DATETIME DEFAULT GETDATE(),
    NgayCapNhat DATETIME DEFAULT GETDATE()
);
GO

-- =====================================================
-- BẢNG QUẢN LÝ SẢN PHẨM
-- =====================================================

CREATE TABLE LoaiXe (
    MaLoaiXe INT PRIMARY KEY IDENTITY(1,1),
    TenLoaiXe NVARCHAR(100) NOT NULL,
    MoTa NVARCHAR(255)
);
GO

CREATE TABLE HangXe (
    MaHangXe INT PRIMARY KEY IDENTITY(1,1),
    TenHangXe NVARCHAR(100) NOT NULL,
    QuocGia NVARCHAR(50),
    Website VARCHAR(255)
);
GO

CREATE TABLE SanPham (
    MaSanPham INT PRIMARY KEY IDENTITY(1,1),
    TenSanPham NVARCHAR(150) NOT NULL,
    MaLoaiXe INT,
    MaHangXe INT,
    PhanKhoi INT,
    MauSac NVARCHAR(50),
    NamSanXuat INT,
    GiaBan DECIMAL(15, 2) NOT NULL,
    SoLuongTon INT DEFAULT 0,
    MoTa NVARCHAR(500),
    ThoiGianBaoHanh INT DEFAULT 12,
    TrangThai VARCHAR(20) DEFAULT 'ConHang' CHECK (TrangThai IN ('ConHang', 'HetHang', 'NgungKinhDoanh')),
    NgayTao DATETIME DEFAULT GETDATE(),
    NgayCapNhat DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (MaLoaiXe) REFERENCES LoaiXe(MaLoaiXe),
    FOREIGN KEY (MaHangXe) REFERENCES HangXe(MaHangXe),
    CONSTRAINT CHK_SoLuongTon CHECK (SoLuongTon >= 0),
    CONSTRAINT CHK_GiaBan CHECK (GiaBan > 0)
);
GO

-- =====================================================
-- BẢNG QUẢN LÝ PHỤ TÙNG
-- =====================================================

CREATE TABLE LoaiPhuTung (
    MaLoaiPhuTung INT PRIMARY KEY IDENTITY(1,1),
    TenLoaiPhuTung NVARCHAR(100) NOT NULL,
    MoTa NVARCHAR(255)
);
GO

CREATE TABLE PhuTung (
    MaPhuTung INT PRIMARY KEY IDENTITY(1,1),
    TenPhuTung NVARCHAR(150) NOT NULL,
    MaLoaiPhuTung INT,
    DonViTinh NVARCHAR(20) DEFAULT N'Cái',
    GiaNhap DECIMAL(15, 2) NOT NULL,
    GiaBan DECIMAL(15, 2) NOT NULL,
    SoLuongTon INT DEFAULT 0,
    MoTa NVARCHAR(500),
    TrangThai VARCHAR(20) DEFAULT 'ConHang' CHECK (TrangThai IN ('ConHang', 'HetHang', 'NgungKinhDoanh')),
    NgayTao DATETIME DEFAULT GETDATE(),
    NgayCapNhat DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (MaLoaiPhuTung) REFERENCES LoaiPhuTung(MaLoaiPhuTung),
    CONSTRAINT CHK_PhuTung_SoLuongTon CHECK (SoLuongTon >= 0),
    CONSTRAINT CHK_PhuTung_GiaBan CHECK (GiaBan > 0),
    CONSTRAINT CHK_PhuTung_GiaNhap CHECK (GiaNhap > 0)
);
GO

-- =====================================================
-- BẢNG QUẢN LÝ KHO
-- =====================================================

CREATE TABLE NhaCungCap (
    MaNhaCungCap INT PRIMARY KEY IDENTITY(1,1),
    TenNhaCungCap NVARCHAR(150) NOT NULL,
    SoDienThoai VARCHAR(15),
    Email VARCHAR(100),
    DiaChi NVARCHAR(255),
    NguoiLienHe NVARCHAR(100),
    TrangThai VARCHAR(20) DEFAULT 'HoatDong' CHECK (TrangThai IN ('HoatDong', 'NgungHopTac')),
    NgayTao DATETIME DEFAULT GETDATE()
);
GO

CREATE TABLE PhieuNhapKho (
    MaPhieuNhap INT PRIMARY KEY IDENTITY(1,1),
    MaNhaCungCap INT,
    MaNguoiDung INT,
    NgayNhap DATETIME DEFAULT GETDATE(),
    TongTien DECIMAL(15, 2) DEFAULT 0,
    TrangThai VARCHAR(20) DEFAULT 'ChoXacNhan' CHECK (TrangThai IN ('ChoXacNhan', 'DaXacNhan', 'Huy')),
    GhiChu NVARCHAR(500),
    FOREIGN KEY (MaNhaCungCap) REFERENCES NhaCungCap(MaNhaCungCap),
    FOREIGN KEY (MaNguoiDung) REFERENCES NguoiDung(MaNguoiDung)
);
GO

CREATE TABLE ChiTietPhieuNhapSanPham (
    MaChiTiet INT PRIMARY KEY IDENTITY(1,1),
    MaPhieuNhap INT,
    MaSanPham INT,
    SoLuong INT NOT NULL,
    DonGia DECIMAL(15, 2) NOT NULL,
    ThanhTien AS (SoLuong * DonGia), -- Computed Column
    FOREIGN KEY (MaPhieuNhap) REFERENCES PhieuNhapKho(MaPhieuNhap),
    FOREIGN KEY (MaSanPham) REFERENCES SanPham(MaSanPham),
    CONSTRAINT CHK_CTPN_SoLuong CHECK (SoLuong > 0)
);
GO

CREATE TABLE ChiTietPhieuNhapPhuTung (
    MaChiTiet INT PRIMARY KEY IDENTITY(1,1),
    MaPhieuNhap INT,
    MaPhuTung INT,
    SoLuong INT NOT NULL,
    DonGia DECIMAL(15, 2) NOT NULL,
    ThanhTien AS (SoLuong * DonGia), -- Computed Column
    FOREIGN KEY (MaPhieuNhap) REFERENCES PhieuNhapKho(MaPhieuNhap),
    FOREIGN KEY (MaPhuTung) REFERENCES PhuTung(MaPhuTung),
    CONSTRAINT CHK_CTPNPT_SoLuong CHECK (SoLuong > 0)
);
GO

-- =====================================================
-- BẢNG QUẢN LÝ KHÁCH HÀNG
-- =====================================================

CREATE TABLE KhachHang (
    MaKhachHang INT PRIMARY KEY IDENTITY(1,1),
    HoTen NVARCHAR(100) NOT NULL,
    SoDienThoai VARCHAR(15) NOT NULL,
    Email VARCHAR(100),
    DiaChi NVARCHAR(255),
    CMND VARCHAR(20),
    NgaySinh DATE,
    GioiTinh VARCHAR(10) CHECK (GioiTinh IN ('Nam', 'Nu', 'Khac')),
    LoaiKhachHang VARCHAR(20) DEFAULT 'ThongThuong' CHECK (LoaiKhachHang IN ('ThanThiet', 'TiemNang', 'ThongThuong')),
    NgayTao DATETIME DEFAULT GETDATE(),
    NgayCapNhat DATETIME DEFAULT GETDATE()
);
GO

-- =====================================================
-- BẢNG KHUYẾN MÃI
-- =====================================================

CREATE TABLE KhuyenMai (
    MaKhuyenMai INT PRIMARY KEY IDENTITY(1,1),
    TenKhuyenMai NVARCHAR(150) NOT NULL,
    LoaiKhuyenMai VARCHAR(20) NOT NULL CHECK (LoaiKhuyenMai IN ('PhanTram', 'TienMat')),
    GiaTri DECIMAL(15, 2) NOT NULL,
    NgayBatDau DATE NOT NULL,
    NgayKetThuc DATE NOT NULL,
    DieuKien NVARCHAR(500),
    TrangThai VARCHAR(20) DEFAULT 'HoatDong' CHECK (TrangThai IN ('HoatDong', 'KhongHoatDong')),
    NgayTao DATETIME DEFAULT GETDATE(),
    CONSTRAINT CHK_NgayKhuyenMai CHECK (NgayKetThuc >= NgayBatDau)
);
GO

-- =====================================================
-- BẢNG HÓA ĐƠN BÁN HÀNG
-- =====================================================

CREATE TABLE HoaDon (
    MaHoaDon INT PRIMARY KEY IDENTITY(1,1),
    MaKhachHang INT,
    MaNguoiDung INT,
    NgayLap DATETIME DEFAULT GETDATE(),
    TongTien DECIMAL(15, 2) DEFAULT 0,
    TienKhuyenMai DECIMAL(15, 2) DEFAULT 0,
    TongThanhToan DECIMAL(15, 2) DEFAULT 0,
    TienDaTra DECIMAL(15, 2) DEFAULT 0,
    TienConNo AS (TongThanhToan - TienDaTra),
    MaKhuyenMai INT,
    PhuongThucThanhToan VARCHAR(20) DEFAULT 'TienMat' CHECK (PhuongThucThanhToan IN ('TienMat', 'ChuyenKhoan', 'TraGop')),
    TrangThai VARCHAR(20) DEFAULT 'ChoXuLy' CHECK (TrangThai IN ('ChoXuLy', 'DaThanhToan', 'ConNo', 'Huy')),
    GhiChu NVARCHAR(500),
    FOREIGN KEY (MaKhachHang) REFERENCES KhachHang(MaKhachHang),
    FOREIGN KEY (MaNguoiDung) REFERENCES NguoiDung(MaNguoiDung),
    FOREIGN KEY (MaKhuyenMai) REFERENCES KhuyenMai(MaKhuyenMai)
);
GO

CREATE TABLE ChiTietHoaDonSanPham (
    MaChiTiet INT PRIMARY KEY IDENTITY(1,1),
    MaHoaDon INT,
    MaSanPham INT,
    SoLuong INT NOT NULL,
    DonGia DECIMAL(15, 2) NOT NULL,
    ThanhTien AS (SoLuong * DonGia),
    FOREIGN KEY (MaHoaDon) REFERENCES HoaDon(MaHoaDon),
    FOREIGN KEY (MaSanPham) REFERENCES SanPham(MaSanPham),
    CONSTRAINT CHK_CTHD_SoLuong CHECK (SoLuong > 0)
);
GO

CREATE TABLE ChiTietHoaDonPhuTung (
    MaChiTiet INT PRIMARY KEY IDENTITY(1,1),
    MaHoaDon INT,
    MaPhuTung INT,
    SoLuong INT NOT NULL,
    DonGia DECIMAL(15, 2) NOT NULL,
    ThanhTien AS (SoLuong * DonGia),
    FOREIGN KEY (MaHoaDon) REFERENCES HoaDon(MaHoaDon),
    FOREIGN KEY (MaPhuTung) REFERENCES PhuTung(MaPhuTung),
    CONSTRAINT CHK_CTHDPT_SoLuong CHECK (SoLuong > 0)
);
GO

-- =====================================================
-- BẢNG BẢO HÀNH
-- =====================================================

CREATE TABLE PhieuBaoHanh (
    MaPhieuBaoHanh INT PRIMARY KEY IDENTITY(1,1),
    MaHoaDon INT,
    MaSanPham INT,
    MaKhachHang INT,
    NgayBatDau DATE NOT NULL,
    NgayKetThuc DATE NOT NULL,
    TrangThai VARCHAR(20) DEFAULT 'ConHieuLuc' CHECK (TrangThai IN ('ConHieuLuc', 'HetHieuLuc', 'DaSuDung')),
    GhiChu NVARCHAR(500),
    NgayTao DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (MaHoaDon) REFERENCES HoaDon(MaHoaDon),
    FOREIGN KEY (MaSanPham) REFERENCES SanPham(MaSanPham),
    FOREIGN KEY (MaKhachHang) REFERENCES KhachHang(MaKhachHang),
    CONSTRAINT CHK_NgayBaoHanh CHECK (NgayKetThuc > NgayBatDau)
);
GO

CREATE TABLE LichSuBaoHanh (
    MaLichSu INT PRIMARY KEY IDENTITY(1,1),
    MaPhieuBaoHanh INT,
    NgaySuaChua DATE NOT NULL,
    MoTaLoi NVARCHAR(500),
    ChiPhiPhatSinh DECIMAL(15, 2) DEFAULT 0,
    NguoiXuLy INT,
    TrangThai VARCHAR(20) DEFAULT 'DangXuLy' CHECK (TrangThai IN ('DangXuLy', 'HoanThanh')),
    GhiChu NVARCHAR(500),
    NgayTao DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (MaPhieuBaoHanh) REFERENCES PhieuBaoHanh(MaPhieuBaoHanh),
    FOREIGN KEY (NguoiXuLy) REFERENCES NguoiDung(MaNguoiDung)
);
GO

-- =====================================================
-- BẢNG CHẤM CÔNG
-- =====================================================

CREATE TABLE ChamCong (
    MaChamCong INT PRIMARY KEY IDENTITY(1,1),
    MaNguoiDung INT,
    NgayChamCong DATE NOT NULL,
    GioVao TIME,
    GioRa TIME,
    SoGioLam DECIMAL(5, 2),
    TrangThai VARCHAR(20) DEFAULT 'DiLam' CHECK (TrangThai IN ('DiLam', 'VangMat', 'NghiPhep', 'DiTre')),
    GhiChu NVARCHAR(255),
    NguoiChamCong INT,
    NgayTao DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (MaNguoiDung) REFERENCES NguoiDung(MaNguoiDung),
    FOREIGN KEY (NguoiChamCong) REFERENCES NguoiDung(MaNguoiDung),
    CONSTRAINT unique_chamcong UNIQUE (MaNguoiDung, NgayChamCong)
);
GO

-- =====================================================
-- TRIGGERS (CHUYỂN ĐỔI TỪ MYSQL SANG SQL SERVER)
-- =====================================================

-- 1. Cập nhật tồn kho khi nhập hàng (Sản phẩm)
CREATE TRIGGER trg_AfterInsert_NhapSanPham
ON ChiTietPhieuNhapSanPham
AFTER INSERT
AS
BEGIN
    UPDATE SanPham 
    SET SoLuongTon = SoLuongTon + i.SoLuong
    FROM SanPham sp
    INNER JOIN inserted i ON sp.MaSanPham = i.MaSanPham;
    
    -- Cập nhật tổng tiền phiếu nhập
    UPDATE PhieuNhapKho
    SET TongTien = (
        SELECT ISNULL(SUM(ThanhTien), 0) 
        FROM ChiTietPhieuNhapSanPham 
        WHERE MaPhieuNhap = i.MaPhieuNhap
    ) + (
        SELECT ISNULL(SUM(ThanhTien), 0) 
        FROM ChiTietPhieuNhapPhuTung 
        WHERE MaPhieuNhap = i.MaPhieuNhap
    )
    FROM PhieuNhapKho p
    INNER JOIN inserted i ON p.MaPhieuNhap = i.MaPhieuNhap;
END;
GO

-- 2. Cập nhật tồn kho khi nhập hàng (Phụ tùng)
CREATE TRIGGER trg_AfterInsert_NhapPhuTung
ON ChiTietPhieuNhapPhuTung
AFTER INSERT
AS
BEGIN
    UPDATE PhuTung 
    SET SoLuongTon = SoLuongTon + i.SoLuong
    FROM PhuTung pt
    INNER JOIN inserted i ON pt.MaPhuTung = i.MaPhuTung;
    
    -- Cập nhật tổng tiền phiếu nhập
    UPDATE PhieuNhapKho
    SET TongTien = (
        SELECT ISNULL(SUM(ThanhTien), 0) 
        FROM ChiTietPhieuNhapSanPham 
        WHERE MaPhieuNhap = i.MaPhieuNhap
    ) + (
        SELECT ISNULL(SUM(ThanhTien), 0) 
        FROM ChiTietPhieuNhapPhuTung 
        WHERE MaPhieuNhap = i.MaPhieuNhap
    )
    FROM PhieuNhapKho p
    INNER JOIN inserted i ON p.MaPhieuNhap = i.MaPhieuNhap;
END;
GO

-- 3. Kiểm tra và giảm tồn kho khi bán hàng (Sản phẩm)
-- Trong SQL Server, logic "BEFORE" thường được xử lý bằng AFTER + ROLLBACK
CREATE TRIGGER trg_AfterInsert_BanSanPham
ON ChiTietHoaDonSanPham
AFTER INSERT
AS
BEGIN
    -- Kiểm tra tồn kho
    IF EXISTS (
        SELECT 1
        FROM inserted i
        JOIN SanPham sp ON i.MaSanPham = sp.MaSanPham
        WHERE sp.SoLuongTon < i.SoLuong
    )
    BEGIN
        RAISERROR ('Số lượng tồn kho không đủ để bán!', 16, 1);
        ROLLBACK TRANSACTION;
        RETURN;
    END

    -- Trừ tồn kho
    UPDATE SanPham 
    SET SoLuongTon = SoLuongTon - i.SoLuong
    FROM SanPham sp
    INNER JOIN inserted i ON sp.MaSanPham = i.MaSanPham;
    
    -- Cập nhật tổng tiền hóa đơn
    UPDATE HoaDon
    SET TongTien = (
        SELECT ISNULL(SUM(ThanhTien), 0) 
        FROM ChiTietHoaDonSanPham 
        WHERE MaHoaDon = i.MaHoaDon
    ) + (
        SELECT ISNULL(SUM(ThanhTien), 0) 
        FROM ChiTietHoaDonPhuTung 
        WHERE MaHoaDon = i.MaHoaDon
    )
    FROM HoaDon hd
    INNER JOIN inserted i ON hd.MaHoaDon = i.MaHoaDon;
    
    -- Cập nhật tổng thanh toán
    UPDATE HoaDon
    SET TongThanhToan = TongTien - TienKhuyenMai
    FROM HoaDon hd
    INNER JOIN inserted i ON hd.MaHoaDon = i.MaHoaDon;
END;
GO

-- 4. Kiểm tra và giảm tồn kho khi bán phụ tùng
CREATE TRIGGER trg_AfterInsert_BanPhuTung
ON ChiTietHoaDonPhuTung
AFTER INSERT
AS
BEGIN
    -- Kiểm tra tồn kho
    IF EXISTS (
        SELECT 1
        FROM inserted i
        JOIN PhuTung pt ON i.MaPhuTung = pt.MaPhuTung
        WHERE pt.SoLuongTon < i.SoLuong
    )
    BEGIN
        RAISERROR ('Số lượng phụ tùng tồn kho không đủ!', 16, 1);
        ROLLBACK TRANSACTION;
        RETURN;
    END

    -- Trừ tồn kho
    UPDATE PhuTung 
    SET SoLuongTon = SoLuongTon - i.SoLuong
    FROM PhuTung pt
    INNER JOIN inserted i ON pt.MaPhuTung = i.MaPhuTung;

    -- Cập nhật tổng tiền hóa đơn (Logic tương tự trigger trên)
    UPDATE HoaDon
    SET TongTien = (
        SELECT ISNULL(SUM(ThanhTien), 0) 
        FROM ChiTietHoaDonSanPham 
        WHERE MaHoaDon = i.MaHoaDon
    ) + (
        SELECT ISNULL(SUM(ThanhTien), 0) 
        FROM ChiTietHoaDonPhuTung 
        WHERE MaHoaDon = i.MaHoaDon
    )
    FROM HoaDon hd
    INNER JOIN inserted i ON hd.MaHoaDon = i.MaHoaDon;
    
    -- Cập nhật tổng thanh toán
    UPDATE HoaDon
    SET TongThanhToan = TongTien - TienKhuyenMai
    FROM HoaDon hd
    INNER JOIN inserted i ON hd.MaHoaDon = i.MaHoaDon;
END;
GO

-- =====================================================
-- DỮ LIỆU MẪU
-- =====================================================

INSERT INTO NguoiDung (TenDangNhap, MatKhau, HoTen, SoDienThoai, Email, VaiTro) VALUES
('admin', '123456', N'Nguyễn Văn Admin', '0901234567', 'admin@cuahangxe.com', 'Admin'),
('quanly01', '123456', N'Trần Thị Quản Lý', '0902345678', 'quanly@cuahangxe.com', 'QuanLy'),
('nhanvien01', '123456', N'Lê Văn Nhân Viên', '0903456789', 'nhanvien@cuahangxe.com', 'NhanVien');
GO

INSERT INTO LoaiXe (TenLoaiXe, MoTa) VALUES
(N'Xe Số', N'Xe số tay truyền thống'),
(N'Xe Tay Ga', N'Xe tay ga tự động'),
(N'Xe Côn Tay', N'Xe côn tay thể thao');
GO

INSERT INTO HangXe (TenHangXe, QuocGia, Website) VALUES
(N'Honda', N'Nhật Bản', 'www.honda.com.vn'),
(N'Yamaha', N'Nhật Bản', 'www.yamaha-motor.com.vn'),
(N'SYM', N'Đài Loan', 'www.sym.com.vn');
GO

INSERT INTO SanPham (TenSanPham, MaLoaiXe, MaHangXe, PhanKhoi, MauSac, NamSanXuat, GiaBan, SoLuongTon) VALUES
(N'Honda Vision 2024', 2, 1, 125, N'Đỏ', 2024, 30000000, 10),
(N'Honda Future 2024', 1, 1, 125, N'Đen', 2024, 28000000, 15),
(N'Yamaha Exciter 155', 3, 2, 155, N'Xanh', 2024, 47000000, 8),
(N'Yamaha Sirius', 1, 2, 110, N'Đen', 2024, 21000000, 20);
GO

INSERT INTO LoaiPhuTung (TenLoaiPhuTung, MoTa) VALUES
(N'Nhớt', N'Dầu nhớt xe máy'),
(N'Lốp xe', N'Lốp xe các loại'),
(N'Phanh', N'Hệ thống phanh'),
(N'Đèn', N'Đèn chiếu sáng');
GO

INSERT INTO PhuTung (TenPhuTung, MaLoaiPhuTung, DonViTinh, GiaNhap, GiaBan, SoLuongTon) VALUES
(N'Nhớt Castrol 10W40', 1, N'Chai', 80000, 120000, 50),
(N'Lốp Michelin 80/90-17', 2, N'Cái', 250000, 350000, 30),
(N'Má phanh Honda', 3, N'Bộ', 80000, 150000, 40),
(N'Đèn LED H4', 4, N'Cái', 150000, 250000, 25);
GO

INSERT INTO NhaCungCap (TenNhaCungCap, SoDienThoai, Email, DiaChi, NguoiLienHe) VALUES
(N'Công ty Honda Việt Nam', '0281234567', 'contact@honda.vn', N'TP. Hồ Chí Minh', N'Nguyễn Văn A'),
(N'Yamaha Motor Việt Nam', '0281234568', 'info@yamaha.vn', N'Hà Nội', N'Trần Thị B');
GO

INSERT INTO KhachHang (HoTen, SoDienThoai, Email, DiaChi, CMND, GioiTinh) VALUES
(N'Phạm Văn Khách', '0912345678', 'khach1@gmail.com', N'123 Đường ABC, Quận 1, TP.HCM', '123456789', 'Nam'),
(N'Nguyễn Thị Lan', '0923456789', 'lan@gmail.com', N'456 Đường XYZ, Quận 2, TP.HCM', '987654321', 'Nu');
GO

-- =====================================================
-- CÁC STORED PROCEDURES
-- =====================================================

-- Procedure: Lấy thông tin tồn kho sản phẩm
CREATE PROCEDURE sp_ThongKeTonKhoSanPham
AS
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
END;
GO

-- Procedure: Thống kê doanh thu theo tháng
CREATE PROCEDURE sp_ThongKeDoanhThuTheoThang
    @nam INT,
    @thang INT
AS
BEGIN
    SELECT 
        CAST(NgayLap AS DATE) AS Ngay,
        COUNT(*) AS SoHoaDon,
        SUM(TongThanhToan) AS DoanhThu,
        SUM(TienKhuyenMai) AS TongKhuyenMai
    FROM HoaDon
    WHERE YEAR(NgayLap) = @nam 
        AND MONTH(NgayLap) = @thang
        AND TrangThai != 'Huy'
    GROUP BY CAST(NgayLap AS DATE)
    ORDER BY Ngay;
END;
GO

-- Procedure: Lấy danh sách sản phẩm sắp hết hàng
CREATE PROCEDURE sp_SanPhamSapHetHang
    @nguong INT
AS
BEGIN
    SELECT 
        sp.MaSanPham,
        sp.TenSanPham,
        hx.TenHangXe,
        sp.SoLuongTon,
        sp.GiaBan
    FROM SanPham sp
    JOIN HangXe hx ON sp.MaHangXe = hx.MaHangXe
    WHERE sp.SoLuongTon <= @nguong
        AND sp.TrangThai = 'ConHang'
    ORDER BY sp.SoLuongTon ASC;
END;
GO

-- =====================================================
-- VIEWS
-- =====================================================

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
GO

CREATE VIEW v_ThongKeNhanVien AS
SELECT 
    nd.MaNguoiDung,
    nd.HoTen,
    nd.VaiTro,
    COUNT(DISTINCT hd.MaHoaDon) AS SoHoaDonLap,
    ISNULL(SUM(hd.TongThanhToan), 0) AS TongDoanhThu,
    COUNT(DISTINCT cc.MaChamCong) AS SoNgayLam
FROM NguoiDung nd
LEFT JOIN HoaDon hd ON nd.MaNguoiDung = hd.MaNguoiDung
LEFT JOIN ChamCong cc ON nd.MaNguoiDung = cc.MaNguoiDung AND cc.TrangThai = 'DiLam'
WHERE nd.VaiTro = 'NhanVien'
GROUP BY nd.MaNguoiDung, nd.HoTen, nd.VaiTro;
GO

-- =====================================================
-- INDEXES
-- =====================================================

CREATE INDEX idx_sanpham_loai ON SanPham(MaLoaiXe);
CREATE INDEX idx_sanpham_hang ON SanPham(MaHangXe);
CREATE INDEX idx_hoadon_khachhang ON HoaDon(MaKhachHang);
CREATE INDEX idx_hoadon_ngaylap ON HoaDon(NgayLap);
CREATE INDEX idx_chamcong_ngay ON ChamCong(NgayChamCong);
CREATE INDEX idx_phieubaohanh_khachhang ON PhieuBaoHanh(MaKhachHang);
GO

PRINT 'Database setup completed successfully!';