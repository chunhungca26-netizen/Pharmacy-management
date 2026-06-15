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
# 2 ĐỊNH NGHĨA LỚP CHA & CÁC LỚP CON KẾ THỪA
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
import json
import os
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
    
# ==========================================
# BƯỚC 3: HÀM ĐỌC VÀ GHI DỮ LIỆU FILE JSON
# ==========================================

def luu_du_lieu_json(kho_thuoc, file_path="database.json"):
    """
    Duyệt qua bảng băm của Nhung và ghi toàn bộ thuốc vào file database.json.
    """
    du_lieu_kho = []
    
    # Duyệt qua từng bucket trong mảng bucket_array của bảng băm để quét các Node
    for current in kho_thuoc.kho_du_lieu.bucket_array:
        while current:
            thong_tin = current.value  # Lấy dict {"doi_tuong": thuoc, "so_luong": X}
            thuoc = thong_tin["doi_tuong"]
            
            # Chuyển các thuộc tính đối tượng Object thành dict để lưu vào JSON
            data_thuoc = {
                "loai": thuoc.__class__.__name__,
                "ma_thuoc": thuoc.ma_thuoc,
                "ten_thuoc": thuoc.ten_thuoc,
                "thanh_phan": thuoc.thanh_phan,
                "don_vi_tinh": thuoc.don_vi_tinh,
                "gia_nhap": thuoc.gia_nhap,
                "han_su_dung": thuoc.han_su_dung,
                "so_luong": thong_tin["so_luong"]
            }
            
            # Nếu là loại Thuốc Kê Đơn thì lưu thêm 2 thuộc tính đặc thù riêng
            if data_thuoc["loai"] == "ThuocKeDon":
                data_thuoc["ma_bac_si"] = thuoc.ma_bac_si
                data_thuoc["canh_bao_lieu_dung"] = thuoc.canh_bao_lieu_dung
                
            du_lieu_kho.append(data_thuoc)
            current = current.next

    # Ghi toàn bộ danh sách dữ liệu vào file JSON cấu trúc rõ ràng
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(du_lieu_kho, f, ensure_ascii=False, indent=4)
    print(f"[FILE] Đã sao lưu dữ liệu kho thuốc vào '{file_path}' thành công!")


def doc_du_lieu_json(kho_thuoc, file_path="database.json"):
    """
    Đọc dữ liệu từ file JSON và tái tạo lại đối tượng thuốc nạp vào bảng băm.
    """
    if not os.path.exists(file_path):
        print(f"[FILE] Chưa có dữ liệu cũ '{file_path}', khởi tạo kho thuốc trống.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        try:
            du_lieu_kho = json.load(f)
        except json.JSONDecodeError:
            print(f"[FILE] Tệp tin '{file_path}' trống hoặc sai định dạng.")
            return

    # Khôi phục các lớp Object từ chuỗi văn bản trong JSON
    from models import ThuocKhongKeDon, ThuocKeDon, ThucPhamChucNang

    for item in du_lieu_kho:
        # Nhận diện loại thuốc để khởi tạo đúng lớp con (Tính đa hình)
        if item["loai"] == "ThuocKeDon":
            thuoc = ThuocKeDon(
                item["ma_thuoc"], item["ten_thuoc"], item["thanh_phan"], 
                item["don_vi_tinh"], item["gia_nhap"], item["han_su_dung"],
                item["ma_bac_si"], item["canh_bao_lieu_dung"]
            )
        elif item["loai"] == "ThuocKhongKeDon":
            thuoc = ThuocKhongKeDon(
                item["ma_thuoc"], item["ten_thuoc"], item["thanh_phan"], 
                item["don_vi_tinh"], item["gia_nhap"], item["han_su_dung"]
            )
        else:
            thuoc = ThucPhamChucNang(
                item["ma_thuoc"], item["ten_thuoc"], item["thanh_phan"], 
                item["don_vi_tinh"], item["gia_nhap"], item["han_su_dung"]
            )
        
        # Đưa thuốc trở lại bảng băm và nạp lại số lượng tồn kho cũ bằng toán tử +=
        kho_thuoc.them_thuoc_moi(thuoc)
        kho_thuoc += (thuoc.ten_thuoc, item["so_luong"])
        
    print(f"[FILE] Phục hồi toàn bộ dữ liệu từ '{file_path}' lên hệ thống thành công!")