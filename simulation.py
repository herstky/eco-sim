from entities import *
from random import randint
from time import sleep

from gui import *

class Board:
    def __init__(self, window, rows=20, cols=30):
        self.window = window
        self.rows = rows
        self.cols = cols
        self.entities = []
        self.board = [[[] for col in range(self.cols)] for row in range(self.rows)]
        self.populateBoard()

    def __getitem__(self, row):
        return self.board[row]

    def addEntity(self, entity, coords):
        '''
        Adds entity to entities list and inserts it to the front of the list at the given coords.
        '''
        entity.row, entity.col = coords
        if entity not in self.entities:
            self.entities.append(entity)
        if not entity.label:
            self.window.addEntity(entity)
        i = 0
        cell = self.board[entity.row][entity.col]
        if len(cell) == 0:
            cell.insert(0, entity)
        else:
            while i < len(cell) and entity.displayPriority > cell[i].displayPriority:
                i += 1 
            cell.insert(i, entity)
 
    
    def removeEntityFromBoard(self, entity):
        '''
        Removes entity from board, but leaves it in the entities list.
        '''
        row = entity.row
        col = entity.col
        entity.row = None
        entity.col = None
        self.board[row][col].remove(entity)

    def deleteEntity(self, entity):
        '''
        Completely destroys entity.
        '''
        self.entities.remove(entity)
        self.removeEntityFromBoard(entity)
        if entity.label:
            entity.label.hide()

    def replaceEntity(self, target, replacement):
        '''
        Completely destroys target and replaces it with replacement.
        '''
        row = target.row
        col = target.col
        self.addEntity(replacement, (row, col))
        self.deleteEntity(target)

    def getEntity(self, coords):
        '''
        Returns entity at the front of the list at the given coords.

        '''
        row, col = coords
        return self.board[row][col][0]

    def getEntityOfClass(self, coords, classObject):
        '''
        Iterates over list at given coords and returns the first instance of classObject encountered.
        '''
        row, col = coords
        for entity in self.board[row][col]:
            if isinstance(entity, classObject):
                return entity
        return None

    def getEntitiesOfClass(self, coords, classObject):
        '''
        Iterates over list at given coords and returns a list of all instances of classObject encountered.
        '''
        row, col = coords
        entityList = []
        for entity in self.board[row][col]:
            if isinstance(entity, classObject):
                entityList.append(entity)
        return entityList
        
    def getEntityOfClasses(self, coords, classList):
        '''
        Iterates over list at given coords and returns first instance of any object in classList encountered.
        '''
        row, col = coords
        for entity in self.board[row][col]:
            for classObject in classList:
                if isinstance(entity, classObject):
                    return entity
        return None     

    def cellContains(self, coords, classObject):
        '''
        Checks if cell at coords contains an instance of classObject.
        '''
        row, col = coords
        if classObject is None:
            if len(self.board[row][col]) == 0:
                return True
            else:
                return False
        for entity in self.board[row][col]:
            if isinstance(entity, classObject):
                return True
        return False

    def moveEntity(self, entity, coords):
        '''
        Inserts entity to the front of the list at the given coords
        and removes entity from previous location.
        '''
        row, col = coords
        if entity.row is not None and entity.col is not None:
            self.removeEntityFromBoard(entity)
        entity.row = row
        entity.col = col
        self.addEntity(entity, coords)

    def validPosition(self, coords):
        '''
        Checks if coords are a valid position on the board.
        '''
        row, col = coords
        if row < 0 or row > self.rows - 1 or col < 0 or col > self.cols - 1:
            return False
        else:
            return True

    def raiseLabels(self):
        '''
        Raises labels so that labels with the highest priorities appear on top.
        '''
        for entity in self.entities:
            cell = self.board[entity.row][entity.col]
            for i in reversed(range(len(cell))):
                if cell[i].label:
                    cell[i].label.raise_()

    def sortEntities(self):
        self.entities.sort(key=lambda x: x.speed, reverse=True) # faster entities go first

    def populateBoard(self):
        herbivoreChance = 8
        carnivoreChance = 1
        plantChance = 70
        for row in range(self.rows):
            for col in range(self.cols):
                roll = randint(1, 100)
                if roll <= plantChance:
                    self.addEntity(Plant(self, randint(10, 35)), (row, col))
                if roll <= herbivoreChance:
                    self.addEntity(Herbivore(self), (row, col))
                elif roll <= herbivoreChance + carnivoreChance:
                    self.addEntity(Carnivore(self), (row, col))

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
            entity.getStatus()
        self.board.sortEntities()
        self.board.raiseLabels()
        print(len(self.board.entities))
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    simulation = Simulation(window, 30, .5, .25)    
    window.show()
    sys.exit(app.exec_())
