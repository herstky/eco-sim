from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt

class Window(QMainWindow):
    def __init__(self, left=50, top=50, width=1200, height=800):
        super().__init__()
        self.setWindowTitle('EcoSim')
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.leftMargin = 50
        self.topMargin = 50
        self.tileSize = 32
        self.qTimer = QTimer()
        self.setGeometry(self.left, self.top, self.width, self.height)
        
    def startTimer(self, function):
        self.qTimer.setInterval(self.simulation.waitBetweenRounds * 1000)
        self.qTimer.timeout.connect(function)
        self.qTimer.start()

    def createBackground(self, rows, cols):
        pixmap = QPixmap('assets/grass.png')
        for row in range(rows):
            top = row * self.tileSize + self.topMargin
            for col in range(cols):
                label = QLabel(self)
                label.setPixmap(pixmap)
                left = col * self.tileSize + self.leftMargin
                label.setGeometry(left, top, self.tileSize, self.tileSize)

    def addEntity(self, entity):
        if not entity.texture:
            return
        pixmap = QPixmap(entity.texture)
        entity.label = QLabel(self)
        entity.label.setPixmap(pixmap)
        left = entity.col * self.tileSize + self.leftMargin
        top = entity.row * self.tileSize + self.topMargin
        entity.label.setGeometry(left, top, self.tileSize, self.tileSize)
        entity.label.show()

    def moveEntity(self, entity):
        if not entity.label:
            return
        left = entity.col * self.tileSize + self.leftMargin
        top = entity.row * self.tileSize + self.topMargin
        entity.label.move(left, top)

