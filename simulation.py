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
        self.board = [[[None] for col in range(self.cols)] for row in range(self.rows)]
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
        i = 0
        while (i < len(self.board[entity.row][entity.col]) and 
              entity.cellPriority > self.board[entity.row][entity.col][i].cellPriority):
            i += 1 
        self.board[entity.row][entity.col].insert(i, entity)
 
    # removes entity from board, but leaves it in the entities list
    def removeEntityFromBoard(self, entity):
        row = entity.row
        col = entity.col
        entity.row = None
        entity.col = None
        self.board[row][col].remove(entity)

    # completely destroys entity
    def deleteEntity(self, entity):
        self.entities.remove(entity)
        self.removeEntityFromBoard(entity)
        entity.label.hide()

    # returns entity at the front of the list at the given coords
    def getEntity(self, coords):
        row, col = coords
        return self.board[row][col][0]

    def getEntityOfClass(self, coords, classObject):
        row, col = coords
        for entity in self.board[row][col]:
            if isinstance(entity, classObject):
                return entity
        return None

    def getEntityofClasses(self, coords, classList):
        row, col = coords
        for entity in self.board[row][col]:
            for classObject in classList:
                if isinstance(entity, classObject):
                    return entity
        return None     

    # checks if cell contains an instance of the given class
    def cellContains(self, coords, classObject):
        row, col = coords
        for entity in self.board[row][col]:
            if isinstance(entity, classObject):
                return True
        return False

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

    def raiseLabels(self):
        for entity in entities:
            cell = self.board[entity.row][entity.col]
            for i in range(len(cell), 0):
                cell[i].label.raise_()

    def sortEntities(self):
        self.entities.sort(key=lambda x: x.speed, reverse=True) # faster entities go first

    def populateBoard(self):
        herbivoreChance = 1
        carnivoreChance = 0
        plantChance = 8
        for row in range(self.rows):
            for col in range(self.cols):
                roll = rand.randint(1, 100)
                if roll <= herbivoreChance:
                    self.addEntity(entities.Herbivore(self), (row, col))
                elif roll <= herbivoreChance + carnivoreChance:
                    self.addEntity(entities.Carnivore(self), (row, col))
                elif roll <= herbivoreChance + carnivoreChance + plantChance:
                    self.addEntity(entities.Plant(self, rand.randint(2, 4)), (row, col))

class Simulation:
    def __init__(self, window, iterations=10, waitBetweenEntities=0.25, waitBetweenRounds=0):
        self.board = Board(window, 10, 10)
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
            entity.getStatus()
        self.board.sortEntities()
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    simulation = Simulation(window, 30, .5, .25)    
    window.show()
    sys.exit(app.exec_())
