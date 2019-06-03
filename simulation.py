from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Process
from random import randint
import sys

from utilities import functionTimer
from entities import *
from board import Board, Cell
from gui import *


class Simulation:
    def __init__(self, window, waitBetweenRounds=.5):
        self.board = Board(window)
        self.simCount = 1
        self.iteration = 1
        self.window = window
        self.waitBetweenRounds = waitBetweenRounds

        self.window.createBackground(self.board.rows, self.board.cols)
        self.addEntities()        
        self.window.startTimer(self, self.tick)

    def addEntities(self):
        for entity in self.board.entities:
            self.window.addEntity(entity)

    def run(self, entity):
        if entity.processed:
            return
        entity.simulate(self.board)
        self.window.moveEntity(entity)
        entity.getStatus(self.board)

    @functionTimer
    def tick(self):
        self.board.queueEntities()
        particles = []
        organisms = []
        for entity in self.board.entities:
            if isinstance(entity, Particle):
                particles.append(entity)
            elif isinstance(entity, Organism):
                organisms.append(entity)
        print('particles:', len(particles))
        print('organisms:', len(organisms))
        for organism in organisms:
            self.run(organism)
        for particle in particles:
            self.run(particle)

        if self.board.herbivores <= 0:
            for entity in self.board.entities:
                if entity.label:
                    entity.label.deleteLater()
            self.board = Board(self.window, self.board.creatureTemplate)
            self.simCount += 1

        self.board.sortEntities()
        self.board.raiseLabels()
        self.iteration += 1




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    simulation = Simulation(window, .25)    
    window.show()
    sys.exit(app.exec_())
