import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QGridLayout, QPushButton, QApplication, QHBoxLayout, QLabel)
from PyQt5.QtGui import QIcon, QPixmap


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        grid = QGridLayout()
        self.setLayout(grid)

        heroes = [
            'Aatrox', 'Ahri', 'Akali', 'Akshan', 'Alistar', 'Amumu',
            'Anivia', 'Annie', 'Aphelios', 'Ashe', 'AurelionSol', 'Azir',
            'Bard', 'Blitzcrank', 'Brand', 'Braum', 'Caitlyn', 'Camille',
            'Cassiopeia', 'Chogath', 'Corki', 'Darius', 'Diana', 'Draven'
        ]

        positions = [(i, j) for i in range(4) for j in range(6)]
        print(positions)

        # btn = QPushButton('', self)
        # btn.move(200, 200)
        # btn.resize(100, 100)
        # pic = 'Ashe.png'
        # btn.setStyleSheet("QPushButton{border-image: url(heroes/" + pic + ")}")

        # pix = QPixmap("heroes/Ashe.png")
        # lab = QLabel(self)
        # lab.setGeometry(0,0,120,120)
        # lab.setPixmap(pix)

        for position, hero in zip(positions, heroes):
            pix = QPixmap("heroes/" + hero + ".png")
            lab = QLabel(self)
            lab.setPixmap(pix)
            grid.addWidget(lab, *position)

            # button = QPushButton(hero, self)
            # # button.resize(100,100)
            # button.setStyleSheet("QPushButton{border-image: url(heroes/" + hero + ".png)}")
            # grid.addWidget(button, *position)
            # grid.setRowMinimumHeight(0,160)

        grid.setSpacing(0)
        grid.setVerticalSpacing(0)
        # grid.setHorizontalSpacing(100)

        self.setWindowTitle("卡尔英雄池")
        self.resize(1200, 800)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_())
