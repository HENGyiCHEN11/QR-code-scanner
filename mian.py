import sys
import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class QRScanner(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("二维码扫描工具 v1.0")
        self.setFixedSize(900, 750)
        self.setStyleSheet("background-color: #f8f9fa;")

        self.last_data = ""
        self.cap = cv2.VideoCapture(0)
        self.detector = cv2.QRCodeDetector()

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(30, 30, 30, 30)

        # 标题
        title = QLabel("✅ 二维码扫描器")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:28px; font-weight:bold; color:#2d3436;")
        layout.addWidget(title)

        # 画面区域
        self.label = QLabel()
        self.label.setFixedSize(640, 480)
        self.label.setStyleSheet("border: 3px solid #0984e3; border-radius:10px; background-color:white;")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label, alignment=Qt.AlignCenter)

        # 结果框
        self.result = QLineEdit()
        self.result.setPlaceholderText("扫描结果将显示在这里")
        self.result.setStyleSheet("padding:12px; font-size:15px; border:1px solid #ddd; border-radius:8px;")
        layout.addWidget(self.result)

        # 按钮
        btn_layout = QHBoxLayout()

        copy = QPushButton("📋 复制结果")
        copy.setStyleSheet("padding:12px; font-size:15px; background-color:#0984e3; color:white; border-radius:8px;")
        copy.clicked.connect(self.copy)

        clear = QPushButton("🗑️ 清空")
        clear.setStyleSheet("padding:12px; font-size:15px; background-color:#636e72; color:white; border-radius:8px;")
        clear.clicked.connect(self.clear)

        btn_layout.addWidget(copy)
        btn_layout.addWidget(clear)
        layout.addLayout(btn_layout)

        # 定时器
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        ret, f = self.cap.read()
        if not ret: return

        data, bbox, _ = self.detector.detectAndDecode(f)

        if bbox is not None:
            cv2.polylines(f, [bbox.astype(int)], True, (0,255,0), 3)

        if data and data != self.last_data:
            self.last_data = data
            self.result.setText(data)

        f = cv2.cvtColor(f, cv2.COLOR_BGR2RGB)
        h, w, ch = f.shape
        bytes = ch * w
        q_img = QImage(f.data, w, h, bytes, QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(q_img).scaled(640, 480, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def copy(self):
        QApplication.clipboard().setText(self.result.text())
        self.result.setText(self.result.text() + "  ✅已复制")

    def clear(self):
