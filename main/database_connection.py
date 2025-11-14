# =================================================================
# FILE: database_connection.py
# MÔ TẢ: Module kết nối SQL SERVER (Đã sửa đổi cho pyodbc)
# =================================================================

import pyodbc

class DatabaseConnection:
    def __init__(self):
        """Khởi tạo thông tin kết nối SQL Server"""
        # --- CẤU HÌNH CỦA BẠN ---
        self.server = 'KenG_Kanowaki\\LEMINHDUCSQL'  # <--- DÁN TÊN SERVER CỦA BẠN VÀO ĐÂY
        self.database = 'QUANLYCUAHANGXEMAY'
        self.driver = '{ODBC Driver 17 for SQL Server}' # Hoặc 'SQL Server' nếu lỗi driver
        self.connection = None
    
    def connect(self):
        """Tạo kết nối đến database"""
        try:
            # Kết nối dùng Windows Authentication (Không cần mật khẩu)
            conn_str = f'DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};Trusted_Connection=yes;'
            
            # Nếu bạn dùng tài khoản sa/pass thì dùng dòng dưới này (bỏ comment):
            # conn_str = f'DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};UID=sa;PWD=mat_khau_cua_ban;'
            
            self.connection = pyodbc.connect(conn_str)
            return True
        except Exception as e:
            print(f"Lỗi kết nối SQL Server: {e}")
            return False
    
    def disconnect(self):
        """Đóng kết nối database"""
        if self.connection:
            self.connection.close()
    
    def execute_query(self, query, params=None):
        """Thực thi câu lệnh INSERT, UPDATE, DELETE"""
        try:
            cursor = self.connection.cursor()
            
            # SQL Server dùng dấu ? làm placeholder thay vì %s
            query = query.replace('%s', '?')
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            self.connection.commit()
            
            # Lấy ID vừa insert (nếu có)
            try:
                cursor.execute("SELECT @@IDENTITY")
                return cursor.fetchone()[0]
            except:
                return True
                
        except Exception as e:
            print(f"Lỗi thực thi query: {e}")
            self.connection.rollback()
            return None
    
    def fetch_one(self, query, params=None):
        """Lấy một bản ghi và chuyển thành Dictionary"""
        try:
            cursor = self.connection.cursor()
            query = query.replace('%s', '?') # Đổi placeholder
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            columns = [column[0] for column in cursor.description]
            row = cursor.fetchone()
            
            if row:
                return dict(zip(columns, row))
            return None
            
        except Exception as e:
            print(f"Lỗi fetch one: {e}")
            return None
    
    def fetch_all(self, query, params=None):
        """Lấy tất cả bản ghi và chuyển thành List of Dictionaries"""
        try:
            cursor = self.connection.cursor()
            query = query.replace('%s', '?') # Đổi placeholder
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()
            
            results = []
            for row in rows:
                results.append(dict(zip(columns, row)))
            
            return results
        except Exception as e:
            print(f"Lỗi fetch all: {e}")
            return []