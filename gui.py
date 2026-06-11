# gui.py - Nghi phụ trách
# BƯỚC 1: Vẽ khung giao diện tĩnh (chưa gắn logic)

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QLineEdit, QLabel,
    QTableWidget, QTableWidgetItem, QStackedWidget,
    QFormLayout, QSpinBox, QHeaderView, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hệ Thống Quản Lý Nhà Thuốc")
        self.setMinimumSize(1000, 650)

        # --- Widget trung tâm ---
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)

        # --- Thanh điều hướng bên trái ---
        nav_layout = QVBoxLayout()
        nav_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        title_label = QLabel("🏥 Nhà Thuốc")
        title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        nav_layout.addWidget(title_label)

        self.btn_nhap_thuoc  = QPushButton("📦  Nhập Thuốc Mới")
        self.btn_lap_don     = QPushButton("📋  Lập Đơn Thuốc")
        self.btn_bao_cao     = QPushButton("📊  Báo Cáo Doanh Thu")

        for btn in [self.btn_nhap_thuoc, self.btn_lap_don, self.btn_bao_cao]:
            btn.setFixedHeight(45)
            nav_layout.addWidget(btn)

        nav_layout.addStretch()
        main_layout.addLayout(nav_layout, stretch=1)

        # --- Khu vực nội dung (QStackedWidget) ---
        self.stack = QStackedWidget()
        self.stack.addWidget(self._tao_man_hinh_nhap_thuoc())   # index 0
        self.stack.addWidget(self._tao_man_hinh_lap_don())      # index 1
        self.stack.addWidget(self._tao_man_hinh_bao_cao())      # index 2
        main_layout.addWidget(self.stack, stretch=4)

        # --- Kết nối nút điều hướng ---
        self.btn_nhap_thuoc.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.btn_lap_don.clicked.connect(lambda:    self.stack.setCurrentIndex(1))
        self.btn_bao_cao.clicked.connect(lambda:    self.stack.setCurrentIndex(2))

    # ── MÀN HÌNH 1: NHẬP THUỐC MỚI ──────────────────────────────────────
    def _tao_man_hinh_nhap_thuoc(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        layout.addWidget(QLabel("📦 Nhập Thuốc Mới Vào Kho"))

        form = QFormLayout()
        self.input_ma      = QLineEdit(); self.input_ma.setPlaceholderText("VD: TH001")
        self.input_ten     = QLineEdit(); self.input_ten.setPlaceholderText("VD: Paracetamol")
        self.input_thanh_phan = QLineEdit(); self.input_thanh_phan.setPlaceholderText("VD: Acetaminophen 500mg")
        self.input_don_vi  = QLineEdit(); self.input_don_vi.setPlaceholderText("VD: viên / vỉ / hộp")
        self.input_gia     = QLineEdit(); self.input_gia.setPlaceholderText("VD: 5000")
        self.input_han     = QLineEdit(); self.input_han.setPlaceholderText("VD: 2026-12-31")
        self.input_sl      = QSpinBox(); self.input_sl.setRange(0, 99999)

        form.addRow("Mã thuốc:",         self.input_ma)
        form.addRow("Tên thuốc:",         self.input_ten)
        form.addRow("Thành phần:",        self.input_thanh_phan)
        form.addRow("Đơn vị tính:",       self.input_don_vi)
        form.addRow("Giá nhập (VNĐ):",    self.input_gia)
        form.addRow("Hạn sử dụng:",       self.input_han)
        form.addRow("Số lượng nhập:",     self.input_sl)
        layout.addLayout(form)

        self.btn_them_kho = QPushButton("✅  Thêm Vào Kho")
        self.btn_them_kho.setFixedHeight(40)
        layout.addWidget(self.btn_them_kho)
        layout.addStretch()
        return widget

    # ── MÀN HÌNH 2: LẬP ĐƠN THUỐC ───────────────────────────────────────
    def _tao_man_hinh_lap_don(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        layout.addWidget(QLabel("📋 Lập Đơn Thuốc"))

        # Ô tìm kiếm thông minh
        search_layout = QHBoxLayout()
        self.input_search = QLineEdit()
        self.input_search.setPlaceholderText("🔍 Gõ tên hoặc mã thuốc để tìm kiếm...")
        search_layout.addWidget(self.input_search)
        layout.addLayout(search_layout)

        # Bảng kết quả tìm kiếm
        layout.addWidget(QLabel("Kết quả tìm kiếm:"))
        self.bang_tim_kiem = QTableWidget(0, 5)
        self.bang_tim_kiem.setHorizontalHeaderLabels(
            ["Mã thuốc", "Tên thuốc", "Đơn vị", "Giá bán", "Tồn kho"]
        )
        self.bang_tim_kiem.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.bang_tim_kiem)

        # Nhập số lượng & thêm vào đơn
        don_layout = QHBoxLayout()
        don_layout.addWidget(QLabel("Số lượng:"))
        self.input_sl_don = QSpinBox(); self.input_sl_don.setRange(1, 9999)
        don_layout.addWidget(self.input_sl_don)
        self.btn_them_don = QPushButton("➕ Thêm Vào Đơn")
        don_layout.addWidget(self.btn_them_don)
        layout.addLayout(don_layout)

        # Bảng đơn thuốc hiện tại
        layout.addWidget(QLabel("Đơn thuốc hiện tại:"))
        self.bang_don_thuoc = QTableWidget(0, 4)
        self.bang_don_thuoc.setHorizontalHeaderLabels(
            ["Tên thuốc", "Số lượng", "Đơn giá", "Thành tiền"]
        )
        self.bang_don_thuoc.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.bang_don_thuoc)

        # Tổng tiền & nút lập đơn
        tong_layout = QHBoxLayout()
        self.label_tong = QLabel("Tổng tiền: 0 VNĐ")
        self.label_tong.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.btn_lap_don_xac_nhan = QPushButton("🧾 Xác Nhận Lập Đơn")
        self.btn_lap_don_xac_nhan.setFixedHeight(40)
        tong_layout.addWidget(self.label_tong)
        tong_layout.addStretch()
        tong_layout.addWidget(self.btn_lap_don_xac_nhan)
        layout.addLayout(tong_layout)
        return widget

    # ── MÀN HÌNH 3: BÁO CÁO DOANH THU ───────────────────────────────────
    def _tao_man_hinh_bao_cao(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel("📊 Báo Cáo Doanh Thu"))

        # Nút lọc thuốc sắp hết hạn
        self.btn_loc_het_han = QPushButton("⚠️  Lọc Thuốc Sắp Hết Hạn (Heap Sort)")
        self.btn_loc_het_han.setFixedHeight(40)
        layout.addWidget(self.btn_loc_het_han)

        # Bảng thuốc sắp hết hạn
        self.bang_het_han = QTableWidget(0, 3)
        self.bang_het_han.setHorizontalHeaderLabels(["Tên thuốc", "Hạn dùng", "Tồn kho"])
        self.bang_het_han.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.bang_het_han)

        # Placeholder biểu đồ (matplotlib sẽ gắn ở bước sau)
        placeholder = QLabel("[ Biểu đồ doanh thu theo ngày/tháng sẽ hiển thị ở đây ]")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("border: 2px dashed #aaa; padding: 60px; color: #888;")
        layout.addWidget(placeholder)
        return widget


# ── CHẠY THỬ STANDALONE ──────────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())