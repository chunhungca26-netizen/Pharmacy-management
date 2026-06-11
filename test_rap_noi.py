from models import ThuocKhongKeDon, ThuocKeDon, KhoThuoc, DonThuoc

print("--- KIỂM TRA RÁP NỐI LOGIC BƯỚC 2 ---")

# 1. [span_18](start_span)Khởi tạo kho thuốc (chứa Bảng băm của Nhung)[span_18](end_span)
my_kho = KhoThuoc()

# 2. Tạo các đối tượng thuốc để test
thuoc_1 = ThuocKhongKeDon("T001", "Paracetamol", "Acetaminophen", "viên", 2000, "2027-12-31")
thuoc_2 = ThuocKeDon("T002", "Amoxicillin", "Kháng sinh", "vỉ", 15000, "2026-11-20", "BS_MINH", "Uống sau khi ăn")

# 3. [span_19](start_span)[span_20](start_span)Đưa thuốc vào hệ thống bảng băm của Nhung[span_19](end_span)[span_20](end_span)
my_kho.them_thuoc_moi(thuoc_1)
my_kho.them_thuoc_moi(thuoc_2)

print("\n--- Thử nghiệm nạp chồng toán tử += ---")
# 4. [span_21](start_span)[span_22](start_span)Gọi toán tử += để chạy ngầm hàm search() và cộng dồn dữ liệu[span_21](end_span)[span_22](end_span)
my_kho += ("Paracetamol", 150)
my_kho += ("Amoxicillin", 80)

print("\n--- Thử nghiệm xuất hóa đơn tính tiền đa hình ---")
# 5. [span_23](start_span)[span_24](start_span)Lập đơn thuốc để kiểm tra tổng tiền[span_23](end_span)[span_24](end_span)
don_hang = DonThuoc("HD_TEST", "2026-06-11")
don_hang.them_thuoc_vao_don(thuoc_1, 5)  # Giá bán: 2000 * 1.10 = 2200đ / viên
don_hang.them_thuoc_vao_don(thuoc_2, 2)  # Giá bán: 15000 * 1.15 = 17250đ / vỉ

# [span_25](start_span)[span_26](start_span)Xuất hóa đơn ra terminal[span_25](end_span)[span_26](end_span)
don_hang.xuat_hoa_don()