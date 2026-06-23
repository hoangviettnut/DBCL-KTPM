from abc import ABC, abstractmethod

class IDiscountStrategy(ABC):
    """Giao diện chung cho các chiến lược giảm giá (Strategy Pattern)"""
    @abstractmethod
    def apply_discount(self, total: float) -> float:
        pass

class VipDiscountStrategy(IDiscountStrategy):
    """Chiến lược giảm giá dành riêng cho khách VIP"""
    def apply_discount(self, total: float) -> float:
        if total > 1000:
            return total - (total * 0.15)
        return total - (total * 0.10)

class CouponDiscountStrategy(IDiscountStrategy):
    """Chiến lược giảm giá dựa trên mã Coupon"""
    def __init__(self, coupon_code: str):
        self.coupon_code = coupon_code
        
    def apply_discount(self, total: float) -> float:
        if self.coupon_code == "WELCOME5":
            return total - (total * 0.05)
        elif self.coupon_code == "SUMMER10" and total > 500:
            return total - (total * 0.10)
        return total

class NoDiscountStrategy(IDiscountStrategy):
    """Chiến lược không giảm giá"""
    def apply_discount(self, total: float) -> float:
        return total
