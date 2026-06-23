# gui.py - Bảo Nghi phụ trách - BƯỚC 4 (Giao diện nâng cấp)

import sys
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QLineEdit, QLabel,
    QTableWidget, QTableWidgetItem, QStackedWidget,
    QFormLayout, QSpinBox, QHeaderView, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

from hashtable import HashTableCaiDat
from models import (
    KhoThuoc, ThuocKhongKeDon,
    OutOfStockError, ExpiredDateError,
    luu_du_lieu_json, doc_du_lieu_json
)

# ══════════════════════════════════════════════
#  BẢNG MÀU & STYLE TOÀN APP
# ══════════════════════════════════════════════
PRIMARY      = "#1565C0"   # Xanh biển đậm (header, active nav)
PRIMARY_DARK = "#0D47A1"   # Xanh đậm hơn (hover)
PRIMARY_LITE = "#E3F2FD"   # Xanh cực nhạt (nền form, row lẻ)
ACCENT       = "#42A5F5"   # Xanh nhạt (icon, border focus)
SUCCESS      = "#2E7D32"   # Xanh lá (thành công)
WARNING      = "#E65100"   # Cam đậm (cảnh báo)
DANGER       = "#C62828"   # Đỏ (hết hạn)
YELLOW_WARN  = "#F9A825"   # Vàng (sắp hết)
WHITE        = "#FFFFFF"
BG           = "#F5F9FF"   # Nền app xanh cực nhạt
NAV_BG       = "#0D47A1"   # Nền sidebar
TEXT_MAIN    = "#0D1B2A"   # Chữ chính
TEXT_MUTED   = "#5C7A99"   # Chữ phụ
BORDER       = "#BBDEFB"   # Viền nhạt

FONT_TITLE   = QFont("Segoe UI", 13, QFont.Weight.Bold)
FONT_SECTION = QFont("Segoe UI", 10, QFont.Weight.Bold)
FONT_BODY    = QFont("Segoe UI", 9)
FONT_TOTAL   = QFont("Segoe UI", 12, QFont.Weight.Bold)

STYLE_APP = f"""
QMainWindow, QWidget {{ background: {BG}; }}

/* ── Sidebar ── */
#sidebar {{ background: {NAV_BG}; border-right: 3px solid {PRIMARY}; }}
#sidebar QLabel {{ color: {WHITE}; padding: 8px 16px; }}

/* ── Nav buttons ── */
#navBtn {{
    background: transparent;
    color: {WHITE};
    border: none;
    border-left: 4px solid transparent;
    text-align: left;
    padding: 14px 20px;
    font-size: 10pt;
    font-family: 'Segoe UI';
    border-radius: 0;
}}
#navBtn:hover {{
    background: rgba(255,255,255,0.12);
    border-left: 4px solid {ACCENT};
}}
#navBtn[active="true"] {{
    background: {PRIMARY};
    border-left: 4px solid {ACCENT};
    font-weight: bold;
}}

/* ── Section title ── */
#sectionTitle {{
    color: {PRIMARY};
    font-size: 13pt;
    font-family: 'Segoe UI';
    font-weight: bold;
    padding: 4px 0 8px 0;
    border-bottom: 2px solid {ACCENT};
    margin-bottom: 8px;
}}

/* ── Card (khung trắng) ── */
#card {{
    background: {WHITE};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 18px;
}}

/* ── Form label ── */
QFormLayout QLabel {{
    color: {TEXT_MAIN};
    font-family: 'Segoe UI';
    font-size: 9pt;
    font-weight: bold;
    min-width: 130px;
}}

/* ── Input ── */
QLineEdit, QSpinBox {{
    background: {WHITE};
    border: 1.5px solid {BORDER};
    border-radius: 6px;
    padding: 7px 10px;
    font-family: 'Segoe UI';
    font-size: 9pt;
    color: {TEXT_MAIN};
    min-height: 22px;
}}
QLineEdit:focus, QSpinBox:focus {{
    border: 1.5px solid {ACCENT};
    background: {PRIMARY_LITE};
}}
QLineEdit::placeholder {{ color: {TEXT_MUTED}; }}

/* ── Nút chính (xanh) ── */
#btnPrimary {{
    background: {PRIMARY};
    color: {WHITE};
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-family: 'Segoe UI';
    font-size: 10pt;
    font-weight: bold;
    min-height: 40px;
}}
#btnPrimary:hover {{ background: {PRIMARY_DARK}; }}
#btnPrimary:pressed {{ background: #0A3880; }}

/* ── Nút phụ (viền xanh) ── */
#btnSecondary {{
    background: {WHITE};
    color: {PRIMARY};
    border: 2px solid {PRIMARY};
    border-radius: 8px;
    padding: 8px 18px;
    font-family: 'Segoe UI';
    font-size: 10pt;
    font-weight: bold;
    min-height: 38px;
}}
#btnSecondary:hover {{ background: {PRIMARY_LITE}; }}

/* ── Nút nguy hiểm (xanh lá confirm) ── */
#btnSuccess {{
    background: {SUCCESS};
    color: {WHITE};
    border: none;
    border-radius: 8px;
    padding: 10px 24px;
    font-family: 'Segoe UI';
    font-size: 10pt;
    font-weight: bold;
    min-height: 40px;
}}
#btnSuccess:hover {{ background: #1B5E20; }}

/* ── Bảng ── */
QTableWidget {{
    background: {WHITE};
    border: 1px solid {BORDER};
    border-radius: 8px;
    gridline-color: {BORDER};
    font-family: 'Segoe UI';
    font-size: 9pt;
    color: {TEXT_MAIN};
    selection-background-color: {PRIMARY_LITE};
    selection-color: {PRIMARY};
}}
QHeaderView::section {{
    background: {PRIMARY};
    color: {WHITE};
    font-family: 'Segoe UI';
    font-size: 9pt;
    font-weight: bold;
    padding: 8px;
    border: none;
    border-right: 1px solid {ACCENT};
}}
QTableWidget::item {{ padding: 6px 8px; }}
QTableWidget::item:alternate {{ background: {PRIMARY_LITE}; }}

/* ── Label tổng tiền ── */
#labelTong {{
    color: {PRIMARY};
    font-family: 'Segoe UI';
    font-size: 13pt;
    font-weight: bold;
    padding: 8px 16px;
    background: {PRIMARY_LITE};
    border-radius: 8px;
    border: 1.5px solid {ACCENT};
}}

/* ── Search box ── */
#searchBox {{
    background: {WHITE};
    border: 2px solid {ACCENT};
    border-radius: 20px;
    padding: 8px 16px;
    font-family: 'Segoe UI';
    font-size: 10pt;
    color: {TEXT_MAIN};
}}
#searchBox:focus {{ border: 2px solid {PRIMARY}; }}

/* ── Placeholder báo cáo ── */
#placeholder {{
    border: 2px dashed {ACCENT};
    padding: 40px;
    color: {TEXT_MUTED};
    border-radius: 10px;
    font-family: 'Segoe UI';
    font-size: 9pt;
}}
"""


def make_divider():
    line = QFrame()
    line.setFrameShape(QFrame.Shape.HLine)
    line.setStyleSheet(f"color: {BORDER}; margin: 4px 0;")
    return line


class MainWindow(QMainWindow):
    def __init__(self, kho: KhoThuoc):
        super().__init__()
        self.kho = kho
        self.don_hien_tai = []
        self._nav_buttons = []

        self.setWindowTitle("Hệ Thống Quản Lý Nhà Thuốc")
        self.setMinimumSize(1100, 700)
        self.setStyleSheet(STYLE_APP)

        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._build_sidebar())

        self.stack = QStackedWidget()
        self.stack.addWidget(self._tao_man_hinh_nhap_thuoc())   # 0
        self.stack.addWidget(self._tao_man_hinh_lap_don())      # 1
        self.stack.addWidget(self._tao_man_hinh_bao_cao())      # 2
        root.addWidget(self.stack)

        self._set_active(0)

    # ─────────────────────────────────────────────────────────
    # SIDEBAR
    # ─────────────────────────────────────────────────────────
    def _build_sidebar(self):
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(210)
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Logo / tiêu đề
        header = QLabel("🏥  Nhà Thuốc\nPharmacy")
        header.setObjectName("sidebarHeader")
        header.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet(f"""
            color: white;
            background: #0A2E6E;
            padding: 22px 10px;
            border-bottom: 2px solid {ACCENT};
        """)
        layout.addWidget(header)

        items = [
            ("📦   Nhập Thuốc Mới", 0),
            ("📋   Lập Đơn Thuốc",  1),
            ("📊   Báo Cáo / Hết Hạn", 2),
        ]
        for label, idx in items:
            btn = QPushButton(label)
            btn.setObjectName("navBtn")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _, i=idx: self._set_active(i))
            self._nav_buttons.append(btn)
            layout.addWidget(btn)

        layout.addStretch()

        # Footer
        footer = QLabel("v1.0  •  Nhóm KTLTNC")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet(f"color: {ACCENT}; font-size: 8pt; padding: 12px;")
        layout.addWidget(footer)
        return sidebar

    def _set_active(self, index: int):
        self.stack.setCurrentIndex(index)
        for i, btn in enumerate(self._nav_buttons):
            btn.setProperty("active", "true" if i == index else "false")
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    # ─────────────────────────────────────────────────────────
    # HELPER: tạo tiêu đề section
    # ─────────────────────────────────────────────────────────
    def _section_title(self, text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setObjectName("sectionTitle")
        lbl.setFont(FONT_TITLE)
        return lbl

    def _card(self) -> tuple[QWidget, QVBoxLayout]:
        card = QWidget()
        card.setObjectName("card")
        lay = QVBoxLayout(card)
        lay.setContentsMargins(18, 16, 18, 16)
        lay.setSpacing(10)
        return card, lay

    # ─────────────────────────────────────────────────────────
    # MÀN HÌNH 0: NHẬP THUỐC
    # ─────────────────────────────────────────────────────────
    def _tao_man_hinh_nhap_thuoc(self):
        page = QWidget()
        outer = QVBoxLayout(page)
        outer.setContentsMargins(28, 22, 28, 22)
        outer.setSpacing(14)

        outer.addWidget(self._section_title("📦  Nhập Thuốc Mới Vào Kho"))

        card, lay = self._card()
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form.setVerticalSpacing(12)
        form.setHorizontalSpacing(16)

        self.input_ma         = QLineEdit(); self.input_ma.setPlaceholderText("VD: TH001")
        self.input_ten        = QLineEdit(); self.input_ten.setPlaceholderText("VD: Paracetamol 500mg")
        self.input_thanh_phan = QLineEdit(); self.input_thanh_phan.setPlaceholderText("VD: Acetaminophen 500mg")
        self.input_don_vi     = QLineEdit(); self.input_don_vi.setPlaceholderText("viên / vỉ / hộp")
        self.input_gia        = QLineEdit(); self.input_gia.setPlaceholderText("VD: 5000")
        self.input_han        = QLineEdit(); self.input_han.setPlaceholderText("YYYY-MM-DD  (VD: 2027-06-30)")
        self.input_sl         = QSpinBox();  self.input_sl.setRange(0, 99999); self.input_sl.setSuffix("  đơn vị")

        for label, widget in [
            ("Mã thuốc *",       self.input_ma),
            ("Tên thuốc *",      self.input_ten),
            ("Thành phần *",     self.input_thanh_phan),
            ("Đơn vị tính *",    self.input_don_vi),
            ("Giá nhập (VNĐ) *", self.input_gia),
            ("Hạn sử dụng *",    self.input_han),
            ("Số lượng nhập",    self.input_sl),
        ]:
            form.addRow(label, widget)

        lay.addLayout(form)
        lay.addWidget(make_divider())

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        self.btn_them_kho = QPushButton("✅  Thêm Vào Kho")
        self.btn_them_kho.setObjectName("btnPrimary")
        self.btn_them_kho.setMinimumWidth(180)
        self.btn_them_kho.clicked.connect(self._xu_ly_nhap_thuoc)
        btn_row.addWidget(self.btn_them_kho)
        lay.addLayout(btn_row)

        outer.addWidget(card)
        outer.addStretch()
        return page

    def _xu_ly_nhap_thuoc(self):
        ma  = self.input_ma.text().strip()
        ten = self.input_ten.text().strip()
        tp  = self.input_thanh_phan.text().strip()
        dv  = self.input_don_vi.text().strip()
        han = self.input_han.text().strip()
        sl  = self.input_sl.value()

        if not all([ma, ten, tp, dv, han]):
            QMessageBox.warning(self, "Thiếu thông tin", "⚠️ Vui lòng điền đầy đủ tất cả các trường có dấu *")
            return
        try:
            gia = float(self.input_gia.text().strip())
        except ValueError:
            QMessageBox.warning(self, "Lỗi giá", "💡 Giá nhập phải là số\nVD: 5000  hoặc  12500.5")
            return
        try:
            datetime.strptime(han, "%Y-%m-%d")
        except ValueError:
            QMessageBox.warning(self, "Lỗi ngày", "💡 Định dạng ngày phải là YYYY-MM-DD\nVD: 2027-06-30")
            return

        thuoc = ThuocKhongKeDon(ma, ten, tp, dv, gia, han)
        self.kho.them_thuoc_moi(thuoc)
        self.kho += (ten, sl)
        luu_du_lieu_json(self.kho)

        QMessageBox.information(self, "Thêm kho thành công",
            f"✅  Đã thêm  '{ten}'  vào kho\n"
            f"Số lượng: {sl} {dv}  |  Giá nhập: {gia:,.0f} VNĐ")

        for w in [self.input_ma, self.input_ten, self.input_thanh_phan,
                  self.input_don_vi, self.input_gia, self.input_han]:
            w.clear()
        self.input_sl.setValue(0)

    # ─────────────────────────────────────────────────────────
    # MÀN HÌNH 1: LẬP ĐƠN
    # ─────────────────────────────────────────────────────────
    def _tao_man_hinh_lap_don(self):
        page = QWidget()
        outer = QVBoxLayout(page)
        outer.setContentsMargins(28, 22, 28, 22)
        outer.setSpacing(12)

        outer.addWidget(self._section_title("📋  Lập Đơn Thuốc"))

        # Search box
        self.input_search = QLineEdit()
        self.input_search.setObjectName("searchBox")
        self.input_search.setPlaceholderText("🔍  Gõ tên hoặc mã thuốc để tìm kiếm ngay...")
        self.input_search.setFixedHeight(42)
        self.input_search.textChanged.connect(self._xu_ly_tim_kiem)
        outer.addWidget(self.input_search)

        # Bảng tìm kiếm
        lbl1 = QLabel("Kết quả tìm kiếm")
        lbl1.setFont(FONT_SECTION)
        lbl1.setStyleSheet(f"color: {TEXT_MUTED}; margin-top: 4px;")
        outer.addWidget(lbl1)

        self.bang_tim_kiem = QTableWidget(0, 5)
        self.bang_tim_kiem.setHorizontalHeaderLabels(
            ["Mã thuốc", "Tên thuốc", "Đơn vị", "Giá bán", "Tồn kho"])
        self.bang_tim_kiem.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.bang_tim_kiem.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.bang_tim_kiem.setAlternatingRowColors(True)
        self.bang_tim_kiem.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.bang_tim_kiem.setFixedHeight(180)
        outer.addWidget(self.bang_tim_kiem)

        # Row: số lượng + nút thêm
        row_sl = QHBoxLayout()
        row_sl.addWidget(QLabel("  Số lượng:"))
        self.input_sl_don = QSpinBox()
        self.input_sl_don.setRange(1, 9999)
        self.input_sl_don.setFixedWidth(120)
        row_sl.addWidget(self.input_sl_don)
        row_sl.addStretch()
        self.btn_them_don = QPushButton("➕  Thêm Vào Đơn")
        self.btn_them_don.setObjectName("btnSecondary")
        self.btn_them_don.setMinimumWidth(160)
        self.btn_them_don.clicked.connect(self._xu_ly_them_vao_don)
        row_sl.addWidget(self.btn_them_don)
        outer.addLayout(row_sl)

        outer.addWidget(make_divider())

        # Bảng đơn
        lbl2 = QLabel("Đơn thuốc hiện tại")
        lbl2.setFont(FONT_SECTION)
        lbl2.setStyleSheet(f"color: {TEXT_MUTED};")
        outer.addWidget(lbl2)

        self.bang_don_thuoc = QTableWidget(0, 4)
        self.bang_don_thuoc.setHorizontalHeaderLabels(
            ["Tên thuốc", "Số lượng", "Đơn giá", "Thành tiền"])
        self.bang_don_thuoc.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.bang_don_thuoc.setAlternatingRowColors(True)
        self.bang_don_thuoc.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        outer.addWidget(self.bang_don_thuoc)

        # Tổng tiền + nút xác nhận
        row_tong = QHBoxLayout()
        self.label_tong = QLabel("Tổng tiền:  0 VNĐ")
        self.label_tong.setObjectName("labelTong")
        row_tong.addWidget(self.label_tong)
        row_tong.addStretch()
        self.btn_xac_nhan = QPushButton("🧾  Xác Nhận Lập Đơn")
        self.btn_xac_nhan.setObjectName("btnSuccess")
        self.btn_xac_nhan.setMinimumWidth(190)
        self.btn_xac_nhan.clicked.connect(self._xu_ly_xac_nhan_don)
        row_tong.addWidget(self.btn_xac_nhan)
        outer.addLayout(row_tong)

        return page

    def _lay_tat_ca_thuoc(self):
        ket_qua = []
        for node in self.kho.kho_du_lieu.bucket_array:
            cur = node
            while cur:
                ket_qua.append({"doi_tuong": cur.value["doi_tuong"], "so_luong": cur.value["so_luong"]})
                cur = cur.next
        return ket_qua

    def _xu_ly_tim_kiem(self, tu_khoa: str):
        self.bang_tim_kiem.setRowCount(0)
        tu_khoa = tu_khoa.strip()
        if not tu_khoa:
            return

        ds = []
        chinh_xac = self.kho.kho_du_lieu.search(tu_khoa)
        if chinh_xac:
            ds.append({"doi_tuong": chinh_xac["doi_tuong"], "so_luong": chinh_xac["so_luong"]})
        else:
            for item in self._lay_tat_ca_thuoc():
                t = item["doi_tuong"]
                if tu_khoa.lower() in t.ten_thuoc.lower() or tu_khoa.lower() in t.ma_thuoc.lower():
                    ds.append(item)

        for item in ds:
            t  = item["doi_tuong"]
            sl = item["so_luong"]
            gia = t.tinh_gia_ban() or t.gia_nhap
            r = self.bang_tim_kiem.rowCount()
            self.bang_tim_kiem.insertRow(r)
            for c, val in enumerate([t.ma_thuoc, t.ten_thuoc, t.don_vi_tinh,
                                      f"{gia:,.0f} ₫", str(sl)]):
                cell = QTableWidgetItem(val)
                cell.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.bang_tim_kiem.setItem(r, c, cell)

            # Màu cảnh báo
            if not t.kiem_tra_han_dung():
                mau = QColor("#FFCDD2")  # Đỏ nhạt
            elif sl == 0:
                mau = QColor("#FFE0B2")  # Cam nhạt
            elif sl < 10:
                mau = QColor("#FFF9C4")  # Vàng nhạt
            else:
                mau = QColor(WHITE)

            for c in range(5):
                self.bang_tim_kiem.item(r, c).setBackground(mau)

    def _xu_ly_them_vao_don(self):
        row = self.bang_tim_kiem.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Chưa chọn thuốc",
                "👆 Hãy click chọn một dòng thuốc trong bảng kết quả tìm kiếm trước.")
            return

        ten = self.bang_tim_kiem.item(row, 1).text()
        sl_yeu_cau = self.input_sl_don.value()
        thong_tin = self.kho.kho_du_lieu.search(ten)
        if not thong_tin:
            QMessageBox.critical(self, "Lỗi", f"Không tìm thấy '{ten}' trong kho!"); return

        thuoc = thong_tin["doi_tuong"]
        sl_kho = thong_tin["so_luong"]

        try:
            if not thuoc.kiem_tra_han_dung():
                raise ExpiredDateError(f"Thuốc  '{ten}'  đã hết hạn sử dụng!\nKhông được phép bán.")
            if sl_yeu_cau > sl_kho:
                raise OutOfStockError(
                    f"Tồn kho chỉ còn  {sl_kho} {thuoc.don_vi_tinh}  '{ten}'\n"
                    f"Không đủ  {sl_yeu_cau} {thuoc.don_vi_tinh}  như yêu cầu.")
        except ExpiredDateError as e:
            QMessageBox.critical(self, "⛔  Thuốc Hết Hạn", str(e)); return
        except OutOfStockError as e:
            QMessageBox.critical(self, "⛔  Hết Hàng Trong Kho", str(e)); return

        self.don_hien_tai.append((thuoc, sl_yeu_cau))
        gia = thuoc.tinh_gia_ban() or thuoc.gia_nhap
        thanh_tien = gia * sl_yeu_cau
        r = self.bang_don_thuoc.rowCount()
        self.bang_don_thuoc.insertRow(r)
        for c, val in enumerate([thuoc.ten_thuoc, str(sl_yeu_cau),
                                  f"{gia:,.0f} ₫", f"{thanh_tien:,.0f} ₫"]):
            cell = QTableWidgetItem(val)
            cell.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.bang_don_thuoc.setItem(r, c, cell)

        tong = sum(t.tinh_gia_ban() * sl for t, sl in self.don_hien_tai)
        self.label_tong.setText(f"Tổng tiền:  {tong:,.0f} VNĐ")

    def _xu_ly_xac_nhan_don(self):
        if not self.don_hien_tai:
            QMessageBox.warning(self, "Đơn trống", "Chưa có thuốc nào trong đơn!"); return

        for thuoc, sl in self.don_hien_tai:
            tt = self.kho.kho_du_lieu.search(thuoc.ten_thuoc)
            if tt: tt["so_luong"] -= sl
        luu_du_lieu_json(self.kho)

        tong = sum(t.tinh_gia_ban() * sl for t, sl in self.don_hien_tai)
        QMessageBox.information(self, "✅  Lập Đơn Thành Công",
            f"Đơn thuốc đã được xuất!\nTổng tiền: {tong:,.0f} VNĐ\n\nDữ liệu kho đã được lưu.")

        self.don_hien_tai.clear()
        self.bang_don_thuoc.setRowCount(0)
        self.label_tong.setText("Tổng tiền:  0 VNĐ")

    # ─────────────────────────────────────────────────────────
    # MÀN HÌNH 2: BÁO CÁO
    # ─────────────────────────────────────────────────────────
    def _tao_man_hinh_bao_cao(self):
        page = QWidget()
        outer = QVBoxLayout(page)
        outer.setContentsMargins(28, 22, 28, 22)
        outer.setSpacing(12)

        outer.addWidget(self._section_title("📊  Báo Cáo Kho Thuốc"))

        row_btn = QHBoxLayout()
        self.btn_loc = QPushButton("⚠️   Lọc & Sắp Xếp Thuốc Sắp Hết Hạn  (Heap Sort)")
        self.btn_loc.setObjectName("btnPrimary")
        self.btn_loc.setMinimumHeight(42)
        self.btn_loc.clicked.connect(self._xu_ly_loc_het_han)
        row_btn.addWidget(self.btn_loc)
        row_btn.addStretch()
        outer.addLayout(row_btn)

        self.bang_het_han = QTableWidget(0, 4)
        self.bang_het_han.setHorizontalHeaderLabels(
            ["Tên thuốc", "Hạn dùng", "Tồn kho", "Trạng thái"])
        self.bang_het_han.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.bang_het_han.setAlternatingRowColors(True)
        self.bang_het_han.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        outer.addWidget(self.bang_het_han)

        placeholder = QLabel("[ Nhấn nút bên trên để lọc và sắp xếp toàn bộ kho theo ngày hết hạn ]")
        placeholder.setObjectName("placeholder")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        outer.addWidget(placeholder)
        return page

    def _xu_ly_loc_het_han(self):
        tat_ca = self._lay_tat_ca_thuoc()
        if not tat_ca:
            QMessageBox.information(self, "Kho trống", "Kho thuốc chưa có dữ liệu!"); return

        doi_tuong_list = [i["doi_tuong"] for i in tat_ca]
        sl_map = {i["doi_tuong"].ten_thuoc: i["so_luong"] for i in tat_ca}
        da_sort = self.kho.kho_du_lieu.heap_sort(doi_tuong_list)

        self.bang_het_han.setRowCount(0)
        hom_nay = datetime.now().date()

        for thuoc in da_sort:
            try:
                ngay = datetime.strptime(thuoc.han_su_dung, "%Y-%m-%d").date()
            except ValueError:
                continue
            sl = sl_map.get(thuoc.ten_thuoc, 0)
            con_lai = (ngay - hom_nay).days

            if con_lai < 0:
                trang_thai, mau = "❌  Đã hết hạn",        QColor("#FFCDD2")
            elif con_lai <= 30:
                trang_thai, mau = f"⚠️  Còn {con_lai} ngày",  QColor("#FFE0B2")
            elif con_lai <= 90:
                trang_thai, mau = f"🟡  Còn {con_lai} ngày",  QColor("#FFF9C4")
            else:
                trang_thai, mau = f"✅  Còn {con_lai} ngày",  QColor("#C8E6C9")

            r = self.bang_het_han.rowCount()
            self.bang_het_han.insertRow(r)
            for c, val in enumerate([thuoc.ten_thuoc, thuoc.han_su_dung, str(sl), trang_thai]):
                cell = QTableWidgetItem(val)
                cell.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.bang_het_han.setItem(r, c, cell)
                self.bang_het_han.item(r, c).setBackground(mau)


# ── CHẠY STANDALONE ──────────────────────────────────────────
if __name__ == "__main__":
    from models import KhoThuoc, doc_du_lieu_json
    kho = KhoThuoc()
    doc_du_lieu_json(kho)
    app = QApplication(sys.argv)
    w = MainWindow(kho)
    w.show()
    sys.exit(app.exec())