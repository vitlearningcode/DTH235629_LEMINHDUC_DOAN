# main/Function/function_Admin/admin_reports_logic.py

import tkinter as tk
from tkinter import messagebox

class AdminReportsLogic:
    def __init__(self, view):
        self.view = view
        self.db = view.db

    def report_revenue(self):
        # (Giữ nguyên logic cửa sổ con nhưng cần chỉnh query bên trong nếu có)
        dialog = tk.Toplevel(self.view.window)
        dialog.title("Báo cáo doanh thu")
        dialog.geometry("800x600")
        tk.Label(dialog, text="Báo cáo doanh thu (Demo)", font=("Arial", 16)).pack(pady=20)
        
    def report_inventory(self): 
        messagebox.showinfo("Info", "Báo cáo tồn kho")
    
    def report_employee_performance(self): 
        messagebox.showinfo("Info", "Báo cáo nhân viên")
    
    def report_top_products(self): 
        messagebox.showinfo("Info", "Báo cáo Top sản phẩm")
    
    def report_loyal_customers(self): 
        messagebox.showinfo("Info", "Báo cáo Khách hàng")
    
    def report_debt(self): 
        messagebox.showinfo("Info", "Báo cáo công nợ")