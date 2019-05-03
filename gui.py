from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QTimer, QElapsedTimer, Qt
from time import sleep
import sys

from simulation import *

class Window(QMainWindow):
    def __init__(self, simulation, left=50, top=50, width=1200, height=800):
        super().__init__()
        self.simulation = simulation
        self.setWindowTitle('EcoSim')
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.leftMargin = 50
        self.topMargin = 50
        self.tileSize = 32

        self.setGeometry(self.left, self.top, self.width, self.height)
        self.createBackground()
        self.placeEntities()
        
        self.qTimer = QTimer()
        self.updatesPerSecond = 60
        self.qTimer.setInterval(1 / self.updatesPerSecond * 1000)
        self.v_x = .5
        self.a_x = .05
        self.v_y = .5
        self.a_y = -.05
        self.row = 50
        self.col = 50

        # self.label = QLabel(self)
        # pixmap = QPixmap('assets/creature.png')
        # self.label.setPixmap(pixmap)
        # self.label.setGeometry(self.row, self.col, pixmap.width(), pixmap.height()) 
        # self.qTimer.timeout.connect(self.move)
        # self.qTimer.start()
        # self.qSimTime = QElapsedTimer()
        # self.qSimTime.start()

    def move(self):
        time = self.qSimTime.elapsed() / 1000
        self.row += self.v_x * time + 1 / 2 * self.a_x * pow(time, 2)
        self.col += self.v_y * time + 1 / 2 * self.a_y * pow(time, 2)
        self.label.move(self.row, self.col)

    def createBackground(self):
        pixmap = QPixmap('assets/grass.png')
        for row in range(self.simulation.board.rows):
            top = row * self.tileSize + self.topMargin
            for col in range(self.simulation.board.cols):
                label = QLabel(self)
                label.setPixmap(pixmap)
                left = col * self.tileSize + self.leftMargin
                label.setGeometry(left, top, self.tileSize, self.tileSize)

    def placeEntities(self):
        for entity in self.simulation.board.entities:
            pixmap = QPixmap('assets/creature.png')
            label = QLabel(self)
            label.setPixmap(pixmap)
            left = entity.col * self.tileSize + self.leftMargin
            top = entity.row * self.tileSize + self.topMargin
            label.setGeometry(left, top, self.tileSize, self.tileSize)


if __name__ == '__main__':
    board = Board()
    sim = Simulation(board)
    
    app = QApplication(sys.argv)
    ex = Window(sim)
    ex.show()
    sys.exit(app.exec_())
