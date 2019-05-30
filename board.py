from random import randint

from entities import *


class Cell:
    def __init__(self):
        self.particles = []
        self.incomingParticles = []
        self.outgoingParticles = []
        self.organisms = []
        
                     
class Board:
    def __init__(self, window, rows=20, cols=30):
        self.window = window
        self.rows = rows
        self.cols = cols
        self.entities = []
        self.board = [[Cell() for col in range(self.cols)] for row in range(self.rows)]
        self.populateBoard() # TODO uncomment
        # self.addEntity(Carnivore((1, 1)), (1, 1)) # TODO remove
        # self.addEntity(Herbivore((3, 1)), (3, 1)) # TODO remove
        # self.addEntity(Herbivore((1, 2)), (1, 2)) # TODO remove
        # self.addEntity(Herbivore((2, 2)), (2, 2)) # TODO remove
        # self.addEntity(Herbivore((10, 10)), (10, 10)) # TODO remove

    def __getitem__(self, row):
        return self.board[row]

    def queueEntities(self):
        for entity in self.entities:
            entity.processed = False

    def addEntity(self, entity, coords):
        '''
        Adds entity to list corresponding to the class of entity and inserts it into the cell
        at coords. Cell order is based on entity.displayPriority
        '''
        entity.coords = coords
        row, col = coords
        if entity not in self.entities:
            self.entities.append(entity)
            self.window.addEntity(entity)
        i = 0
        cellEntities = self.board[row][col].organisms
        if len(cellEntities) == 0:
            cellEntities.insert(0, entity)
        else:
            while i < len(cellEntities) and entity.displayPriority > cellEntities[i].displayPriority:
                i += 1 
            cellEntities.insert(i, entity)
 
    def removeEntityFromBoard(self, entity):
        '''
        Removes entity from board, but leaves it in the entities list.
        '''
        row, col = entity.coords
        entity.coords = None
        self.board[row][col].organisms.remove(entity)

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
        row, col = target.coords
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
        entities = []
        for entity in self.board[row][col].organisms:
            if isinstance(entity, classObject):
                entities.append(entity)
        return entities
        
    def getEntityOfClasses(self, coords, classes):
        '''
        Iterates over list at given coords and returns first instance of any object in classes encountered.
        '''
        row, col = coords
        for entity in self.board[row][col].organisms:
            for classObject in classes:
                if isinstance(entity, classObject):
                    return entity
        return None     

    def cellContains(self, coords, classObject):
        '''
        Checks if cell at coords contains an instance of classObject.
        '''
        row, col = coords
        if classObject is None:
            if len(self.board[row][col].organisms) == 0:
                return True
            else:
                return False
        for entity in self.board[row][col].organisms:
            if isinstance(entity, classObject):
                return True
        return False

    def moveEntity(self, entity, coords):
        '''
        Inserts entity to the front of the list at the given coords
        and removes entity from previous location.
        '''
        row, col = coords
        entityRow, entityCol = entity.coords
        if entityRow is not None and entityCol is not None:
            self.removeEntityFromBoard(entity)
        entity.coords = (row, col)
        self.addEntity(entity, coords)

    def getCoordsAtDirection(self, initialCoords, direction, magnitude=1):
        '''
        Returns a tuple containing the new coords, with the row as the first element
        and the col as the second. Returned coords must be checked for validity by 
        calling function
        '''
        row, col = initialCoords
        if direction == 'N':
            row -= magnitude
        elif direction == 'NE':
            row -= magnitude
            col += magnitude
        elif direction == 'E':
            col += magnitude
        elif direction == 'SE':
            row += magnitude
            col += magnitude
        elif direction == 'S':
            row += magnitude
        elif direction == 'SW':
            row += magnitude
            col -= magnitude
        elif direction == 'W':
            col -= magnitude
        elif direction == 'NW':
            row -= magnitude
            col -= magnitude
        return (row, col)

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
            row, col = entity.coords
            cellEntities = self.board[row][col].organisms
            for i in reversed(range(len(cellEntities))):
                if cellEntities[i].label:
                    cellEntities[i].label.raise_()

    def sortEntities(self):
        self.entities.sort(key=lambda x: x.speed, reverse=True) # faster entities go first

    def populateBoard(self):
        herbivoreChance = 8
        carnivoreChance = 1
        plantChance = 70
        for row in range(self.rows):
            for col in range(self.cols):
                roll = randint(1, 100)
                coords = (row, col)
                if roll <= plantChance:
                    self.addEntity(Plant(coords, randint(10, 35)), coords)
                if roll <= herbivoreChance:
                    self.addEntity(Herbivore(coords), coords)
                elif roll <= herbivoreChance + carnivoreChance:
                    self.addEntity(Carnivore(coords), coords)

    def mapToBoard(self, function):
        '''
        Calls function on every Cell in self.
        '''
        for row in self.rows:
            for col in self.cols:
                function(self.board[row][col])

    def consolidateParticles(self, board):
        for row in range(self.rows):
            for col in range(self.cols):
                self.board[row][col].consolidateParticles(board)