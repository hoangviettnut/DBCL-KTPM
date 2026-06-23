from dataclasses import dataclass
from typing import List
from src.models import Product, Customer
from src.clean_code.interfaces import ICustomerRepository
from src.clean_code.strategies import VipDiscountStrategy, CouponDiscountStrategy, NoDiscountStrategy
@dataclass
class OrderPayload:
    """Áp dụng Encapsulate Field: Gom các tham số lại thành object"""
    customer_id: str
    products: List[Product]
    discount_code: str
    apply_tax: bool

class CleanOrderProcessor:
    def __init__(self, customer_repo: ICustomerRepository):
        """
        Áp dụng Dependency Injection.
        Thay vì tự khởi tạo DB bên trong, ta "tiêm" ICustomerRepository vào từ bên ngoài.
        Tăng Controllability lên mức tối đa theo sách của Saeed Parsa.
        """
        self.customer_repo = customer_repo
        
    def process_order(self, payload: OrderPayload) -> float:
        # Lấy thông tin khách hàng thông qua Interface (có thể là DB thật hoặc Stub)
        customer = self.customer_repo.fetch_customer_by_id(payload.customer_id)
        if not customer:
            raise ValueError("Customer not found")
            
        return self._calculate_total(customer, payload.products, payload.discount_code, payload.apply_tax)
        
    def _get_discount_strategy(self, customer: Customer, discount_code: str):
        if customer.is_vip:
            return VipDiscountStrategy()
        if discount_code:
            return CouponDiscountStrategy(discount_code)
        return NoDiscountStrategy()
        
    def _calculate_total(self, customer: Customer, products: List[Product], discount_code: str, apply_tax: bool) -> float:
        """
        Áp dụng Extract Method và Strategy Pattern cho logic tính toán.
        """
        total = sum(prod.price for prod in products)
        
        # Áp dụng Strategy Pattern
        discount_strategy = self._get_discount_strategy(customer, discount_code)
        total = discount_strategy.apply_discount(total)
        
        total = self._apply_tax(total, customer.is_vip, apply_tax)
        total = self._apply_loyalty_points(total, customer.loyalty_points)
        
        return max(0.0, total)
        
    def _apply_tax(self, total: float, is_vip: bool, apply_tax: bool) -> float:
        if not apply_tax:
            return total
        return total * 1.05 if is_vip else total * 1.10
        
    def _apply_loyalty_points(self, total: float, points: int) -> float:
        return total - 50 if points > 1000 else total
