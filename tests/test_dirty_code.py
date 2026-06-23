import time
import pytest
from src.dirty_code.order_processor import LegacyOrderProcessor
from src.models import Product

def test_legacy_order_processor_slow_execution():
    processor = LegacyOrderProcessor()
    products = [Product("P1", "Laptop", 1200.0)]
    
    start_time = time.time()
    # Phải truyền "CUST-001" để hợp lệ với dữ liệu hardcode trong DB chậm
    total = processor.process_order_and_calculate_total("CUST-001", products, "", True)
    end_time = time.time()
    
    execution_time = end_time - start_time
    
    # VIP > 1000 => giảm 15%: 1200 * 0.85 = 1020
    # Tax 5%: 1020 * 1.05 = 1071
    # Loyalty > 1000 => giảm 50: 1071 - 50 = 1021
    assert total == 1021.0
    
    # Chứng minh mã nguồn vi phạm testability vì chạy quá lâu (> 1.5s)
    assert execution_time > 1.5
    print(f"\n[Before Refactoring] Legacy Execution Time: {execution_time:.2f} seconds")
