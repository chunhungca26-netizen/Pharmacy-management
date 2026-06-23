# main.py - File khởi động toàn bộ dự án

import sys
from PyQt6.QtWidgets import QApplication
from models import KhoThuoc, doc_du_lieu_json
from gui import MainWindow


def main():
    # Khởi tạo kho và nạp dữ liệu cũ từ database.json
    kho = KhoThuoc()
    doc_du_lieu_json(kho)

    app = QApplication(sys.argv)
    window = MainWindow(kho)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()