import entities 
import random as rand
from time import sleep

from gui import *

class Board:
    def __init__(self, window, rows=20, cols=30):
        self.window = window
        self.rows = rows
        self.cols = cols
        self.entities = []
        self.board = [[[entities.EmptySpace(self)] for col in range(self.cols)] for row in range(self.rows)]
        self.populateBoard()

    def __getitem__(self, row):
        return self.board[row]

    # adds entity to entities list and inserts it at the front of the list at the given coords
    def addEntity(self, entity, coords):
        entity.row, entity.col = coords
        if entity not in self.entities:
            self.entities.append(entity)
        if not entity.label:
            self.window.addEntity(entity)
        self.board[entity.row][entity.col].insert(0, entity)
 
    # removes entity from board, but leaves it in the entities list
    def removeEntityFromBoard(self, entity):
        row = entity.row
        col = entity.col
        entity.row = None
        entity.col = None
        self.board[row][col].remove(entity)
        if len(self.board[row][col]) == 0:
            self.board[row][col].insert(entities.EmptySpace(self))

    # completely destroys entity
    def deleteEntity(self, entity):
        self.entities.remove(entity)
        self.removeEntityFromBoard(entity)

    # returns entity at the front of the list at the given coords
    def getEntity(self, coords):
        row, col = coords
        return self.board[row][col][0]

    # insert entity at the front of the list at the given coords
    # also removes entity from previous location
    def moveEntity(self, entity, coords):
        row, col = coords
        if entity.row is not None and entity.col is not None:
            self.removeEntityFromBoard(entity)
        entity.row = row
        entity.col = col
        self.addEntity(entity, coords)

    def validPosition(self, coords):
        row, col = coords
        if row < 0 or row > self.rows - 1 or col < 0 or col > self.cols - 1:
            return False
        else:
            return True

    def sortEntities(self):
        self.entities.sort(key=lambda x: x.speed, reverse=True) # faster entities go first

    def populateBoard(self):
        herbivoreChance = 5
        carnivoreChance = 5
        plantChance = 10
        for row in range(self.rows):
            for col in range(self.cols):
                roll = rand.randint(1, 100)
                if roll <= herbivoreChance:
                    self.addEntity(entities.Herbivore(self), (row, col))
                elif roll <= herbivoreChance + carnivoreChance:
                    self.addEntity(entities.Carnivore(self), (row, col))
                # elif roll <= herbivoreChance + carnivoreChance + plantChance:
                #     self.addEntity(entities.Plant(self, rand.randint(2, 4)), (row, col))

    def tick(self):
        self.simulateEntities()
        self.updateEntities()

    # prints the first entity in every cell
    # it would appear the MS interpreter can't print all this. TODO delete
    def printBoard(self):
        for col in range(self.cols + 2):
            print('-', end='')
        for row in range(self.rows):
            print('')
            for col in range(self.cols):
                if col == 0:
                    print('|{}'.format(self.getEntity((row, col)).character), end='')
                elif col == self.cols - 1:
                    print('{}|'.format(self.getEntity((row, col)).character), end='')
                else:
                    print(self.getEntity((row, col)).character, end='')
        print('')
        for col in range(self.cols + 2):
            print('-', end='')    
        print('')

class Simulation:
    def __init__(self, window, iterations=10, waitBetweenEntities=0.25, waitBetweenRounds=0):
        self.board = Board(window)
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

    def tick(self):
        for entity in self.board.entities:
            entity.simulate()
            self.window.moveEntity(entity)
        self.board.sortEntities()
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    simulation = Simulation(window, 30, .5, .5)    
    window.show()
    sys.exit(app.exec_())
