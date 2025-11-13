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

**Chúc bạn thành công với đồ án! 🎉**
