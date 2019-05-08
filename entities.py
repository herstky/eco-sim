import random as rand

class Entity:
    def __init__(self, board):
        self.board = board
        self.name = 'Entity'
        self.texture = None
        self.label = None
        self.row = None
        self.col = None
        
    def removeFromBoard(self):
        self.board.removeEntityFromBoard(self)

    def delete(self):
        self.board.deleteEntity(self)

    def getStatus(self):
        pass

class EmptySpace(Entity):
    def __init__(self, board):
        super().__init__(board)
        self.name = 'EmptySpace'

class Organism(Entity):
    def __init__(self, board):
        super().__init__(board)
        self.name = 'Organism'
        self.health = self.calculateHealth()
        self.speed = self.calculateSpeed()
        
    def calculateHealth(self, base=100, variance=0):
        health = base * rand.randint(0, 1) + variance * rand.uniform(-1, 1) 
        return max(health, 0)

    def calculateSpeed(self, base=0, variance=0):
        speed = base * rand.randint(0, 1) + variance * rand.uniform(-1, 1) 
        return max(speed, 0)

    def getStatus(self):
        if self.health <= 0:
            return self.delete()

class Animal(Organism):
    def __init__(self, board):
        super().__init__(board)
        self.name = 'Animal'
        self.speed = self.calculateSpeed(5, 2)
        self.diet = []
        self.satiation = 100
        self.satiationAmount = 10
        self.hungerAmount = 10
        self.stepsPerRound = 1
        self.remainingStepsInRound = self.stepsPerRound
        self.stepsToBreed = 8
        self.remainingStepsToBreed = self.stepsToBreed

    def getStatus(self):
        super().getStatus()
        if self.satiation <= 0:
            self.delete()

    def decrementStepsInRound(self):
        if self.remainingStepsInRound > 0:
            self.remainingStepsInRound -= 1

    def decrementStepsToBreed(self):
        if self.remainingStepsToBreed > 0:
            self.remainingStepsToBreed -= 1

    def resetStepsInRound(self):
        self.remainingStepsInRound = self.stepsPerRound

    def resetStepsToBreed(self):
        self.remainingStepsToBreed = self.stepsToBreed

    def restoreSatiation(self):
        self.satiation += self.satiationAmount
        if self.satiation > 100:
            self.satiation = 100

    def decrementSatiation(self):
        self.satiation -= self.hungerAmount

    # returns a tuple containing the new coords, with the row as the first element
    # and the col as the second. returned coords must be checked for validity by 
    # calling function
    def getCoordsAtDirection(self, direction):
        row = self.row
        col = self.col
        if direction == 'N':
                row -= 1
        elif direction == 'E':
                col += 1
        elif direction == 'S':
                row += 1
        elif direction == 'W':
                col -= 1
        return (row, col)
        
    # checks if the adjacent cell in the given direction is empty
    def isClear(self, direction):
        row, col = self.getCoordsAtDirection(direction)
        if (not self.board.validPosition((row, col)) or 
            not isinstance(self.board.getEntity((row, col)), EmptySpace)):
            return False
        else:
            return True

    # moves the entity to the adjacent cell in the given direction
    def moveInDirection(self, direction):
        newRow, newCol = self.getCoordsAtDirection(direction)
        self.board.moveEntity(self, (newRow, newCol))

    def simulate(self):
        self.move()

    def move(self):
        if self.remainingStepsInRound <= 0: # this must always be checked first
            return 

        possibleMoves = ['N', 'E', 'S', 'W']
        hasMoved = False
        while len(possibleMoves) > 0 and not hasMoved:
            roll = rand.randint(0, len(possibleMoves) - 1)
            direction = possibleMoves[roll]
            if self.isClear(direction):
                self.moveInDirection(direction)
                hasMoved = True
            else:
                possibleMoves.remove(direction)

    def attemptToEat(self):
        possibleMoves = ['N', 'E', 'S', 'W']
        hasEaten = False
        while len(possibleMoves) > 0 and not hasEaten:
            roll = rand.randint(0, len(possibleMoves) - 1)
            direction = possibleMoves[roll]
            if self.checkForValidEntity(direction, self.diet):
                coords = self.getCoordsAtDirection(direction)
                self.board.getEntity(coords).delete()
                self.moveInDirection(coords)
                self.restoreSatiation()
                hasEaten = True
            else:
                possibleMoves.remove(possibleMoves[roll])
        if not hasEaten:
            self.decrementSatiation()
        return hasEaten

    # checks if adjacent cell in specificed direction contains an entity in the validEntities list
    def checkForValidEntity(self, direction, validEntities):
        row, col = self.getCoordsAtDirection(direction)
        if not self.board.validPosition((row, col)):
            return False
        for entity in validEntities:
            if isinstance(self.board.getEntity((row, col)), entity):
                return True
            return False

    def attemptToBreed(self):
        hasBred = False
        if self.remainingStepsToBreed <= 0:     
            possibleSpaces = ['N', 'E', 'S', 'W']
            while len(possibleSpaces) > 0 and not hasBred:
                roll = rand.randint(0, len(possibleSpaces) - 1)
                direction = possibleSpaces[roll]
                if self.isClear(direction):
                    self.breed(direction)
                    self.resetStepsToBreed()
                    hasBred = True
                else:
                    possibleSpaces.remove(direction)
        if not hasBred:
            self.decrementStepsToBreed()
        return hasBred
    
    def breed(self, direction):
        newRow, newCol = self.getCoordsAtDirection(direction)
        self.board.addEntity(self.__class__(self.board), (newRow, newCol))



class Herbivore(Animal):
    def __init__(self, board):
        super().__init__(board)
        self.name ='Herbivore'
        self.texture = 'assets/blueCircle.png'
        self.diet.append(Plant)
        self.hungerAmount = 1

    def move(self):
        if not self.attemptToEat():
            super().move()
        self.attemptToBreed()

class Carnivore(Animal):
    def __init__(self, board):
        super().__init__(board)
        self.name = 'Carnivore'
        self.texture = 'assets/orangeCircle.png'
        self.diet.append(Herbivore)
        self.hungerAmount = 15
        self.satiationAmount = 50

    def move(self):
        if not self.attemptToEat():
            super().move()
        self.attemptToBreed()

class Omnivore(Animal):
    def __init__(self):
        super().__init__()
        self.name = 'Omnivore'
        self.diet.extend((Plant, Animal))

class Plant(Entity):
    def __init__(self, board, size=4):
        super().__init__(board)
        self.name = 'Plant'
        self.characters = ['.', ':',';', '#']
        self.size = size
        self.setCharacter()

    def setCharacter(self):
        self.character = self.characters[self.size - 1]

    def simulate(self):
        return True

class Scent(Entity):
    def __init__(self, board, intensity=3):
        super().__init__(board)
        self.name = 'Scent'
        self.intensity = intensity
        self.setCharacter()
