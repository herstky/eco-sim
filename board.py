from random import randint

from entities import *


class Cell:
    def __init__(self, board):
        self.board = board
        self.particles = []
        self.incomingParticles = []
        self.outgoingParticles = []
        self.entities = []
        
    def generateParticles(self, particle, coords, count):
        '''
        Creates incomingParticle object based on particle and adds it to the incomingParticles list
        of the Cell at coords.
        '''
        row, col = coords
        incomingParticle = Particle(particle.sourceClass, coords, count)
        self.board[row][col].incomingParticles.append(incomingParticle) 

    def destroyParticles(self, particle, coords, count):
        '''
        Creates outgoingParticle object based on particle and adds it to the outgoingParticles list
        of the Cell at coords.
        '''
        row, col = coords
        outgoingParticle = Particle(particle.sourceClass, coords, count)
        self.board[row][col].outgoingParticles.append(outgoingParticle)

    def transferParticles(self, particle, outputCoords, inputCoords, count):
        outputRow, outputCol = outputCoords
        outgoingParticle = Particle(particle.sourceClass, outputCoords, count)
        self.board[outputRow][outputCol].outgoingParticles.append(outgoingParticle)
        inputRow, inputCol = inputCoords
        incomingParticle = Particle(particle.sourceClass, inputCoords, count)
        self.board[inputRow][inputRow].incomingParticles.append(incomingParticle)

    def mapToParticles(self, function):
        for particle in particles:
            function(particle)

    def mapToEntities(self, function):
        for entity in entities:
            self.function(entity)

    def simulateParticles(self):
        for particle in self.particles:
            particle.simulate()

    def consolidateParticles(self):
        while len(self.incomingParticles) > 0:
            incomingParticle = self.incomingParticles.pop()
            particleAdded = False
            for particle in self.particles:
                if incomingParticle.sourceClass == particle.sourceClass:
                    particle.count += incomingParticle.count
                    particleAdded = True
                    break
            if not particleAdded:    
                self.particles.append(incomingParticle)

        while len(self.outgoingParticles) > 0:
            outgoingParticle = self.outgoingParticles.pop()
            for particle in self.particles:
                if outgoingParticle.sourceClass == particle.sourceClass:
                    particle.count -= outgoingParticle.count
                
        for particle in self.particles:        
            if particle.count <= 0:
                self.particles.remove(particle)
               
                    
class Board:
    def __init__(self, window, rows=20, cols=30):
        self.window = window
        self.rows = rows
        self.cols = cols
        self.entities = []
        self.board = [[Cell(self) for col in range(self.cols)] for row in range(self.rows)]
        self.populateBoard() # TODO uncomment
        # self.addEntity(Herbivore((1, 1)), (1, 1)) # TODO remove

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
        cellEntities = self.board[row][col].entities
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
        self.board[row][col].entities.remove(entity)

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
        for entity in self.board[row][col].entities:
            if isinstance(entity, classObject):
                entities.append(entity)
        return entities
        
    def getEntityOfClasses(self, coords, classes):
        '''
        Iterates over list at given coords and returns first instance of any object in classes encountered.
        '''
        row, col = coords
        for entity in self.board[row][col].entities:
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
            if len(self.board[row][col].entities) == 0:
                return True
            else:
                return False
        for entity in self.board[row][col].entities:
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
            cellEntities = self.board[row][col].entities
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

    # TODO technical debt mounting
    def consolidateParticles(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.board[row][col].consolidateParticles()