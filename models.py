# ==========================================
# 1. ĐỊNH NGHĨA CÁC LỚP LỖI TỰ CHẾ (CUSTOM EXCEPTIONS)
# ==========================================
class OutOfStockError(Exception):
    """Ngoại lệ xảy ra khi số lượng thuốc trong kho không đủ bán."""
    def __init__(self, message="Số lượng thuốc trong kho không đủ cung cấp!"):
        self.message = message
        super().__init__(self.message)

class ExpiredDateError(Exception):
    """Ngoại lệ xảy ra khi thuốc đã quá hạn sử dụng."""
    def __init__(self, message="Nghiêm cấm bán! Thuốc này đã hết hạn sử dụng!"):
        self.message = message
        super().__init__(self.message)