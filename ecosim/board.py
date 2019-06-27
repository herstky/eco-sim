from random import randint
from copy import deepcopy

from ecosim.entities import *


class Cell:
    def __init__(self):
        self.particles = []
        self.incomingParticles = []
        self.outgoingParticles = []
        self.organisms = []
        
                     
class Board:
    def __init__(self, window, creatureTemplate=None, rows=30, cols=40):
        self.window = window
        self.creatureTemplate = creatureTemplate
        self.rows = rows
        self.cols = cols
        self.entities = []
        self.carnivores = 0
        self.herbivores = 0
        self.oldestHerbivore = 0
        self.board = [[Cell() for col in range(self.cols)] for row in range(self.rows)]
        self.populateBoard()

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
            entity.label.deleteLater()

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
        for entity in self.board[row][col].organisms:
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

    def checkForAdjacentAnimal(self, coords):
        directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        while len(directions) > 0:
            direction = directions[randint(0, len(directions) - 1)]
            coordsAtDirection = self.getCoordsAtDirection(coords, direction)
            if self.cellContains(coordsAtDirection, Animal):
                return True
            else:
                directions.remove(direction)
        return False

    def searchForEmptySpace(self, coords):
        directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        while len(directions) > 0:
            direction = directions[randint(0, len(directions) - 1)]
            coordsAtDirection = self.getCoordsAtDirection(coords, direction)
            if self.validPosition(coordsAtDirection) and not self.cellContains(coordsAtDirection, Animal):
                return self.getCoordsAtDirection(coords, direction)
            else:
                directions.remove(direction)
        return None 

    def searchForAdjacentClass(self, coords, classObj):
        directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        while len(directions) > 0:
            direction = directions[randint(0, len(directions) - 1)]
            coordsAtDirection = self.getCoordsAtDirection(coords, direction)
            if self.cellContains(coordsAtDirection, classObj):
                return self.getCoordsAtDirection(coords, direction)
            else:
                directions.remove(direction)
        return None


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
        and the col as the second. Returned coords should be checked for validity. 
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
        carnivoreChance = 3
        plantChance = 70
        for row in range(self.rows):
            for col in range(self.cols):
                roll = randint(1, 100)
                coords = (row, col)
                if roll <= plantChance:
                    self.addEntity(Plant(coords, 0, randint(10, 25)), coords)
                if roll <= herbivoreChance:
                    if self.creatureTemplate is None:
                        self.addEntity(Herbivore(coords), coords)
                    else:
                        newHerbivore = Herbivore(coords)
                        newHerbivore.brain = deepcopy(self.creatureTemplate.brain)
                        newHerbivore.brain.mutate()
                        self.addEntity(newHerbivore, coords)
                    self.herbivores += 1
                # elif roll <= herbivoreChance + carnivoreChance:
                #     if self.creatureTemplate is None:
                #         self.addEntity(Carnivore(coords), coords)
                #     else:
                #         newCarnivore = Carnivore(coords)
                #         newCarnivore.brain = deepcopy(self.creatureTemplate.brain)
                #         newCarnivore.brain.mutate()
                #         self.addEntity(newCarnivore, coords)
                #     self.carnivores += 1

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