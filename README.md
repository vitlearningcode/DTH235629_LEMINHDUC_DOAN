# =================================================================
# FILE: README.md
# HƯỚNG DẪN CÀI ĐẶT VÀ SỬ DỤNG HỆ THỐNG
# =================================================================

# HỆ THỐNG QUẢN LÝ CỬA HÀNG XE MÁY

## 📋 MÔ TẢ DỰ ÁN

Hệ thống quản lý cửa hàng xe máy được phát triển bằng Python Tkinter với cơ sở dữ liệu MySQL. Hệ thống hỗ trợ 3 vai trò người dùng với phân quyền rõ ràng:

- **Admin (Chủ cửa hàng)**: Toàn quyền quản lý tất cả các chức năng
- **QuanLy (Quản lý)**: Chỉ xem thông tin và có quyền chấm công
- **NhanVien (Nhân viên)**: Lập hóa đơn bán hàng, dịch vụ sửa chữa

## 🎨 ĐẶC ĐIỂM GIAO DIỆN

- **Màu sắc chủ đạo**: Các tông màu xanh da trời (#87CEEB, #4682B4, #5F9EA0)
- **Thiết kế**: Đơn giản, dễ sử dụng, phù hợp cho người mới học Python
- **Responsive**: Giao diện tự động điều chỉnh theo kích thước màn hình

## 📦 YÊU CẦU HỆ THỐNG

### Phần mềm cần cài đặt:
1. **Python 3.8+** (Tải tại: https://www.python.org/downloads/)
2. **MySQL Server 8.0+** (Tải tại: https://dev.mysql.com/downloads/mysql/)
3. **MySQL Connector for Python**

### Thư viện Python:
```bash
pip install mysql-connector-python
pip install tkinter  # Thường đã có sẵn với Python
```

## 🚀 HƯỚNG DẪN CÀI ĐẶT

### Bước 1: Cài đặt MySQL Server
1. Tải và cài đặt MySQL Server
2. Trong quá trình cài đặt, thiết lập:
   - Username: `root`
   - Password: (tùy chọn của bạn)
   - Port: `3306` (mặc định)

### Bước 2: Tạo Database
1. Mở MySQL Workbench hoặc Command Line
2. Chạy file `database_setup.sql`:
   ```sql
   mysql -u root -p < database_setup.sql
   ```
   Hoặc copy toàn bộ nội dung file và chạy trong MySQL Workbench

### Bước 3: Cấu hình kết nối
Mở file `database_connection.py` và chỉnh sửa thông tin kết nối:
```python
self.host = 'localhost'
self.database = 'QUANLYCUAHANGXEMAY'
self.user = 'root'          # Thay bằng username MySQL của bạn
self.password = ''          # Thay bằng password MySQL của bạn
```

### Bước 4: Cài đặt thư viện
```bash
pip install mysql-connector-python
```

### Bước 5: Chạy chương trình
```bash
python login.py
```

## 👥 TÀI KHOẢN MẶC ĐỊNH

| Vai trò | Tên đăng nhập | Mật khẩu | Quyền hạn |
|---------|---------------|----------|-----------|
| Admin | admin | 123456 | Toàn quyền |
| Quản lý | quanly01 | 123456 | Xem + Chấm công |
| Nhân viên | nhanvien01 | 123456 | Bán hàng |

## 📁 CẤU TRÚC FILE

```
QuanLyCuaHangXeMay/
│
├── database_setup.sql          # Script tạo database
├── database_connection.py      # Module kết nối database
├── login.py                    # Form đăng nhập
├── admin_window.py             # Giao diện Admin
├── quanly_window.py           # Giao diện Quản lý
├── nhanvien_window.py         # Giao diện Nhân viên
└── README.md                   # File hướng dẫn này
```

## 🗄️ CẤU TRÚC DATABASE

### Các bảng chính:
1. **NguoiDung**: Quản lý tài khoản người dùng
2. **SanPham**: Thông tin xe máy
3. **PhuTung**: Phụ tùng, linh kiện
4. **KhachHang**: Thông tin khách hàng
5. **HoaDon**: Hóa đơn bán hàng
6. **PhieuNhapKho**: Phiếu nhập hàng
7. **PhieuBaoHanh**: Phiếu bảo hành
8. **ChamCong**: Chấm công nhân viên
9. **KhuyenMai**: Chương trình khuyến mãi

### Các trigger tự động:
- ✅ Tự động cập nhật tồn kho khi nhập hàng
- ✅ Kiểm tra tồn kho trước khi bán (tránh số âm)
- ✅ Tự động tính tổng tiền hóa đơn
- ✅ Tự động tính tổng tiền phiếu nhập

## 🔧 CHỨC NĂNG CHI TIẾT

### 🔑 Class Login
- Đăng nhập với phân quyền
- Kiểm tra trạng thái tài khoản
- Chuyển hướng đến giao diện phù hợp

### 👨‍💼 Class Admin (Chủ cửa hàng)
**Toàn quyền chỉnh sửa:**
- ✏️ Quản lý nhân viên (Thêm/Sửa/Xóa)
- 🏍️ Quản lý sản phẩm (Thêm/Sửa/Xóa)
- 🔧 Quản lý phụ tùng (Thêm/Sửa/Xóa)
- 📦 Quản lý kho (Nhập/Xuất)
- 🎁 Quản lý khuyến mãi
- 👤 Quản lý khách hàng
- 📄 Quản lý hóa đơn
- ⏰ Quản lý chấm công
- 📊 Báo cáo thống kê đầy đủ

### 👔 Class QuanLy (Quản lý)
**Chỉ xem và chấm công:**
- 👁️ Xem thông tin tất cả các module
- ✅ Chấm công cho nhân viên
- ❌ Không có quyền chỉnh sửa dữ liệu

### 👨‍💻 Class NhanVien (Nhân viên)
**Bán hàng và dịch vụ:**
- 🛒 Tạo hóa đơn bán xe
- 🔧 Lập phiếu sửa chữa/bảo dưỡng
- 👤 Thêm khách hàng mới
- 📋 Xem lịch sử hóa đơn của mình
- ⚠️ **Logic đồng bộ kho**: Hệ thống tự động kiểm tra tồn kho, không cho phép bán khi số lượng không đủ

## 🔒 BẢO MẬT

- Mật khẩu được lưu trữ ở dạng plain text (trong thực tế nên hash)
- Phân quyền rõ ràng theo vai trò
- Kiểm tra trạng thái tài khoản trước khi đăng nhập

## 📊 TRIGGER VÀ RÀNG BUỘC

### Ràng buộc dữ liệu:
```sql
- SoLuongTon >= 0 (không cho phép âm)
- GiaBan > 0
- NgayKetThuc >= NgayBatDau
- Unique constraints trên các trường quan trọng
```

### Trigger tự động:
```sql
- after_insert_nhapsanpham: Cập nhật tồn kho sau khi nhập
- before_insert_bansanpham: Kiểm tra tồn kho trước khi bán
- after_insert_chitiet_hoadon: Tự động tính tổng tiền hóa đơn
```

## 🎯 HƯỚNG DẪN SỬ DỤNG

### Đăng nhập lần đầu:
1. Chạy `python login.py`
2. Đăng nhập bằng tài khoản `admin/123456`
3. Khám phá các chức năng

### Quy trình bán hàng (Nhân viên):
1. Đăng nhập tài khoản nhân viên
2. Nhập SĐT khách hàng (hoặc thêm mới)
3. Chọn sản phẩm từ danh sách
4. Thêm vào giỏ hàng
5. Thanh toán

### Quy trình nhập hàng (Admin):
1. Vào "Quản lý kho"
2. Tạo phiếu nhập mới
3. Chọn nhà cung cấp
4. Thêm sản phẩm và số lượng
5. Lưu phiếu nhập

### Chấm công (Quản lý):
1. Vào "Chấm công"
2. Chọn ngày
3. Chọn nhân viên
4. Nhập giờ vào/ra
5. Chọn trạng thái (Đi làm/Vắng mặt/Nghỉ phép/Đi trễ)
6. Lưu

## 🐛 XỬ LÝ LỖI THƯỜNG GẶP

### Lỗi kết nối database:
```
Error: Can't connect to MySQL server
```
**Giải pháp**: 
- Kiểm tra MySQL Server đã chạy chưa
- Kiểm tra username/password trong `database_connection.py`

### Lỗi import module:
```
ModuleNotFoundError: No module named 'mysql.connector'
```
**Giải pháp**:
```bash
pip install mysql-connector-python
```

### Lỗi trigger:
```
Error: Số lượng tồn kho không đủ để bán!
```
**Giải pháp**: Đây là tính năng bảo vệ, cần nhập thêm hàng trước khi bán

## 📝 GHI CHÚ

- Code được viết đơn giản, dễ hiểu cho người mới học Python
- Không sử dụng các kỹ thuật tối ưu phức tạp
- Có thể mở rộng thêm nhiều chức năng khác
- Database đã có sẵn dữ liệu mẫu để test

## 🔄 PHÁT TRIỂN THÊM

Các chức năng có thể mở rộng:
- [ ] Báo cáo thống kê chi tiết hơn (biểu đồ)
- [ ] In hóa đơn PDF
- [ ] Backup/Restore database
- [ ] Gửi email thông báo
- [ ] Quản lý lương nhân viên
- [ ] Tích hợp thanh toán online

## 📞 HỖ TRỢ

Nếu gặp vấn đề trong quá trình sử dụng:
1. Kiểm tra lại các bước cài đặt
2. Đảm bảo MySQL Server đang chạy
3. Kiểm tra thông tin kết nối database
4. Xem log lỗi trong console

## 📚 TÀI LIỆU THAM KHẢO

- [Python Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [MySQL Connector Python](https://dev.mysql.com/doc/connector-python/en/)

---

# QUẢN LÝ CỬA HÀNG XE MÁY — TÀI LIỆU HƯỚNG DẪN TOÀN DIỆN

Phiên bản dự án: 1.0.0  
Ngày tạo: 2025-11-18  
Ngôn ngữ chính: Python 3.8+ (Tkinter)  
Cơ sở dữ liệu: MySQL 8.0+ (mặc định) — có thể chuyển sang SQL Server theo cấu hình.  
Mục tiêu tài liệu: cung cấp hướng dẫn cài đặt, cấu hình, vận hành, phát triển và bảo trì chi tiết cho người cài đặt, lập trình viên và người kiểm thử.

---
MỤC LỤC
1. Tổng quan dự án
2. Yêu cầu hệ thống
3. Chuẩn bị môi trường
4. Thiết lập cơ sở dữ liệu
5. Cấu hình ứng dụng
6. Cài đặt và chạy ứng dụng
7. Kiến trúc hệ thống và mô tả module
8. Cơ sở dữ liệu — mô tả chi tiết bảng và ràng buộc
9. Trigger, stored procedures và rules nghiệp vụ
10. Quy trình nghiệp vụ (Use cases)
11. Giao diện người dùng — hướng dẫn sử dụng từng màn hình
12. Bảo mật và quản trị hệ thống
13. Backup, khôi phục và quản lý dữ liệu
14. Kiểm thử và test cases
15. Tối ưu hiệu năng và gợi ý mở rộng
16. DevOps, CI/CD và triển khai sản phẩm
17. Quy ước mã nguồn, đóng góp và review
18. FAQ và khắc phục lỗi thường gặp
19. Lịch sử phiên bản (CHANGELOG)
20. Liên hệ, license và tài liệu tham khảo

---

1. TỔNG QUAN DỰ ÁN
Dự án "Quản lý cửa hàng xe máy" là một ứng dụng desktop phát triển bằng Python và Tkinter.
Mục tiêu: tự động hóa các nghiệp vụ bán hàng, quản lý tồn kho, quản lý khách hàng, chấm công và báo cáo cho cửa hàng xe máy vừa và nhỏ.
Thiết kế hướng tới: dễ cài đặt trên Windows, dễ mở rộng, dễ hiểu cho sinh viên và lập trình viên mới.
Hỗ trợ phân quyền ba vai trò: Admin, Quản lý (QuanLy) và Nhân viên (NhanVien).
Ứng dụng tích hợp các kiểm tra nghiệp vụ để đảm bảo tính toàn vẹn dữ liệu (ví dụ kiểm tra tồn kho trước khi bán).
Ứng dụng cung cấp cơ chế import/export dữ liệu (CSV/Excel) và các báo cáo cơ bản.
Tài liệu hiện tại mô tả chi tiết cách cài đặt, cấu hình, vận hành, triển khai và phát triển tiếp.

2. YÊU CẦU HỆ THỐNG
Hệ điều hành: Windows 10/11 (được kiểm thử), có thể chạy trên Linux/Mac với một số điều chỉnh.
Phần mềm: Python 3.8 hoặc cao hơn.
Cơ sở dữ liệu: MySQL Server 8.0+ (mặc định). Hỗ trợ SQL Server nếu cấu hình lại module kết nối.
Driver DB: mysql-connector-python hoặc pyodbc (nếu dùng SQL Server).
Không gian đĩa tối thiểu: 500 MB trống cho mã nguồn và dữ liệu mẫu.
RAM tối thiểu: 4 GB; khuyến nghị 8 GB cho môi trường sản xuất nhỏ.
Mạng: cổng kết nối MySQL mở (mặc định 3306) nếu dùng server từ xa.
Quyền hệ thống: quyền cài đặt Python, gói pip và quyền tạo database trên MySQL.

3. CHUẨN BỊ MÔI TRƯỜNG
3.1 Tải Python
Tải Python 3.8+ từ https://www.python.org/downloads/.
Trong quá trình cài đặt, chọn "Add Python to PATH".
3.2 Tạo Virtual Environment
Tại thư mục dự án, thực hiện:
python -m venv .venv
.venv\Scripts\activate
3.3 Cài pip và cập nhật
python -m pip install --upgrade pip setuptools wheel
3.4 Cài các thư viện cần thiết
pip install -r requirements.txt
Nếu không có requirements.txt:
pip install mysql-connector-python pillow openpyxl pandas
Nếu dùng SQL Server:
pip install pyodbc
Gợi ý: chạy lệnh pip trong virtualenv để tránh xung đột hệ thống.

4. THIẾT LẬP CƠ SỞ DỮ LIỆU
4.1 Tạo database
Mở MySQL Workbench hoặc sử dụng mysql command line:
mysql -u root -p
CREATE DATABASE quanly_cuahang_xemay CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
4.2 Khởi tạo schema
Chạy file database_setup.sql có trong thư mục gốc:
mysql -u root -p quanly_cuahang_xemay < database_setup.sql
4.3 Dữ liệu mẫu
File database_setup.sql chứa:
- Tạo bảng chính
- Ràng buộc foreign key
- Trigger mẫu
- Dữ liệu mẫu cho tài khoản demo, sản phẩm, khách hàng
Kiểm tra sau khi chạy: SELECT COUNT(*) FROM NguoiDung; SELECT COUNT(*) FROM SanPham;
4.4 Quyền truy cập
Khuyến nghị: tạo user riêng cho ứng dụng:
CREATE USER 'app_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT SELECT, INSERT, UPDATE, DELETE ON quanly_cuahang_xemay.* TO 'app_user'@'localhost';
FLUSH PRIVILEGES;
Không sử dụng tài khoản root trên môi trường production.

5. CẤU HÌNH ỨNG DỤNG
5.1 File cấu hình
Mở file config.py hoặc database_connection.py (tùy cấu trúc dự án).
Các tham số chính:
- host / server
- port
- database name
- username
- password
- driver (nếu dùng pyodbc)
Đặt cấu hình phù hợp với môi trường (local hoặc production).
5.2 Ví dụ cấu hình (MySQL)
self.host = 'localhost'
self.port = 3306
self.database = 'quanly_cuahang_xemay'
self.user = 'app_user'
self.password = 'secure_password'
5.3 Ví dụ cấu hình (SQL Server)
self.server = r'localhost\SQLEXPRESS'
self.database = 'QUANLYCUAHANGXEMAY'
self.username = 'sa'
self.password = 'your_password'
self.driver = 'ODBC Driver 17 for SQL Server'
5.4 Biện pháp bảo mật cấu hình
- Không commit file cấu hình chứa mật khẩu vào git.
- Sử dụng biến môi trường (os.environ) hoặc file .env kết hợp python-dotenv.
- Đối với production, dùng secret manager nếu có.

6. CÀI ĐẶT VÀ CHẠY ỨNG DỤNG
6.1 Chuẩn bị
Kích hoạt virtualenv.
Đảm bảo MySQL đang chạy.
Đảm bảo file database đã được tạo.
6.2 Chạy ứng dụng
python login.py
6.3 Tạo shortcut (Windows)
Tạo file .bat:
@echo off
call .venv\Scripts\activate
python %~dp0\login.py
pause
6.4 Kiểm tra logs
Ứng dụng in log ra console. Xem file logs nếu dự án cấu hình logging sang file.
6.5 Tài khoản demo
Admin: admin / 123456
QuanLy: quanly01 / 123456
NhanVien: nhanvien01 / 123456
Lưu ý: thay đổi mật khẩu mặc định sau khi cài đặt.

7. KIẾN TRÚC HỆ THỐNG VÀ MÔ TẢ MODULE
7.1 Tổng quan kiến trúc
Ứng dụng theo mô hình client-side desktop app.
Giao diện: Tkinter.
Business logic: các module Python trong thư mục Function/ hoặc src/.
Database access: module database_connection.py.
Tài nguyên tĩnh: images, icons, assets.
7.2 Module chính
- login.py: xử lý đăng nhập và phân quyền.
- database_connection.py: lớp quản lý kết nối và truy vấn.
- admin_window.py: GUI cho Admin.
- quanly_window.py: GUI cho Quản lý.
- nhanvien_window.py: GUI cho Nhân viên.
- Function/: các module nghiệp vụ (sanpham.py, phutung.py, hoadon.py, phieunhap.py, chamcong.py, khuyenmai.py, khachhang.py).
7.3 Dòng chảy nghiệp vụ (flow)
Người dùng mở login.py -> xác thực -> điều hướng sang cửa sổ tương ứng -> tương tác các module -> lưu thay đổi DB -> thông báo kết quả.
7.4 Mô-đun truy vấn
Tất cả truy vấn DB phải sử dụng prepared statements (parameterized queries) để tránh SQL injection.
Tránh nối chuỗi để tạo query trực tiếp với input người dùng.
7.5 Logging
Sử dụng logging module để ghi log ở các mức INFO, WARNING, ERROR.
Lưu log ra file logs/app.log để theo dõi trong production.

8. CƠ SỞ DỮ LIỆU — MÔ TẢ CHI TIẾT
8.1 Bảng NguoiDung
- IDNguoiDung (PK, int, auto_increment)
- TenDangNhap (varchar, unique, not null)
- MatKhau (varchar, not null) — LƯU Ý: hệ thống mẫu dùng plain text, production phải hash.
- HoTen (varchar)
- VaiTro (enum: Admin, QuanLy, NhanVien)
- TrangThai (tinyint: 0=khóa, 1=hoạt động)
- NgayTao, NgayCapNhat
Index: TenDangNhap unique.
8.2 Bảng SanPham
- IDSanPham (PK)
- MaSanPham (varchar, unique)
- TenSanPham (varchar)
- MoTa (text)
- GiaNhap (decimal)
- GiaBan (decimal)
- SoLuongTon (int) — constraints >= 0
- HinhAnh (varchar)
- NhaCungCapID (FK)
- NgayTao
8.3 Bảng PhuTung
- IDPhuTung (PK)
- MaPhuTung
- TenPhuTung
- Gia
- SoLuongTon
- Nhom (loại phụ tùng)
8.4 Bảng KhachHang
- IDKhachHang
- Ten
- SoDienThoai (unique)
- DiaChi
- Email
- DiaChiGiaoHang
8.5 Bảng HoaDon
- IDHoaDon
- MaHoaDon (unique)
- IDNhanVien (FK)
- IDKhachHang (FK, nullable)
- NgayLap
- TongTien
- TrangThaiThanhToan
8.6 Bảng ChiTietHoaDon
- IDChiTiet (PK)
- IDHoaDon (FK)
- IDSanPham (FK)
- SoLuong
- DonGia
- ThanhTien (SoLuong * DonGia)
8.7 Bảng PhieuNhapKho
- IDPhieuNhap
- MaPhieu
- IDNhanVienNhap
- NgayNhap
- TongTienNhap
8.8 Bảng ChiTietPhieuNhap
- ID
- IDPhieuNhap
- IDSanPham
- SoLuong
- DonGiaNhap
8.9 Bảng ChamCong
- IDChamCong
- IDNhanVien
- Ngay
- GioVao
- GioRa
- TrangThai (DiLam, VangMat, NghiPhep, DiTre)
8.10 Bảng KhuyenMai
- IDKhuyenMai
- MaKM
- Ten
- Loai (phan tram/so tien)
- GiaTri
- NgayBatDau
- NgayKetThuc
8.11 Ràng buộc chung
- SoLuongTon >= 0
- GiaBan > 0
- GiaNhap >= 0
- NgayKetThuc >= NgayBatDau cho chương trình khuyến mãi
- Các khóa ngoại phải tồn tại
8.12 Index và hiệu năng
- Index trên MaSanPham, TenSanPham, SoDienThoai khách hàng.
- Index trên NgayLap cho bảng HoaDon để truy vấn theo thời gian nhanh.
- Tránh index quá mức gây ảnh hưởng ghi.

9. TRIGGER, STORED PROCEDURE VÀ BUSINESS RULES
9.1 Trigger cập nhật tồn kho sau khi nhập
Mục đích: sau khi insert vào ChiTietPhieuNhap, tăng SoLuongTon trên SanPham.
9.2 Trigger kiểm tra tồn trước khi bán
Mục đích: trước khi insert vào ChiTietHoaDon, kiểm tra SoLuongTon >= SoLuong bán.
Hành vi: nếu không đủ tồn, hủy transaction và báo lỗi cho UI.
9.3 Trigger cập nhật tổng tiền hóa đơn
Sau khi insert/update/delete ChiTietHoaDon, cập nhật lại TongTien trong HoaDon.
9.4 Stored procedures (tùy chọn)
- sp_CreateInvoice (tạo hóa đơn mới, tính thuế, khuyến mãi)
- sp_AddStock (tạo phiếu nhập và cập nhật tồn)
9.5 Quy ước giao dịch
Sử dụng transaction khi tạo hóa đơn và khi nhập kho để đảm bảo atomicity.
Trong Python, sử dụng connection.begin() / commit() / rollback() hoặc context manager.

10. QUY TRÌNH NGHIỆP VỤ (USE CASES)
10.1 Use case: Đăng nhập
Người dùng nhập TenDangNhap và MatKhau.
Hệ thống kiểm tra tồn tại và trạng thái tài khoản.
Hệ thống gửi thông báo nếu sai mật khẩu hoặc tài khoản bị khóa.
10.2 Use case: Lập hóa đơn bán hàng
Nhân viên tạo hóa đơn mới.
Tìm khách hàng theo SĐT hoặc thêm khách hàng mới.
Chọn sản phẩm, thêm vào giỏ hàng.
Hệ thống kiểm tra tồn cho mỗi sản phẩm.
Hoàn tất thanh toán và lưu hóa đơn.
Giảm SoLuongTon tương ứng.
Tạo in hóa đơn (nếu có).
10.3 Use case: Nhập kho
Admin/Quản lý tạo phiếu nhập.
Chọn nhà cung cấp và sản phẩm.
Lưu phiếu nhập và tăng tồn kho.
10.4 Use case: Chấm công
Quản lý vào module chấm công.
Chọn nhân viên và ngày.
Nhập giờ vào/ra và trạng thái.
Hệ thống lưu và cho phép xuất báo cáo chấm công.
10.5 Use case: Quản lý khuyến mãi
Admin tạo chương trình khuyến mãi.
Áp dụng khuyến mãi cho sản phẩm/hoá đơn theo loại.
Đảm bảo ngày bắt đầu/ket thúc hợp lệ.

11. GIAO DIỆN NGƯỜI DÙNG — HƯỚNG DẪN SỬ DỤNG
11.1 Màn hình đăng nhập
Trường: TenDangNhap, MatKhau.
Nút: Đăng nhập, Quên mật khẩu (nếu triển khai).
Hệ thống chuyển sang cửa sổ theo VaiTro.
11.2 Màn hình Admin
Menu: Người dùng, Sản phẩm, Kho, Hóa đơn, Khuyến mãi, Báo cáo, Cài đặt.
Chức năng: CRUD người dùng, quản lý quyền, sao lưu DB, cấu hình.
11.3 Màn hình Quản lý
Menu: Xem thông tin tất cả module, Chấm công, Báo cáo cơ bản.
Quản lý không có quyền xóa/sửa người dùng (tùy cài đặt).
11.4 Màn hình Nhân viên
Menu: Bán hàng, Khách hàng, Lịch sử hóa đơn, Dịch vụ sửa chữa.
Nhân viên được phép tạo hóa đơn và thêm khách hàng.
11.5 Hướng dẫn từng tác vụ
Mỗi form có nút Lưu, Hủy, Làm mới, Tìm kiếm.
Tìm kiếm hỗ trợ lọc theo tên, mã, khoảng giá, nhà cung cấp.
Danh sách kết quả hỗ trợ chọn nhiều dòng, export Excel.
11.6 In ấn và export
Hỗ trợ xuất hóa đơn/phiếu nhập ra Excel (openpyxl).
Khuyến nghị: tích hợp tạo PDF nếu cần (reportlab hoặc wkhtmltopdf).

12. BẢO MẬT VÀ QUẢN TRỊ HỆ THỐNG
12.1 Mật khẩu
Hiện mẫu: lưu plain text (không an toàn).
Phải: hash mật khẩu bằng bcrypt/argon2 trước khi lưu.
Sử dụng bcrypt với salt tự động.
12.2 Phân quyền
Quyết định quyền tại tầng ứng dụng và DB.
Kiểm tra quyền trước mỗi hành động nhạy cảm (xóa, import, export, backup).
12.3 Kết nối DB
Sử dụng account DB có quyền giới hạn cho ứng dụng.
Không dùng tài khoản root/sa trong production.
12.4 Mã hóa dữ liệu nhạy cảm
Mã hóa thông tin khách hàng hoặc thông tin thẻ nếu lưu (tốt nhất không lưu thẻ).
12.5 Logging & Audit
Ghi lịch sử thao tác quan trọng: ai tạo/ sửa/ xóa hoá đơn, nhập kho.
Lưu audit trail (NguoiDungID, HanhDong, ThoiGian, ChiTiet).
12.6 Cập nhật và vá lỗi
Giữ Python và thư viện cập nhật để giảm rủi ro bảo mật.
Theo dõi CVE cho các thư viện quan trọng.

13. BACKUP, KHÔI PHỤC VÀ QUẢN LÝ DỮ LIỆU
13.1 Backup DB
Sử dụng mysqldump:
mysqldump -u app_user -p quanly_cuahang_xemay > backup_YYYYMMDD.sql
Lên lịch backup định kỳ (hàng ngày cho dữ liệu giao dịch).
13.2 Restore DB
mysql -u root -p quanly_cuahang_xemay < backup_YYYYMMDD.sql
Kiểm tra restore trên môi trường staging trước khi đưa vào production.
13.3 Export/Import CSV, Excel
Hỗ trợ export danh sách sản phẩm, khách hàng, hoá đơn.
Hỗ trợ import sản phẩm/khách hàng từ file CSV (có mapping và kiểm tra dữ liệu).
13.4 Dọn dẹp dữ liệu
Thiết kế script cron/batch để xóa dữ liệu test cũ hoặc nén logs.
13.5 Lưu trữ hình ảnh
Lưu ảnh sản phẩm trong thư mục assets/images hoặc Lưu URL nếu dùng object storage.
Không lưu ảnh trực tiếp vào DB.

14. KIỂM THỬ VÀ TEST CASES
14.1 Unit tests
Tách logic xử lý khỏi GUI để test dễ dàng.
Sử dụng pytest cho unit test.
14.2 Integration tests
Test luồng từ UI -> DB (mô phỏng DB test).
Sử dụng DB test hoặc in-memory DB khi khả thi.
14.3 Test cases mẫu
- TC-001: Đăng nhập thành công với account Admin.
- TC-002: Không đăng nhập khi mật khẩu sai.
- TC-003: Không tạo hoá đơn khi tồn kho không đủ.
- TC-004: Nhập kho tăng đúng số lượng tồn.
- TC-005: Áp dụng khuyến mãi đúng thời gian.
- TC-006: Export danh sách sản phẩm ra Excel và kiểm tra nội dung.
14.4 Kiểm thử bảo mật
- Test injection: đảm bảo prepared statements.
- Test XSS: không áp dụng trong desktop nhưng kiểm tra input hiển thị HTML.
- Test quyền truy cập: đảm bảo vai trò không thể truy cập chức năng giới hạn.
14.5 Quy trình test
Tạo test plan, viết test script, chạy test, report bug vào issue tracker.

15. TỐI ƯU HIỆU NĂNG VÀ GỢI Ý MỞ RỘNG
15.1 Tối ưu truy vấn
- Sử dụng index hợp lý.
- Giảm số lượng query trong một luồng xử lý (batch queries).
15.2 Caching
- Sử dụng caching ở tầng ứng dụng cho dữ liệu tĩnh (danh mục, nhà cung cấp).
- Thận trọng khi cache dữ liệu thay đổi thường xuyên.
15.3 Tối ưu GUI
- Sử dụng lazy loading cho danh sách lớn (pagination).
- Tránh render lại toàn bộ table khi chỉ cập nhật vài dòng.
15.4 Mở rộng sang web/API
- Xây API REST (Flask/FastAPI) để tích hợp POS hoặc website.
- Tách business logic ra service để tái sử dụng.
15.5 Scaling
- Với lượng dữ liệu lớn, chuyển DB lên MySQL cluster hoặc dùng cloud DB.
- Sử dụng backup incremental và replication.

16. DEVOPS, CI/CD VÀ TRIỂN KHAI
16.1 Repository & branching
- Branch chính: main (production), develop (tích lũy), feature/* cho chức năng mới.
- Pull request: review trước merge.
16.2 CI (ví dụ GitHub Actions)
- Kiểm tra code style (flake8).
- Chạy unit tests (pytest).
- Build artifacts nếu cần.
16.3 CD
- Với ứng dụng desktop, tạo package bằng PyInstaller hoặc cx_Freeze.
- Tạo installer (.exe) hoặc zip để phân phối.
16.4 Packaging
- requirements.txt cho runtime.
- setup.py hoặc pyproject.toml cho package nội bộ.
16.5 Triển khai lên máy chủ
- Đặt DB trên server riêng.
- Cung cấp đường dẫn cấu hình và user ứng dụng.
- Đào tạo nhân viên trước khi chuyển đổi.

17. QUY ƯỚC MÃ NGUỒN, ĐÓNG GÓP VÀ REVIEW
17.1 Tiêu chuẩn code
- Tuân thủ PEP8.
- Viết docstring cho hàm và lớp (sphinx-style hoặc google-style).
- Đặt tên biến rõ ràng, bằng tiếng Anh cho code.
17.2 Commit messages
- Dùng dạng: [MODULE] Short description — ví dụ: [HOADON] Add invoice validation
- Viết mô tả chi tiết trong body nếu cần.
17.3 Pull request
- Mô tả thay đổi, test case đã chạy, ảnh chụp màn hình nếu có.
- Review ít nhất 1 người khác trước khi merge.
17.4 Issue tracker
- Ghi lỗi rõ ràng: tiêu đề, môi trường, bước tái tạo, kết quả mong đợi và thực tế.
17.5 Contribution guide
- Fork -> feature branch -> PR -> review -> merge.
- Chạy test trước khi gửi PR.

18. FAQ VÀ KHẮC PHỤC LỖI THƯỜNG GẶP
18.1 Lỗi: Can't connect to MySQL server
- Kiểm tra service MySQL đã chạy.
- Kiểm tra host, port, user và password.
- Kiểm tra firewall và quyền truy cập.
18.2 Lỗi: ModuleNotFoundError: No module named 'mysql.connector'
- Chạy: pip install mysql-connector-python
- Kiểm tra virtualenv đã active.
18.3 Lỗi: Tồn kho âm sau khi bán
- Kiểm tra trigger trước khi bán có áp dụng không.
- Kiểm tra luồng transaction: commit/rollback có đúng chỗ không.
18.4 Lỗi: Mật khẩu bị lộ
- Thay đổi mật khẩu tức thời.
- Mã hóa mật khẩu bằng bcrypt.
- Kiểm tra lịch sử commit để đảm bảo mật khẩu không bị commit.
18.5 Lỗi: Ứng dụng chậm khi load danh sách lớn
- Thực hiện pagination.
- Chỉ load cột cần thiết, không load text/ảnh nặng trong table.
18.6 Lỗi: Lỗi thời gian/định dạng ngày
- Chuẩn hóa timezone và format ngày.
- Lưu trên DB ở dạng DATETIME hoặc TIMESTAMP với timezone thống nhất.

19. CHANGELOG (LỊCH SỬ PHIÊN BẢN)
V1.0.0 - 2025-11-18
- Phiên bản đầu tiên hoàn thiện nghiệp vụ cơ bản.
- Hỗ trợ phân quyền, bán hàng, nhập kho, chấm công, báo cáo cơ bản.
- Tích hợp trigger kiểm tra tồn và cập nhật tổng tiền.
- Cung cấp file database_setup.sql và dữ liệu mẫu.

20. LIÊN HỆ, LICENSE VÀ TÀI LIỆU THAM KHẢO
20.1 Liên hệ
- Tên tác giả: LEMINHDUC (thông tin chi tiết lưu nội bộ dự án)
- Hướng dẫn viên / giảng viên: ghi trong tài liệu dự án.
20.2 License
- Thêm file LICENSE nếu muốn public (ví dụ MIT).
20.3 Tài liệu tham khảo
- Python: https://www.python.org/doc/
- Tkinter: https://docs.python.org/3/library/tkinter.html
- MySQL: https://dev.mysql.com/doc/
- mysql-connector-python: https://dev.mysql.com/doc/connector-python/en/
- pyodbc: https://github.com/mkleehammer/pyodbc

---

PHỤ LỤC A — CÁC CÂU LỆNH SQL MẪU
A.1 Tạo user ứng dụng:
CREATE USER 'app_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT SELECT, INSERT, UPDATE, DELETE ON quanly_cuahang_xemay.* TO 'app_user'@'localhost';
FLUSH PRIVILEGES;
A.2 Trigger kiểm tra tồn trước khi bán (mẫu MySQL):
DELIMITER $$
CREATE TRIGGER before_insert_chitiet_hoadon
BEFORE INSERT ON ChiTietHoaDon
FOR EACH ROW
BEGIN
  DECLARE avail INT;
  SELECT SoLuongTon INTO avail FROM SanPham WHERE IDSanPham = NEW.IDSanPham;
  IF avail IS NULL THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'San pham khong ton tai';
  ELSEIF avail < NEW.SoLuong THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'So luong ton khong du de ban';
  END IF;
END$$
DELIMITER ;
A.3 Trigger cập nhật tồn sau khi nhập kho (mẫu):
DELIMITER $$
CREATE TRIGGER after_insert_chitiet_phieunhap
AFTER INSERT ON ChiTietPhieuNhap
FOR EACH ROW
BEGIN
  UPDATE SanPham SET SoLuongTon = SoLuongTon + NEW.SoLuong WHERE IDSanPham = NEW.IDSanPham;
END$$
DELIMITER ;

PHỤ LỤC B — MẪU UNIT TEST (pytest)
B.1 test_database_connection.py (mẫu)
import pytest
from database_connection import Database
def test_connect():
    db = Database(config_test)
    conn = db.connect()
    assert conn is not None
B.2 test_business_logic.py (mẫu)
def test_calculate_line_total():
    from Function.hoadon import calculate_line_total
    assert calculate_line_total(2, 15000) == 30000

PHỤ LỤC C — HƯỚNG DẪN TÌM VÀ SỬA LỖI LOGIC THƯỜNG GẶP
C.1 Kiểm tra luồng transaction
- Mở code tạo hóa đơn.
- Kiểm tra: bắt đầu transaction, insert ChiTietHoaDon, cập nhật tồn, commit.
- Nếu commit trước khi cập nhật tồn, rollback khi lỗi.
C.2 Xác minh dữ liệu test
- Kiểm tra dữ liệu mẫu: giá trị SoLuongTon khởi tạo.
- Dùng truy vấn SELECT để xác minh trước và sau thao tác.
C.3 Debugging
- Bật logging chi tiết cho module DB:
logging.getLogger('db').setLevel(logging.DEBUG)
- In query và parameters trong logs (không in mật khẩu).

PHỤ LỤC D — DANH SÁCH TASK TODO CHO PHÁT TRIỂN TIẾP
- [ ] Hash mật khẩu bằng bcrypt.
- [ ] Tạo chế độ quên mật khẩu bằng email (SMTP).
- [ ] Thêm tính năng in hóa đơn dưới dạng PDF.
- [ ] Thêm API REST cho mobile/POS.
- [ ] Viết test coverage >= 80%.
- [ ] Tạo installer cho Windows bằng PyInstaller.
- [ ] Tối ưu hóa giao diện cho màn hình độ phân giải cao.
- [ ] Thêm cron job backup tự động.

PHỤ LỤC E — MẪU CẤU TRÚC THƯ MỤC ĐỀ XUẤT
QuanLyCuaHangXeMay/
├─ .venv/
├─ assets/
│  ├─ images/
│  └─ icons/
├─ database/
│  ├─ database_setup.sql
│  └─ seed_data.sql
├─ docs/
│  └─ README.md (this file)
├─ src/
│  ├─ login.py
│  ├─ admin_window.py
│  ├─ quanly_window.py
│  ├─ nhanvien_window.py
│  ├─ database_connection.py
│  └─ Function/
├─ tests/
│  ├─ test_database.py
│  └─ test_business.py
├─ requirements.txt
├─ LICENSE
└─ README.md

KẾT LUẬN NGẮN GỌN
README này cung cấp hướng dẫn toàn diện để cài đặt, chạy, bảo trì và phát triển tiếp cho hệ thống quản lý cửa hàng xe máy.
Thực hiện các bước theo thứ tự: chuẩn bị môi trường -> thiết lập DB -> cấu hình ứng dụng -> chạy -> kiểm thử.
Luôn thay đổi mật khẩu mặc định và ưu tiên hash mật khẩu trước khi triển khai.
Ghi nhận công việc phát triển và commit thay đổi cùng test phù hợp.

---
