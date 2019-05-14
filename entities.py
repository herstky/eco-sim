from random import randint, uniform
from constants import *
from body import *

# TODO clean up checking for valid entities and indexes
# TODO tune animal starvation


class Entity:
    def __init__(self, board):
        self.board = board
        self.name = 'Entity'
        self.texture = None
        self.label = None
        self.row = None
        self.col = None
        self.cellPriority = 10
        
    def removeFromBoard(self):
        self.board.removeEntityFromBoard(self)

    def die(self):
        self.board.deleteEntity(self)

    def getStatus(self):
        pass

    def randomizeMembers(self):
        pass

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

    def validCell(self, direction):
        row, col = self.getCoordsAtDirection(direction)
        if not self.board.validPosition((row, col)):
            return False
        else:
            return True

    # checks if adjacent cell in specificed direction contains an entity in the validEntities list
    def checkForValidEntityFromList(self, direction, validClasses):
        row, col = self.getCoordsAtDirection(direction)
        if not self.board.validPosition((row, col)):
            return False
        for classObject in validClasses:
            if self.board.cellContains((row, col), classObject):
                return True
            return False

    # checks if the adjacent cell in the given direction contains a given object
    def containsAnimal(self, direction):
        row, col = self.getCoordsAtDirection(direction)
        if not self.board.validPosition((row, col)):
            return False
        elif self.board.cellContains((row, col), Animal):
            return True
        else:
            return False

    # checks if the adjacent cell in the given direction is a valid cell and if it is empty
    def isEmpty(self, direction):
        row, col = self.getCoordsAtDirection(direction)
        if not self.board.validPosition((row, col)):
            return False
        elif len(self.board[row][col]) == 0:
            return True
        else:
            return False 


class Organism(Entity):
    def __init__(self, board, randomize=False):
        super().__init__(board)
        self.name = 'Organism'
        self.cellPriority = 5
        self.age = 0 # time steps
        self.generation = 0
        self.maturityAge = 0
        self.health = 0
        self.healthBaseline = 0
        self.initializeHealth() 
        self.speed = 0
        self.speedBaseline = 0
        self.initializeSpeed()
        if randomize:
            self.randomizeMembers()

    def initializeHealth(self):
        self.health = self.healthBaseline = self.generateParameter()

    def initializeSpeed(self):
        self.speed = self.speedBaseline = self.generateParameter(0)

    def generateParameter(self, base=100, variance=0):
        return max(0, base + variance * uniform(-1, 1)) 

    def randomizeMembers(self):
        self.age = randint(0, 10)

    def simulate(self):
        pass

    def getStatus(self):
        if self.health <= 0:
            return self.die()
     

class Animal(Organism):
    def __init__(self, board, randomize=False):
        super().__init__(board, randomize)
        self.name = 'Animal'
        self.cellPriority = 1
        self.diet = []
        self.body = AnimalBody()
        self.strength = 0
        self.strengthBaseline = 0
        self.stepsToBreed = 6
        self.remainingStepsToBreed = 0
        self.resetStepsToBreed()
        if randomize:
            self.randomizeMembers()
    
    def initializeStrength(self):
        self.strength = self.strengthBaseline = self.generateParameter()

    def randomizeMembers(self):
        self.body.stomachContentsMass = self.body.stomachCapacity * uniform(0, 1)
        self.body.fatMassFraction = uniform(.15, .25)
        self.body.muscleMassFraction = uniform(.30, .40)

    def getStatus(self):
        super().getStatus()
        if self.body.starved():
            self.die()

    def decrementStepsToBreed(self):
        if self.remainingStepsToBreed > 0:
            self.remainingStepsToBreed -= 1

    def resetStepsToBreed(self):
        self.remainingStepsToBreed = self.stepsToBreed

    # moves the entity to the adjacent cell in the given direction
    def moveInDirection(self, direction):
        newRow, newCol = self.getCoordsAtDirection(direction)
        self.board.moveEntity(self, (newRow, newCol))

    def simulate(self):
        self.body.baselineEnergyExpenditure()
        self.move()
        self.body.metabolize()
        self.age += 1

    def move(self):
        possibleMoves = ['N', 'E', 'S', 'W']
        hasMoved = False
        while len(possibleMoves) > 0 and not hasMoved:
            roll = randint(0, len(possibleMoves) - 1)
            direction = possibleMoves[roll]
            if not self.containsAnimal(direction) and self.validCell(direction):
                self.moveInDirection(direction)
                self.body.actionEnergyExpenditure(1)
                hasMoved = True
            else:
                possibleMoves.remove(direction)

    def attemptToEat(self):
        possibleMoves = ['N', 'E', 'S', 'W']
        hasEaten = False
        while len(possibleMoves) > 0 and not hasEaten:
            roll = randint(0, len(possibleMoves) - 1)
            direction = possibleMoves[roll]
            if self.checkForValidEntityFromList(direction, self.diet):
                coords = self.getCoordsAtDirection(direction)
                prey = self.board.getEntityOfClasses(coords, self.diet)
                self.body.actionEnergyExpenditure(uniform(1, 3))
                self.body.eat(prey)
                prey.die()
                self.moveInDirection(direction)
                hasEaten = True
            else:
                possibleMoves.remove(possibleMoves[roll])
        return hasEaten

    def attemptToBreed(self):
        hasBred = False
        if self.remainingStepsToBreed <= 0 and self.body.canReproduce() and self.age >= self.maturityAge:     
            possibleSpaces = ['N', 'E', 'S', 'W']
            while len(possibleSpaces) > 0 and not hasBred:
                roll = randint(0, len(possibleSpaces) - 1)
                direction = possibleSpaces[roll]
                if not self.containsAnimal(direction) and self.validCell(direction):
                    self.breed(direction)
                    self.body.actionEnergyExpenditure(uniform(2, 4))
                    hasBred = True
                else:
                    possibleSpaces.remove(direction)
            self.resetStepsToBreed()
        if not hasBred:
            self.decrementStepsToBreed()
        return hasBred
    
    def breed(self, direction):
        newRow, newCol = self.getCoordsAtDirection(direction)
        self.board.addEntity(self.__class__(self.board), (newRow, newCol))


class Herbivore(Animal):
    def __init__(self, board, randomize=False):
        super().__init__(board, randomize)
        self.name ='Herbivore'
        self.texture = 'assets/blueCircle.png'
        self.diet.append(Plant)
        self.maturityAge = 15
        self.stepsToBreed = randint(3, 6)

    def move(self):
        if not self.attemptToEat():
            super().move()
        self.attemptToBreed()


class Carnivore(Animal):
    def __init__(self, board, randomize=False):
        super().__init__(board, randomize)
        self.name = 'Carnivore'
        self.texture = 'assets/orangeCircle.png'
        self.diet.append(Herbivore)
        self.maturityAge = 20
        self.stepsToBreed = randint(8, 12)

    def move(self):
        hasEaten = False
        if self.body.hungry:
            hasEaten = self.attemptToEat()
        if not hasEaten:
            super().move()
        self.attemptToBreed()


class Omnivore(Animal):
    def __init__(self):
        super().__init__()
        self.name = 'Omnivore'
        self.diet.extend((Plant, Animal))


class Plant(Organism):
    def __init__(self, board, mass=20, germinationChance=.1):
        super().__init__(board)
        self.name = 'Plant'
        self.cellPriority = 5
        self.texture = 'assets/plant.png'
        self.body = Body(mass, 15)
        self.germinationChance = germinationChance

    def simulate(self):
        self.reproduce()
        pass

    def reproduce(self):
        directions = ['N', 'E', 'S', 'W']
        for direction in directions:
            roll = uniform(0, 1)
            if roll <= self.germinationChance and self.isEmpty(direction) and self.validCell(direction):
                coords = self.getCoordsAtDirection(direction)
                self.board.addEntity(self.__class__(self.board, 1), coords)


class Scent(Entity):
    def __init__(self, board, intensity=3):
        super().__init__(board)
        self.name = 'Scent'
        self.cellPriority = 4
        self.intensity = intensity
        self.setCharacter()
