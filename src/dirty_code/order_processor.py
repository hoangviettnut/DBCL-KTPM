from typing import List
from src.models import Product
from src.database import SqlDatabaseConnection

class LegacyOrderProcessor:
    """
    Đây là ví dụ điển hình của một "God Object" vi phạm Clean Code:
    1. Trực tiếp khởi tạo I/O (Database) bên trong hàm -> Tight Coupling, Controllability thấp (khó mock).
    2. Logic tính toán bị chìm lẫn với truy xuất dữ liệu -> Vi phạm Single Responsibility Principle.
    3. Nhiều vòng lặp và câu lệnh IF -> Cyclomatic Complexity cao.
    4. Danh sách tham số rời rạc (Long Parameter List) thay vì một Object gom cụm.
    """
    def process_order_and_calculate_total(self, customer_id: str, products: List[Product], discount_code: str, apply_tax: bool) -> float:
        total = 0.0
        
        # ❌ LỖI 1: Gọi trực tiếp tới I/O từ bên trong hàm. (Dependency ẩn)
        # Làm cho Unit test chạy chậm (mất > 1.5s) và không thể chạy độc lập.
        db = SqlDatabaseConnection()
        customer = db.fetch_customer_by_id(customer_id)
        
        if not customer:
            raise ValueError("Customer not found")
            
        # Tính tổng tiền cơ bản
        for prod in products:
            total += prod.price
            
        # ❌ LỖI 2: Logic giảm giá phức tạp đan xen với nhau (Tăng Cyclomatic Complexity)
        if customer.is_vip:
            if total > 1000:
                total -= total * 0.15 # VIP giảm 15% cho hóa đơn lớn
            else:
                total -= total * 0.10 # VIP giảm 10% cho hóa đơn nhỏ
        else:
            if discount_code == "WELCOME5":
                total -= total * 0.05
            elif discount_code == "SUMMER10" and total > 500:
                total -= total * 0.10
        
        # Logic tính thuế
        if apply_tax:
            if customer.is_vip:
                total += total * 0.05 # VIP chịu thuế 5%
            else:
                total += total * 0.10 # Thường chịu thuế 10%
                
        # Giảm thêm dựa trên điểm thành viên (loyalty points)
        if customer.loyalty_points > 1000:
            total -= 50
            
        return max(0.0, total)
