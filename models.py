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
        
from datetime import datetime

# ==========================================
# 2. ĐỊNH NGHĨA LỚP CHA & CÁC LỚP CON KẾ THỪA
# ==========================================
class DuocPham:
    def __init__(self, ma_thuoc, ten_thuoc, thanh_phan, don_vi_tinh, gia_nhap, han_su_dung):
        self.ma_thuoc = ma_thuoc          # Mã thuốc
        self.ten_thuoc = ten_thuoc        # Tên thuốc
        self.thanh_phan = thanh_phan      # Thành phần dược lý
        self.don_vi_tinh = don_vi_tinh    # viên, vỉ, hộp...
        self.gia_nhap = gia_nhap          # Giá nhập kho
        self.han_su_dung = han_su_dung    # Chuỗi định dạng 'YYYY-MM-DD'

    def kiem_tra_han_dung(self):
        """So sánh ngày hết hạn với ngày hiện tại."""
        ngay_hien_tai = datetime.now().date()
        ngay_het_han = datetime.strptime(self.han_su_dung, "%Y-%m-%d").date()
        return ngay_het_han >= ngay_hien_tai

    def tinh_gia_ban(self):
        """Hàm ảo để các lớp con ghi đè đa hình."""
        pass

class ThuocKeDon(DuocPham):
    def __init__(self, ma_thuoc, ten_thuoc, thanh_phan, don_vi_tinh, gia_nhap, han_su_dung, ma_bac_si, canh_bao_lieu_dung):
        super().__init__(ma_thuoc, ten_thuoc, thanh_phan, don_vi_tinh, gia_nhap, han_su_dung)
        self.ma_bac_si = ma_bac_si                  # Thuộc tính riêng
        self.canh_bao_lieu_dung = canh_bao_lieu_dung # Thuộc tính riêng

    def tinh_gia_ban(self):
        # Thuốc kê đơn tính thêm VAT và phí quản lý (Ví dụ: +15%)
        return self.gia_nhap * 1.15

class ThuocKhongKeDon(DuocPham):
    def tinh_gia_ban(self):
        # Thuốc không kê đơn lời 10%
        return self.gia_nhap * 1.10

class ThucPhamChucNang(DuocPham):
    def tinh_gia_ban(self):
        # Thực phẩm chức năng lời 8%
        return self.gia_nhap * 1.08