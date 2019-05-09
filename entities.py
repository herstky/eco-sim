import random as rand
from constants import *

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
        self.cellPriority = 5
        self.age = 0 # time steps
        self.maturityAge = 0
        self.health = 0
        self.healthBaseline = 0
        self.initializeHealth() 
        self.speed = 0
        self.speedBaseline = 0
        self.initializeSpeed()
        self.bodyMass = 0 # kg
        self.bodyMassCapacity = 0

    def initializeHealth(self):
        self.health = self.healthBaseline = self.generateParameter()

    def initializeSpeed(self):
        self.speed = self.speedBaseline = self.generateParameter(0)

    def generateParameter(self, base=100, variance=0):
        return max(0, base + variance * rand.uniform(-1, 1)) 

    def getStatus(self):
        if self.health <= 0:
            return self.delete()

class Animal(Organism):
    def __init__(self, board):
        super().__init__(board)
        self.name = 'Animal'
        self.cellPriority = 1
        self.speed = self.calculateSpeed(5, 2)
        self.bodyMass = 10 
        self.bodyMassCapacity = 100
        self.bodyFatMassFraction = .12
        self.bodyMuscleMassFraction = .35
        self.bodyFatStorageFraction = 0
        self.bodyMuscleStorageFraction = 0
        self.initializeMassStorageFractions()
        self.energyReserves = self.bodyMass * self.bodyFatMassFraction * 37000 # kj
        self.totalEnergyExpenditure = 0 # keeps track of the total amount of energy spent during current tick
        self.consumedFoodMass = 0
        self.maxConsumedFoodMass = self.bodyMass * .1 # animal can only consume some percent of its body weight
        self.satiationThreshold = .8
        self.diet = []
        self.satiationAmount = 10
        self.hungerAmount = 10
        self.strength = 0
        self.strengthBaseline = 0
        self.stepsToBreed = 6
        self.remainingStepsToBreed = 0
        self.resetStepsToBreed()
    
    def initializeStrength(self):
        self.strength = self.strengthBaseline = self.generateParameter()

    def initializeMassStorageFractions(self):
        self.bodyFatStorageFraction = self.bodyFatMassFraction / (self.bodyFatMassFraction + self.bodyMuscleMassFraction)
        self.bodyMuscleStorageFraction = 1 - self.bodyFatStorageFraction

    def hungry(self):
        pass

    def eat(self):
        pass

    def digest(self):
        if self.consumedFoodMass > 0:
            amountDigested -= min(self.consumedFoodMass, self.mass * .1)
            self.consumedFoodMass -= amountDigested
            energyGained = 7000 * amountDigested # assuming energy content of 7000 KJ/kg for food consumed
            if self.bodyMass < self.bodyMassCapacity: # if fully grown, all excess energy is stored as fat
                self.bodyMass += (energyGained - self.totalEnergyExpenditure) 
                                 / (self.bodyFatStorageFraction * BODY_FAT_ENERGY_CONTENT + self.bodyMuscleStorageFraction * BODY_MUSCLE_ENERGY_CONTENT)
            else:
                massGained = (energyGained - self.totalEnergyExpenditure) / BODY_FAT_ENERGY_CONTENT



    def baselineEnergyExpenditure(self):
        return 90 * self.bodyMass

    def actionEnergyExpenditure(self, magnitude):
        return magnitude * self.bodyMass * 50 

    def getStatus(self):
        super().getStatus()
        if self.energyReserves <= 0:
            self.delete()

    def decrementStepsToBreed(self):
        if self.remainingStepsToBreed > 0:
            self.remainingStepsToBreed -= 1

    def resetStepsToBreed(self):
        self.remainingStepsToBreed = self.stepsToBreed

    def restoreSatiation(self):
        self.energyReserves += self.satiationAmount
        if self.energyReserves > 100:
            self.energyReserves = 100

    def decrementSatiation(self):
        self.energyReserves -= self.hungerAmount

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
        if not self.board.validPosition((row, col)) or self.board.cellContains((row, col), Animal):
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
                self.board.getEntityOfClasses(coords, self.diet).delete()
                self.moveInDirection(coords)
                self.restoreSatiation()
                hasEaten = True
            else:
                possibleMoves.remove(possibleMoves[roll])
        if not hasEaten:
            self.decrementSatiation()
        return hasEaten

    # checks if adjacent cell in specificed direction contains an entity in the validEntities list
    def checkForValidEntity(self, direction, validClasses):
        row, col = self.getCoordsAtDirection(direction)
        if not self.board.validPosition((row, col)):
            return False
        for classObject in validClasses:
            if self.board.cellContains((row, col), classObject):
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
        self.hungerAmount = 3

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
        self.stepsToBreed = 8

    def move(self):
        if not self.attemptToEat():
            super().move()
        self.attemptToBreed()

class Omnivore(Animal):
    def __init__(self):
        super().__init__()
        self.name = 'Omnivore'
        self.diet.extend((Plant, Animal))

class Plant(Organism):
    def __init__(self, board, size=4):
        super().__init__(board)
        self.name = 'Plant'
        self.cellPriority = 5
        self.texture = 'assets/plant.png'
        self.size = size

    def simulate(self):
        return True

class Scent(Entity):
    def __init__(self, board, intensity=3):
        super().__init__(board)
        self.name = 'Scent'
        self.cellPriority = 4
        self.intensity = intensity
        self.setCharacter()
