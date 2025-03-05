import os
import sys

import requests
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton

SCREEN_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.spn = 0.002
        self.getImage()
        self.initUI()

    def getImage(self):
        server_address = 'https://static-maps.yandex.ru/v1?'
        api_key = '7099749a-10db-45e9-82e2-dcdebe051633'
        ll_spn = f'll=37.595348,55.827206&spn={self.spn},{self.spn}'

        map_request = f"{server_address}{ll_spn}&apikey={api_key}"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        self.up = QPushButton('PgUp', self)
        self.up.move(10, 100)
        self.up.clicked.connect(self.up_f)

        self.down = QPushButton('PgDown', self)
        self.down.move(10, 200)
        self.down.clicked.connect(self.down_f)

        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(100, 0)
        self.image.resize(500, 400)
        self.image.setPixmap(self.pixmap)

    def update_map(self):
        self.getImage()
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        os.remove(self.map_file)

    def up_f(self):
        if self.spn < 0.07:
            self.spn *= 1.5
            self.update_map()

    def down_f(self):
        if self.spn > 0.001:
            self.spn /= 1.5
            self.update_map()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
