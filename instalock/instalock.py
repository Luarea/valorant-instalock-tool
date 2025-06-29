import os
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
os.environ["QT_SCALE_FACTOR"] = "1"

import sys
import pyautogui
import keyboard
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QGridLayout, QLineEdit, QMessageBox, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QIcon

pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False

karakter_koordinatlari = {
    "Brimstone": (282, 344),
    "Phoenix": (81, 740),
    "Sage": (388, 744),
    "Sova": (189, 838),
    "Viper": (383, 834),
    "Cypher": (172, 422),
    "Reyna": (285, 741),
    "Killjoy": (185, 644),
    "Breach": (190, 354),
    "Omen": (382, 643),
    "Jett": (381, 543),
    "Raze": (186, 740),
    "Skye": (87, 834),
    "Yoru": (295, 894),
    "KAY/O": (87, 643),
    "Chamber": (380, 352),
    "Neon": (282, 638),
    "Fade": (387, 433),
    "Harbor": (196, 544),
    "Gekko": (74, 543),
    "Deadlock": (290, 450),
    "Astra": (75, 318),
    "Iso": (282, 543),
    "Clove": (73, 448),
    "Vyse": (93, 894),
    "Tejo": (282, 842),
    "Waylay": (175, 896),
}

lock_koordinat = (960, 720)
secilen_ajan = None
SABIT_KEY = "instalock"  # Burada belirlediğin key

class LockThread(QThread):
    update_status = pyqtSignal(str)

    def run(self):
        global secilen_ajan
        while True:
            if keyboard.is_pressed("F8") and secilen_ajan:
                x, y = karakter_koordinatlari[secilen_ajan]
                pyautogui.click(x=x, y=y)
                pyautogui.click(x=lock_koordinat[0], y=lock_koordinat[1])
            elif keyboard.is_pressed("esc"):
                self.update_status.emit("ÇIKIYORUZ...")
                break

class GlowButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("""
            QPushButton {
                background-color: #6a0dad;
                color: #e0c3fc;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #9b30ff;
            }
        """)
        self.setFont(QFont("Consolas", 11))
        glow = QGraphicsDropShadowEffect(self)
        glow.setBlurRadius(25)
        glow.setColor(QColor("#9b30ff"))
        glow.setOffset(0)
        self.setGraphicsEffect(glow)
        self.setMinimumHeight(40)
        self.setMaximumWidth(140)

class InstalockUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VALORANT INSTALOCK – by Luarea")
        self.setWindowIcon(QIcon("bbl.ico"))
        self.setFixedSize(800, 500)
        self.setStyleSheet("background-color: #1a001a; color: #e0c3fc;")

        main_layout = QVBoxLayout()

        self.title = QLabel("VALORANT INSTALOCK")
        self.title.setFont(QFont("Consolas", 18, QFont.Weight.Bold))
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("color: #d8b6ff;")
        main_layout.addWidget(self.title)

        self.status = QLabel("Ajan seçilmedi")
        self.status.setFont(QFont("Consolas", 12))
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status.setStyleSheet("color: #c1a3f5;")
        main_layout.addWidget(self.status)

        grid = QGridLayout()
        grid.setSpacing(10)

        ajanlar = list(karakter_koordinatlari.keys())
        cols = 6
        for i, ajan in enumerate(ajanlar):
            btn = GlowButton(ajan)
            btn.clicked.connect(lambda _, a=ajan: self.ajan_sec(a))
            row = i // cols
            col = i % cols
            grid.addWidget(btn, row, col)

        main_layout.addLayout(grid)

        self.kontrol = QLabel("▶ F8: Spam Lock (basılı tut) | ESC: Çık")
        self.kontrol.setFont(QFont("Consolas", 10))
        self.kontrol.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.kontrol.setStyleSheet("color: #b296f7;")
        main_layout.addWidget(self.kontrol)

        self.imza = QLabel("Made by Luarea")
        self.imza.setFont(QFont("Consolas", 9))
        self.imza.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.imza.setStyleSheet("color: #a37bdf;")
        main_layout.addWidget(self.imza)

        self.setLayout(main_layout)

        self.thread = LockThread()
        self.thread.update_status.connect(self.update_status)
        self.thread.start()

    def ajan_sec(self, ajan):
        global secilen_ajan
        secilen_ajan = ajan
        self.status.setText(f"Seçilen: {ajan}")

    def update_status(self, mesaj):
        self.status.setText(mesaj)

class LoginUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Giriş - Valorant Instalock")
        self.setFixedSize(300, 150)
        self.setStyleSheet("background-color: #1a001a; color: #e0c3fc;")

        layout = QVBoxLayout()

        self.label = QLabel("Lütfen key girin:")
        self.label.setFont(QFont("Consolas", 12))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        self.key_input = QLineEdit()
        self.key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.key_input.setFont(QFont("Consolas", 12))
        self.key_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.key_input.returnPressed.connect(self.check_key)
        layout.addWidget(self.key_input)

        self.login_button = GlowButton("Giriş Yap")
        self.login_button.clicked.connect(self.check_key)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def check_key(self):
        girilen_key = self.key_input.text()
        if girilen_key == SABIT_KEY:
            self.accept_login()
        else:
            QMessageBox.warning(self, "Hata", "Geçersiz key! Tekrar deneyin.")
            self.key_input.clear()

    def accept_login(self):
        self.close()
        self.instalock_ui = InstalockUI()
        self.instalock_ui.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = LoginUI()
    login.show()
    sys.exit(app.exec())
