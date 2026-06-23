import time
from .models import Customer

class SqlDatabaseConnection:
    """
    Mô phỏng một kết nối cơ sở dữ liệu tốn kém về thời gian (I/O Bound).
    Đây là nguyên nhân chính khiến mã nguồn khó Unit Test vì chạy rất chậm 
    và phụ thuộc vào môi trường (mạng, DB thật).
    """
    def __init__(self):
        # Giả lập thời gian trễ khi khởi tạo kết nối (1 giây)
        time.sleep(1.0)
        self.connected = True
        
    def fetch_customer_by_id(self, customer_id: str) -> Customer:
        # Giả lập độ trễ network I/O khi truy vấn dữ liệu (0.5 giây)
        time.sleep(0.5)
        
        # Dữ liệu hardcode để demo
        if customer_id == "CUST-001":
            return Customer(id="CUST-001", name="Alice", is_vip=True, loyalty_points=1500)
        elif customer_id == "CUST-002":
            return Customer(id="CUST-002", name="Bob", is_vip=False, loyalty_points=100)
        
        return None
