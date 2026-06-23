import time
import pytest
from src.clean_code.order_processor import CleanOrderProcessor, OrderPayload
from src.clean_code.interfaces import ICustomerRepository
from src.models import Product, Customer

class StubCustomerRepository(ICustomerRepository):
    """
    Test Double (Stub): Trả về dữ liệu giả định ngay lập tức.
    Kỹ thuật này giúp bẻ gãy sự phụ thuộc vào Database thật,
    tăng Controllability và Observability.
    """
    def fetch_customer_by_id(self, customer_id: str) -> Customer:
        if customer_id == "CUST-001":
            return Customer(id="CUST-001", name="Alice", is_vip=True, loyalty_points=1500)
        return None

def test_clean_order_processor_fast_execution():
    # Sử dụng Dependency Injection với Stub
    stub_repo = StubCustomerRepository()
    processor = CleanOrderProcessor(stub_repo)
    
    products = [Product("P1", "Laptop", 1200.0)]
    payload = OrderPayload(customer_id="CUST-001", products=products, discount_code="", apply_tax=True)
    
    start_time = time.time()
    total = processor.process_order(payload)
    end_time = time.time()
    
    execution_time = end_time - start_time
    
    assert total == 1021.0
    
    # Chứng minh tính kiểm thử cao vì chạy cực nhanh (thường < 0.01s)
    assert execution_time < 0.1
    print(f"\n[After Refactoring] Clean Code Execution Time: {execution_time:.5f} seconds")
