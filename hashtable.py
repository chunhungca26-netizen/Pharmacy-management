# hashtable.py
import datetime

class Node:
    """Nút chứa dữ liệu phục vụ cơ chế xử lý trùng mã băm bằng Linked List."""
    def __init__(self, key, value):
        self.key = key          # Mã thuốc hoặc tên thuốc đã chuẩn hóa
        self.value = value      # Đối tượng thuốc (DuocPham, ThuocKeDon,...)
        self.next = None        # Con trỏ trỏ đến Node tiếp theo


class HashTableCaiDat:
    """Bảng băm thuần tự cài đặt, kích thước cố định, không dùng dict của Python."""
    def __init__(self, size=1000):
        self.size = size
        self.bucket_array = [None] * self.size
    
    def _hash_function(self, key):
        """Hàm băm đa thức (Polynomial Rolling Hash) tối ưu, giảm xung đột."""
        hash_value = 0
        p = 31
        for char in str(key):
            hash_value = (hash_value * p + ord(char)) % self.size
        return hash_value

    def insert(self, key, value):
        index = self._hash_function(key)
        
        # 1. Kiểm tra xem thuốc này đã có trong kho chưa để cập nhật
        current = self.bucket_array[index]
        while current:
            if current.key == key:
                current.value = value  # Cập nhật thông tin/số lượng mới
                return                 # THOÁT HÀM NGAY, không chạy xuống dưới nữa
            current = current.next
            
        # 2. Nếu chưa có, chèn Node mới thẳng vào ĐẦU danh sách liên kết (Đạt tốc độ O(1))
        new_node = Node(key, value)
        new_node.next = self.bucket_array[index]
        self.bucket_array[index] = new_node

    def search(self, key):
        """Tìm kiếm thuốc cực nhanh từ mã/tên thuốc. Trả về Object hoặc None."""
        index = self._hash_function(key)
        current = self.bucket_array[index]
        
        while current:
            if current.key == key:
                return current.value
            current = current.next
        return None

    # --- Các hàm thuật toán của Nhung (Đã đồng bộ thuộc tính với Thư) ---
    def _parse_date(self, date_str):
        if isinstance(date_str, datetime.date): return date_str
        try: return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except: return datetime.datetime.strptime(date_str, "%d/%m/%Y").date()

    def _heapify(self, arr, n, i):
        smallest = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n and self._parse_date(arr[left].han_su_dung) < self._parse_date(arr[smallest].han_su_dung):
            smallest = left
        if right < n and self._parse_date(arr[right].han_su_dung) < self._parse_date(arr[smallest].han_su_dung):
            smallest = right
        if smallest != i:
            arr[i], arr[smallest] = arr[smallest], arr[i]
            self._heapify(arr, n, smallest)

    def heap_sort(self, list_thuoc):
        arr = list(list_thuoc)
        n = len(arr)
        for i in range(n // 2 - 1, -1, -1):
            self._heapify(arr, n, i)
        ket_qua = []
        while arr:
            ket_qua.append(arr[0])
            if len(arr) > 1:
                arr[0] = arr.pop()
                self._heapify(arr, len(arr), 0)
            else:
                arr.pop()
        return ket_qua

    def loc_de_quy_thanh_phan(self, danh_sach_thuoc, tu_khoa_muc_tieu, index=0, ket_qua=None):
        """Đệ quy lọc thuốc theo tên hoặc thành phần dược lý (Thay cho thuộc tính danh_muc bị thiếu)"""
        if ket_qua is None: ket_qua = []
        if index >= len(danh_sach_thuoc): return ket_qua
        
        thuoc = danh_sach_thuoc[index]
        ten = getattr(thuoc, 'ten_thuoc', '').lower()
        tp = getattr(thuoc, 'thanh_phan', '').lower()
        
        if tu_khoa_muc_tieu.lower() in ten or tu_khoa_muc_tieu.lower() in tp:
            ket_qua.append(thuoc)
            
        return self.loc_de_quy_thanh_phan(danh_sach_thuoc, tu_khoa_muc_tieu, index + 1, ket_qua)