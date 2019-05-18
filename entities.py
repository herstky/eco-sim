from random import randint, uniform

from constants import *
from body import *
from particles import *

# TODO clean up checking for valid entities and indexes
# TODO plants and seeds slowing performance. calculate seed landing cell and 
#      allow plants to be eaten over multiple steps


class Entity:
    def __init__(self, board):
        self.board = board
        self.name = 'Entity'
        self.processed = True
        self.texture = None
        self.label = None
        self.row = None
        self.col = None
        self.displayPriority = 10
        self.speed = 0
        self.speedBaseline = 0
        self.initializeSpeed()
        
    def generateParameter(self, base=100, variance=0):
        return max(0, base + variance * uniform(-1, 1)) 

    def initializeSpeed(self):
        self.speed = self.speedBaseline = self.generateParameter(0)
    
    def removeFromBoard(self):
        self.board.removeEntityFromBoard(self)

    def die(self):
        self.processed = True # ensures entity is not simulated after dying
        self.board.deleteEntity(self)

    def getStatus(self):
        pass

    def randomizeMembers(self):
        pass

    def getCoordsAtDirection(self, direction, magnitude=1):
        '''
        Returns a tuple containing the new coords, with the row as the first element
        and the col as the second. Returned coords must be checked for validity by 
        calling function
        '''
        row = self.row
        col = self.col
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

    def moveInDirection(self, direction):
        '''
        Moves self to the adjacent cell in the given direction.
        '''
        newRow, newCol = self.getCoordsAtDirection(direction)
        self.board.moveEntity(self, (newRow, newCol))

    def validCell(self, direction):
        '''
        Checks if adjacent cell in the given direction is a valid position on the board.
        '''
        row, col = self.getCoordsAtDirection(direction)
        if not self.board.validPosition((row, col)):
            return False
        else:
            return True

    def checkForValidEntityFromList(self, direction, validClasses):
        '''
        Checks if adjacent cell in specificed direction contains an entity in the validClasses list.
        '''
        row, col = self.getCoordsAtDirection(direction)
        if not self.board.validPosition((row, col)):
            return False
        for classObject in validClasses:
            if self.board.cellContains((row, col), classObject):
                return True
            return False
 
    def containsAnimal(self, direction):
        '''
        Checks if the adjacent cell in the given direction contains an instance of Animal.
        '''
        row, col = self.getCoordsAtDirection(direction)
        if not self.board.validPosition((row, col)):
            return False
        elif self.board.cellContains((row, col), Animal):
            return True
        else:
            return False

    def isEmpty(self, direction):
        '''
        Checks if the adjacent cell in the given direction is a valid board position and if it is empty.
        '''
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
        self.displayPriority = 5
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

    def randomizeMembers(self):
        self.age = randint(0, 10)

    def simulate(self):
        pass

    def getStatus(self):
        if self.health <= 0:
            return self.die()
     

class Animal(Organism):
    def __init__(self, board, mass=50, massCapacity=100, randomize=False):
        super().__init__(board, randomize)
        self.name = 'Animal'
        self.displayPriority = 1
        self.diet = []
        self.body = AnimalBody(mass, massCapacity)
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

    def simulate(self):
        self.body.baselineEnergyExpenditure()
        self.move()
        self.body.metabolize()
        
        self.age += 1

    def emanateScent(self):
        scent = Particle(self.board, self.__class__, (self.row, self.col), 75)
        scent.addToBoard((self.row, self.col))

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
    def __init__(self, board, mass=20, massCapacity=60, randomize=False):
        super().__init__(board, mass, massCapacity, randomize)
        self.name ='Herbivore'
        self.texture = 'assets/blueCircle.png'
        self.diet.append(Plant)
        self.maturityAge = 12
        self.stepsToBreed = randint(9, 13)

    def move(self):
        if not self.attemptToEat():
            super().move()
        self.attemptToBreed()


class Carnivore(Animal):
    def __init__(self, board, mass=50, massCapacity=200, randomize=False):
        super().__init__(board, mass, massCapacity, randomize)
        self.name = 'Carnivore'
        self.texture = 'assets/orangeCircle.png'
        self.diet.append(Herbivore)
        self.maturityAge = 18
        self.stepsToBreed = randint(14, 18)

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
    def __init__(self, board, mass=1, massCapacity=35, germinationChance=30):
        super().__init__(board)
        self.name = 'Plant'
        self.displayPriority = 5
        self.texture = 'assets/plant.png'
        self.body = PlantBody(mass, massCapacity)
        self.germinationChance = germinationChance

    def simulate(self):
        self.spreadSeeds()
        self.body.grow()

    def spreadSeeds(self):
        directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        direction = directions[randint(0, len(directions) - 1)]
        magnitude = randint(1, 10)
        coords = self.getCoordsAtDirection(direction, magnitude)
        if self.board.validPosition(coords):
            if not self.board.cellContains(coords, Plant) and not self.board.cellContains(coords, Seed):
                self.board.addEntity(Seed(self.board, randint(12, 20)), coords)
    

class Seed(Organism):
    def __init__(self, board, daysToSprout=6):
        super().__init__(board)
        self.name = 'Seed'
        self.daysToSprout = daysToSprout

    def simulate(self):
        if self.daysToSprout > 0:
            self.daysToSprout -= 1
        else:
            self.sprout()
                
    def sprout(self):
        self.board.replaceEntity(self, Plant(self.board, 10))
    
