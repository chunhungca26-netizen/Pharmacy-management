from hashtable import HashTableCaiDat

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
    
# ==========================================
# 3. LỚP ĐƠN THUỐC (DON THUOC)
# ==========================================
class DonThuoc:
    def __init__(self, ma_don, ngay_ke):
        self.ma_don = ma_don
        self.ngay_ke = ngay_ke
        self.danh_sach_thuoc = []  # Lưu các tuple: (đối tượng_thuoc, so_luong)

    def them_thuoc_vao_don(self, duoc_pham, so_luong):
        """Kiểm tra hạn dùng trước khi thêm, nếu hết hạn thì báo lỗi ngay."""
        if not duoc_pham.kiem_tra_han_dung():
            raise ExpiredDateError(f"Không thể bán! Thuốc {duoc_pham.ten_thuoc} đã hết hạn!")
        self.danh_sach_thuoc.append((duoc_pham, so_luong))

    def tinh_tong_tien(self):
        """Tính tổng tiền bằng cách gọi hàm tinh_gia_ban() đa hình của từng lớp con."""
        tong_tien = 0
        for thuoc, so_luong in self.danh_sach_thuoc:
            tong_tien += thuoc.tinh_gia_ban() * so_luong
        return tong_tien

    def xuat_hoa_don(self):
        """In hóa đơn ra màn hình để kiểm tra nhanh."""
        print(f"--- HÓA ĐƠN: {self.ma_don} ---")
        print(f"Ngày kê: {self.ngay_ke}")
        for thuoc, so_luong in self.danh_sach_thuoc:
            print(f"- {thuoc.ten_thuoc} x{so_luong} | Đơn giá: {thuoc.tinh_gia_ban():.2f}")
        print(f"Tổng tiền cần thanh toán: {self.tinh_tong_tien():.2f}")
        
# ==========================================
# BƯỚC 2: CÀI ĐẶT KHO THUỐC VÀ TOÁN TỬ NẠP CHỒNG +=
# ==========================================
class KhoThuoc:
    def __init__(self):
        # [span_8](start_span)[span_9](start_span)Khởi tạo Bảng băm tự cài đặt của Nhung[span_8](end_span)[span_9](end_span)
        self.kho_du_lieu = HashTableCaiDat()

    def them_thuoc_moi(self, thuoc):
        """Hàm hỗ trợ khởi tạo thuốc vào kho với số lượng ban đầu bằng 0"""
        # [span_10](start_span)[span_11](start_span)Lưu vào bảng băm: Key là Tên thuốc, Value là một dict chứa đối tượng và số lượng[span_10](end_span)[span_11](end_span)
        self.kho_du_lieu.insert(thuoc.ten_thuoc, {"doi_tuong": thuoc, "so_luong": 0})

    def __iadd__(self, other):
        """
        [span_12](start_span)[span_13](start_span)Nạp chồng toán tử += để cộng dồn số lượng thuốc vào kho[span_12](end_span)[span_13](end_span).
        Cú pháp sử dụng: my_kho += ("Paracetamol", 100)
        """
        # other nhận vào một tuple gồm: (ten_thuoc, so_luong_them)
        ten_thuoc, so_luong_them = other
        
        # [span_14](start_span)[span_15](start_span)Gọi hàm search() từ file hashtable.py của Nhung để tra cứu thuốc[span_14](end_span)[span_15](end_span)
        thong_tin_thuoc = self.kho_du_lieu.search(ten_thuoc)
        
        if thong_tin_thuoc:
            # [span_16](start_span)[span_17](start_span)Nếu tìm thấy thuốc trong bảng băm, tiến hành cộng dồn số lượng[span_16](end_span)[span_17](end_span)
            thong_tin_thuoc["so_luong"] += so_luong_them
            print(f"[KHO] Đã cộng thêm {so_luong_them} vào thuốc '{ten_thuoc}'.")
        else:
            print(f"[LỖI] Không tìm thấy thuốc '{ten_thuoc}' trong kho!")
            
        return self