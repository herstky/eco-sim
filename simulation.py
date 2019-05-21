from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Process
from random import randint
import sys

from utilities import functionTimer
from entities import *
from board import Board, Cell
from gui import *


class Simulation:
    def __init__(self, window, iterations=10, waitBetweenEntities=0.25, waitBetweenRounds=0):
        self.board = Board(window)
        self.iteration = 0
        self.window = window
        self.iterations = iterations
        self.waitBetweenEntities = waitBetweenEntities
        self.waitBetweenRounds = waitBetweenRounds

        self.window.simulation = self
        self.window.createBackground(self.board.rows, self.board.cols)
        self.addEntities()
        self.window.startTimer(self.tick)

    def addEntities(self):
        for entity in self.board.entities:
            self.window.addEntity(entity)

    def run(self, entity):
        if entity.processed:
            return
        entity.simulate(self.board)
        self.window.moveEntity(entity)
        entity.getStatus(self.board)

    def test(self, cell):
        cell.simulateParticles()

    def simulateParticles(self, entities):
        for entity in entities:
            entiy.emanateScent()
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                for particle in self.board[row][col].particles:
                    particle.simulate()
        self.board.consolidateParticles()

    def simParticle(self, entity):
        entity.emanateScent()

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

        self.board.consolidateParticles()
        self.board.sortEntities()
        self.board.raiseLabels()
        self.iteration += 1

    @functionTimer
    def tick2(self):
        self.board.queueEntities()        
        pool = ThreadPool(8)
        results = pool.map(self.run, self.board.entities)
        pool.close()
        pool.join()

        self.board.consolidateParticles()
        self.board.sortEntities()
        self.board.raiseLabels()
        print('entities:', len(self.board.entities))
        self.iteration += 1
            
    @functionTimer
    def tick3(self):
        self.board.queueEntities()
        for entity in self.board.entities:
            self.run(entity)
        # for row in range(self.board.rows):
        #     for col in range(self.board.cols):
        #         for particle in self.board[row][col].particles:
        #             particle.simulate()

        for row in self.board:
            pool = ThreadPool(16)
            result = pool.map(self.test, row)
            pool.close()
            pool.join()
        
        self.board.consolidateParticles()
        self.board.sortEntities()
        self.board.raiseLabels()
        print('entities:', len(self.board.entities))
        self.iteration += 1


    @functionTimer
    def tick4(self):
        self.board.queueEntities()
        entitiesSnapshot = self.board.entities[:]
        processes = []
        for entity in entitiesSnapshot:
            process = Process(target=self.simParticle, args = (entity,))
            processes.append(process)
            process.start()
        for process in processes:
            process.join()

        for entity in self.board.entities:
            self.run(entity)
        self.board.sortEntities()
        self.board.raiseLabels()


        print('entities:', len(self.board.entities))
        self.iteration += 1


    @functionTimer
    def tick5(self):
        self.board.queueEntities()
        for entity in self.board.entities:
            self.run(entity)
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                for particle in self.board[row][col].particles:
                    particle.simulate()
        self.board.consolidateParticles()
        self.board.sortEntities()
        self.board.raiseLabels()
        print('entities:', len(self.board.entities))
        self.iteration += 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    simulation = Simulation(window, 30, .5, .5)    
    window.show()
    sys.exit(app.exec_())
