=================================================================
FILE: README.md
HƯỚNG DẪN CÀI ĐẶT VÀ SỬ DỤNG HỆ THỐNG
=================================================================
HỆ THỐNG QUẢN LÝ CỬA HÀNG XE MÁY
📋 MÔ TẢ DỰ ÁN
Hệ thống quản lý cửa hàng xe máy phát triển bằng Python Tkinter với cơ sở dữ liệu SQL Server. Hệ thống hỗ trợ 3 vai trò người dùng với phân quyền rõ ràng:

Admin (Chủ cửa hàng): Toàn quyền quản lý tất cả các chức năng

QuanLy (Quản lý): Chỉ xem thông tin và có quyền chấm công

NhanVien (Nhân viên): Lập hóa đơn bán hàng, dịch vụ sửa chữa

🎨 ĐẶC ĐIỂM GIAO DIỆN
Màu sắc chủ đạo: Xanh da trời (#87CEEB, #4682B4, #5F9EA0)

Thiết kế: Đơn giản, dễ dùng, thích hợp cho nhân viên phổ thông, người mới học Python

Responsive: Tự động co giãn giao diện

📦 YÊU CẦU HỆ THỐNG
Phần mềm bắt buộc:
Python 3.8+

SQL Server 2017+ (Express hoặc bản đủ tính năng)

SQL Server Management Studio (SSMS)

ODBC Driver 17 for SQL Server

Thư viện Python:
bash
pip install pyodbc
pip install pillow
pip install openpyxl
pip install tkinter      # Thường đã có sẵn với Python mặc định
🚀 HƯỚNG DẪN CÀI ĐẶT
Bước 1: Cài đặt SQL Server
Tải và cài “SQL Server” và SSMS

Tạo user “sa” hoặc account riêng để kết nối

Bước 2: Tạo Database
Mở SSMS hoặc cmd line

Chạy script database_setup.sql để tạo database và các bảng:

sql
:r database_setup.sql
Hoặc copy toàn bộ nội dung script, dán vào SSMS rồi chạy

Bước 3: Cấu hình kết nối
Mở file database_connection.py và chỉnh thông tin:

python
self.server = 'localhost\\\\SQLEXPRESS'
self.database = 'QUANLYCUAHANGXEMAY'
self.username = 'sa'                 # đổi nếu dùng username khác
self.password = '...'                # mật khẩu SQL Server
self.driver = 'ODBC Driver 17 for SQL Server'
Bước 4: Cài đặt thư viện Python bắt buộc
bash
pip install pyodbc pillow openpyxl
Bước 5: Chạy chương trình
bash
python login.py
👥 TÀI KHOẢN MẶC ĐỊNH
Vai trò	Tên đăng nhập	Mật khẩu	Quyền hạn
Admin	admin	123456	Toàn quyền
Quản lý	quanly01	123456	Xem + Chấm công
Nhân viên	nhanvien01	123456	Bán hàng, nhập khách mới
📁 CẤU TRÚC FILE
text
QuanLyCuaHangXeMay/
├── database_setup.sql          # Script tạo database SQL Server
├── database_connection.py      # Module kết nối pyodbc
├── login.py                    # Form đăng nhập
├── admin_window.py             # Giao diện Admin
├── quanly_window.py            # Giao diện Quản lý
├── nhanvien_window.py          # Giao diện Nhân viên
├── Function/                   # Tất cả logic nghiệp vụ (Admin/NhanVien/QuanLy)
├── README.md                   # File hướng dẫn này
🗄️ CẤU TRÚC DATABASE
Bảng chính:
NguoiDung: Quản lý tài khoản + phân quyền

SanPham: Danh mục xe máy

PhuTung: Phụ tùng linh kiện

KhachHang: Thông tin khách

HoaDon: Hóa đơn bán/phiếu bảo hành

PhieuNhapKho: Nhập hàng kho

ChamCong: Bảng chấm công nhân viên

KhuyenMai: Chương trình khuyến mại

Trigger chính:
✅ Tự động cập nhật tồn kho khi nhập/bán/sp xuất kho

✅ Tự động kiểm tra số lượng tồn kho trước khi bán (không cho phép số âm)

✅ Tự động update tổng tiền hóa đơn/phiếu nhập

🔧 CHỨC NĂNG CHI TIẾT
🔑 Đăng nhập & Phân quyền
Đăng nhập với kiểm tra role (Admin/QuanLy/NhanVien)

Trạng thái tài khoản, reset password

👨‍💼 Admin (Chủ cửa hàng)
Quản lý nhân viên (CRUD)

Quản lý sản phẩm (CRUD)

Quản lý phụ tùng (CRUD)

Quản lý kho, nhập/xuất kho

Quản lý khuyến mãi, khách hàng, hóa đơn, chấm công

Báo cáo, xuất dữ liệu Excel/PDF

👔 Quản lý (QuanLy)
Xem thông tin tất cả module

Chấm công cho nhân viên

👨‍💻 Nhân viên (NhanVien)
Lập hóa đơn bán hàng

Thêm khách mới

Lập phiếu sửa chữa/bảo dưỡng

Xem lịch sử hóa đơn cá nhân

Logic kho: tự động kiểm tra tồn kho, không cho phép bán khi hết hàng

🔒 BẢO MẬT
Mật khẩu lưu plain text (khuyến nghị mã hoá hash)

Phân quyền rõ ràng cho các vai trò

Kiểm tra trạng thái active/trạng thái tài khoản

📊 RÀNG BUỘC & TRIGGER DỮ LIỆU
Ràng buộc SQL:
sql
- SoLuongTon >= 0           -- Không cho phép tồn kho âm
- GiaBan > 0                -- Giá trị dương
- NgayKetThuc >= NgayBatDau -- Bảo hành hợp lệ
- UNIQUE các trường chính/tài khoản/login
Trigger mẫu:
sql
- trgAfterNhapSanPham: update tồn kho khi nhập hàng
- trgBeforeBanSanPham: kiểm tra tồn kho trước khi bán
- trgAfterInsertHoaDon: tự động tổng hợp hóa đơn
🎯 HƯỚNG DẪN SỬ DỤNG
Đăng nhập lần đầu:

Chạy python login.py

Đăng nhập admin / 123456

Tuỳ vai trò, giao diện sẽ tự động chuyển chế độ

Quy trình bán hàng (Nhân viên):

Đăng nhập account Nhân viên

Nhập SĐT khách hoặc thêm mới

Chọn xe, phụ tùng, số lượng

Thanh toán

Hệ thống auto trừ tồn kho, in hóa đơn

Quy trình nhập kho (Admin):

Vào “Quản lý kho”

Thêm phiếu nhập mới

Cập nhật danh sách sản phẩm + số lượng

Lưu phiếu nhập kho

Chấm công (Quản lý):

Chọn menu “Chấm công”

Nhập ngày, nhân viên, trạng thái (đi làm/vắng mặt…)

Lưu lại

🐛 LỖI & GIẢI PHÁP
Lỗi kết nối SQL Server:

text
Error: ('08001', '[08001] [Microsoft][ODBC Driver 17 for SQL Server]...')
Kiểm tra SQL Server đã chạy, ODBC driver đã cài, connection string đúng

Lỗi module pyodbc:

text
ModuleNotFoundError: No module named 'pyodbc'
Cài lại:

bash
pip install pyodbc
Lỗi trigger:

text
Không đủ tồn kho để bán!
Nhập thêm hàng trước khi tạo hóa đơn bán

📝 GHI CHÚ
Code dễ hiểu, dễ bảo trì, phù hợp học sinh-sinh viên

Dễ mở rộng thêm nghiệp vụ, báo cáo

Database kèm dữ liệu mẫu demo

🔄 PHÁT TRIỂN THÊM
Báo cáo có biểu đồ (Matplotlib)

Xuất hóa đơn, báo cáo PDF

Gửi email/SMS nhắc bảo hành

Backup/Restore database tự động

Tích hợp thanh toán điện tử (VNPay,...)

📞 HỖ TRỢ
Nếu gặp khó khăn:

Kiểm tra các bước cài đặt

Kiểm tra kết nối SQL Server, ODBC còn hoạt động

Kiểm tra lại account và phân quyền

Đọc lỗi console, xem hướng dẫn trong README

📚 TÀI LIỆU THAM KHẢO
Python Tkinter Documentation

SQL Server Documentation

PyODBC Documentation

