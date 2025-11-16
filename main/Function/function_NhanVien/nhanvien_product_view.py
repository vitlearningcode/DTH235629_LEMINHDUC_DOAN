import tkinter as tk
from tkinter import ttk
import os 

class NhanVienProductView:
    """
    Lớp chịu trách nhiệm vẽ màn hình 'Xem sản phẩm'.
    Khởi tạo với parent_view (instance của NhanVien) để truy cập db, sales_logic, content_frame...
    """
    def __init__(self, parent_view):
        self.parent = parent_view
        # _product_images dùng để giữ tham chiếu, tránh bị garbage collector xóa ảnh
        self._product_images = []
        
        # Đường dẫn tới thư mục chứa ảnh SanPham
        self.resource_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "..", "..", "resource", "SanPham"
        ))
        # Tạo thư mục nếu chưa tồn tại
        if not os.path.exists(self.resource_path):
            try:
                os.makedirs(self.resource_path)
            except Exception as e:
                print(f"Không thể tạo thư mục resource: {e}")

    def show(self):
        """Vẽ UI sản phẩm (gọi từ nhanvien_window.view_products)"""
        self.parent.clear_content()
        tk.Label(
            self.parent.content_frame,
            text="DANH SÁCH SẢN PHẨM",
            font=("Arial", 18, "bold"),
            bg=self.parent.bg_color
        ).pack(pady=10)

        container = tk.Frame(self.parent.content_frame, bg=self.parent.bg_color)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        canvas = tk.Canvas(container, bg=self.parent.bg_color, highlightthickness=0)
        v_scroll = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=v_scroll.set)

        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        inner_frame = tk.Frame(canvas, bg=self.parent.bg_color)
        window_id = canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        def _on_canvas_configure(event):
            canvas.itemconfig(window_id, width=event.width)
        canvas.bind("<Configure>", _on_canvas_configure)

        def _on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        inner_frame.bind("<Configure>", _on_configure)

        def _on_mousewheel(event):
            if event.delta:
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            else:
                if event.num == 4:
                    canvas.yview_scroll(-1, "units")
                elif event.num == 5:
                    canvas.yview_scroll(1, "units")

        # chỉ bind canvas cho cuộn ở vùng này
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        canvas.bind_all("<Button-4>", _on_mousewheel)
        canvas.bind_all("<Button-5>", _on_mousewheel)

        self._product_images.clear()

        def populate_product_grid(products):
            """Vẽ lưới sản phẩm từ dữ liệu đã tải"""
            for w in inner_frame.winfo_children():
                w.destroy()
            self._product_images.clear()

            cols = 4 # Số cột hiển thị sản phẩm
            padx = 20
            pady = 15

            for idx, p in enumerate(products):
                row = idx // cols
                col = idx % cols

                card = tk.Frame(inner_frame, width=180, height=220, bg="white", bd=1, relief=tk.RIDGE)
                card.grid(row=row, column=col, padx=padx, pady=pady, sticky="n")
                card.grid_propagate(False) # Ngăn card co lại

                img_frame = tk.Frame(card, width=150, height=150, bg="white")
                img_frame.pack(pady=(8,4))
                img_frame.pack_propagate(False)

                img_label = tk.Label(img_frame, bg="white")
                img_label.pack(expand=True)

                img_obj = None
                img_path = p.get("image_path") # Lấy đường dẫn đã được xây dựng

                # Cố gắng tải ảnh bằng PIL (ưu tiên)
                if img_path and os.path.exists(img_path):
                    try:
                        from PIL import Image, ImageTk
                        img = Image.open(img_path).convert("RGBA")
                        img = img.resize((150, 150), Image.LANCZOS)
                        img_obj = ImageTk.PhotoImage(img)
                    except Exception as e_pil:
                        try:
                            img_obj = tk.PhotoImage(file=img_path)
                        except Exception as e_tk:
                            img_obj = None
                
                # Nếu không có ảnh (kể cả default) hoặc tải lỗi, hiển thị placeholder
                if img_obj:
                    img_label.configure(image=img_obj)
                    self._product_images.append(img_obj) # Giữ tham chiếu
                else:
                    ph = tk.Canvas(img_frame, width=150, height=150, bg="#f0f0f0", highlightthickness=0)
                    ph.create_rectangle(2, 2, 148, 148, outline="#cccccc")
                    ph.create_text(75, 75, text="No Image", fill="#666666")
                    ph.pack(fill=tk.BOTH, expand=True)

                # Hiển thị Tên
                name = p.get("name", "Tên sản phẩm")
                tk.Label(card, text=name, bg="white", wraplength=170, justify="center", font=("Arial", 10, "bold")).pack(pady=(4,0))

                # Hiển thị Giá (Đã được format từ _load_products)
                price = p.get("price", "0")
                price_text = f"{price} VNĐ"
                tk.Label(card, text=price_text, bg="white", fg="red", font=("Arial", 10, "bold")).pack(pady=(2,6))

            for c in range(cols):
                inner_frame.grid_columnconfigure(c, weight=1, minsize=180)

        
        products = self._load_products()
        populate_product_grid(products)

    def _load_products(self):
        """Lấy danh sách sản phẩm từ CSDL và XÂY DỰNG đường dẫn ảnh"""
        products = []
        try:
            # Truy cập CSDL thông qua self.parent (NhanVien)
            if hasattr(self.parent, "db"):
                      
                query = """
                    SELECT MaSanPham, TenSanPham, GiaBan, SoLuongTon
                    FROM SanPham
                    ORDER BY TenSanPham
                """
                               

                rows = self.parent.db.fetch_all(query)
                
             
                    
                if rows:
                    for r in rows:
                        # Format giá bán ngay tại đây
                        price_formatted = f"{r['GiaBan']:,.0f}" if r['GiaBan'] is not None else "0"
                        product_id = r['MaSanPham']
                        
                        # TỰ XÂY DỰNG ĐƯỜNG DẪN ẢNH (GIỐNG FILE QUANLY)
                        image_path = os.path.join(self.resource_path, f"{product_id}.png")
                        
                        # Nếu ảnh SP không tồn tại, dùng ảnh default
                        if not os.path.exists(image_path):
                            image_path = os.path.join(self.resource_path, "default_product.png")

                        products.append({
                            "id": product_id,
                            "name": r['TenSanPham'],
                            "price": price_formatted, # Giá đã format
                            "image_path": image_path, # Đường dẫn ảnh (ĐÃ SỬA)
                            "stock": r['SoLuongTon']
                        })
                    return products
            
            # Nếu không tìm thấy self.parent.db
            return []

        except Exception as e:
            # Lỗi này có thể xảy ra nếu CSDL vẫn sai tên cột
            print(f"--- [DEBUG] LỖI NẶNG TRONG _load_products: {e}")
            return [] # Trả về list rỗng nếu có lỗi
