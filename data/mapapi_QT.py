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
        self.k1 = 37.595348
        self.k2 = 55.82720
        self.ogr1 = self.k1 - 0.2
        self.ogr2 = self.k1 + 0.2
        self.ogr3 = self.k2 + 0.2
        self.ogr4 = self.k2 - 0.2
        self.theme = "light"
        self.getImage()
        self.initUI()

    def getImage(self):
        server_address = 'https://static-maps.yandex.ru/v1?'
        api_key = '7099749a-10db-45e9-82e2-dcdebe051633'
        ll_spn = f'll={self.k1},{self.k2}&spn={self.spn},{self.spn}'

        params = {
            "theme": self.theme
        }

        map_request = f"{server_address}{ll_spn}&apikey={api_key}"
        response = requests.get(map_request, params=params)

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
        self.up.move(10, 10)
        self.up.clicked.connect(self.up_f)

        self.down = QPushButton('PgDown', self)
        self.down.move(10, 50)
        self.down.clicked.connect(self.down_f)

        self.up1 = QPushButton('вверх', self)
        self.up1.move(10, 90)
        self.up1.clicked.connect(self.up_f2)

        self.down1 = QPushButton('вниз', self)
        self.down1.move(10, 130)
        self.down1.clicked.connect(self.down_f2)

        self.left = QPushButton('вправо', self)
        self.left.move(10, 170)
        self.left.clicked.connect(self.right_f)

        self.right = QPushButton('влево', self)
        self.right.move(10, 210)
        self.right.clicked.connect(self.left_f)

        self.dark = QPushButton(f'тёмная/\nсветлая', self)
        self.dark.move(10, 250)
        self.dark.clicked.connect(self.dark_f)

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

    def up_f2(self):
        if self.k2 < self.ogr3:
            self.k2 += self.spn / 2
            self.update_map()

    def down_f2(self):
        if self.k2 > self.ogr4:
            self.k2 -= self.spn / 2
            self.update_map()

    def left_f(self):
        if self.k1 > self.ogr1:
            self.k1 -= self.spn / 2
            self.update_map()

    def right_f(self):
        if self.k1 < self.ogr2:
            self.k1 += self.spn / 2
            self.update_map()

    def dark_f(self):
        if self.theme == "light":
            self.theme = "dark"
        else:
            self.theme = "light"
        self.update_map()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
