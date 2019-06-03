from random import randint, uniform
from copy import deepcopy

from constants import *
from neuralNetwork import NeuralNetwork
from body import *

# TODO clean up checking for valid entities and indexes
# TODO plants and seeds slowing performance. calculate seed landing cell and 
#      allow plants to be eaten over multiple steps


class Entity:
    def __init__(self, coords):
        self.name = 'Entity'
        self.coords = coords
        self.processed = True
        self.texture = None
        self.label = None
        self.displayPriority = 10
        self.speed = 0
        self.speedBaseline = 0
        self.initializeSpeed()
        
    def generateParameter(self, base=100, variance=0):
        return max(0, base + variance * uniform(-1, 1)) 

    def initializeSpeed(self):
        self.speed = self.speedBaseline = self.generateParameter(0)
    
    def removeFromBoard(self, board):
        board.removeEntityFromBoard(self)

    def die(self, board):
        self.processed = True # ensures entity is not simulated after dying
        board.deleteEntity(self)

    def getStatus(self, board):
        pass

    def randomizeMembers(self):
        pass

    def simulate(self, board):
        pass

    def getCoordsAtDirection(self, direction, magnitude=1):
        '''
        Returns a tuple containing the new coords, with the row as the first element
        and the col as the second. Returned coords must be checked for validity by 
        calling function
        '''
        row, col = self.coords
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

    def moveInDirection(self, board, direction):
        '''
        Moves self to the adjacent cell in the given direction.
        '''
        newRow, newCol = self.getCoordsAtDirection(direction)
        board.moveEntity(self, (newRow, newCol))

    def validCell(self, board, direction):
        '''
        Checks if adjacent cell in the given direction is a valid position on the board.
        '''
        row, col = self.getCoordsAtDirection(direction)
        if not board.validPosition((row, col)):
            return False
        else:
            return True

    def checkForValidEntityFromList(self, board, direction, validClasses):
        '''
        Checks if adjacent cell in specificed direction contains an entity in the validClasses list.
        '''
        row, col = self.getCoordsAtDirection(direction)
        if not board.validPosition((row, col)):
            return False
        for classObject in validClasses:
            if board.cellContains((row, col), classObject):
                return True
            return False
 
    def containsAnimal(self, board, direction):
        '''
        Checks if the adjacent cell in the given direction contains an instance of Animal.
        '''
        row, col = self.getCoordsAtDirection(direction)
        if not board.validPosition((row, col)):
            return False
        elif board.cellContains((row, col), Animal):
            return True
        else:
            return False

    def isEmpty(self, board, direction):
        '''
        Checks if the adjacent cell in the given direction is a valid board position and if it is empty.
        '''
        row, col = self.getCoordsAtDirection(direction)
        if not board.validPosition((row, col)):
            return False
        elif len(board[row][col]) == 0:
            return True
        else:
            return False 


class Particle(Entity): 
    '''
    Particles start at an altitude above ground level and float to adjacent cells until they hit the
    ground. Particles behave independently of other entities and can therefore be simulated in parallel. 
    '''
    def __init__(self, coords, sourceClass, count=1000, diffusionRate=.1, decayRate=.1):
        super().__init__(coords)
        self.name = 'Particle'
        self.sourceClass = sourceClass
        self.count = count
        self.diffusionRate = diffusionRate # the fraction of count that will diffuse to adjacent cells
        self.decayRate = decayRate

    def addToBoard(self, board, coords):
        row, col = coords
        board[row][col].particles.append(self)
        board.entities.append(self)

    def removeFromBoard(self, board, coords):
        row, col = coords
        board[row][col].particles.remove(self)
        board.entities.remove(self)

    @classmethod
    def generate(cls, board, source, amount):
        row, col = source.coords
        cell = board[row][col]
        for particle in cell.particles:
            if particle.sourceClass == source.__class__:
                particle.count += amount
                return
        newParticle = Particle(source.coords, source.__class__, amount)
        cell.particles.append(newParticle)
        board.entities.append(newParticle)

    def transferOut(self, board, coords, amount):
        if not board.validPosition(coords):
                return
        amount = min(amount, self.count)
        self.count -= amount
        row, col = coords 
        cell = board[row][col]
        for particle in cell.particles: 
            if particle.sourceClass == self.sourceClass:
                particle.count += amount
                return
        newParticle = Particle(coords, self.sourceClass, amount)  
        newParticle.addToBoard(board, coords)    

    def decay(self, board):
        if self.count <= 0:
            return
        row, col = self.coords
        self.count -= 5 + int(self.decayRate * self.count)

    def diffuse(self, board):
        if self.count <= 0:
            return
        row, col = self.coords
        cell = board[row][col]
        directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        diffusingParticlesPerDirection = int(self.count * self.diffusionRate / len(directions)) 
        self.count -= diffusingParticlesPerDirection * len(directions) 
        for direction in directions:
            adjCoords = self.getCoordsAtDirection(board, direction)
            self.transferOut(board, adjCoords, diffusingParticlesPerDirection)                            
    
    def die(self, board):
        row, col = self.coords
        self.removeFromBoard(board, self.coords)

    def simulate(self, board):
        self.decay(board)
        self.diffuse(board)

    def getStatus(self, board):
        if self.count <= 0:
            self.die(board)


class Organism(Entity):
    def __init__(self, coords, generation=0, randomize=False):
        super().__init__(coords)
        self.name = 'Organism'
        self.generation = generation
        self.displayPriority = 5
        self.age = 0 # time steps
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

    def getStatus(self, board):
        if self.health <= 0:
            return self.die(board)
     

class Animal(Organism):
    def __init__(self, coords, generation=0, mass=50, massCapacity=100, randomize=False):
        super().__init__(coords, generation, randomize)
        self.name = 'Animal'
        self.displayPriority = 1
        self.diet = []
        self.body = AnimalBody(mass, massCapacity)
        self.nose = Nose()
        self.brain = Brain()
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

    def getStatus(self, board):
        super().getStatus(board)
        if self.body.starved():
            self.die(board)

    def decrementStepsToBreed(self):
        if self.remainingStepsToBreed > 0:
            self.remainingStepsToBreed -= 1

    def resetStepsToBreed(self):
        self.remainingStepsToBreed = self.stepsToBreed

    def simulate(self, board):
        self.body.baselineEnergyExpenditure()
        self.move(board)
        self.body.metabolize()
        self.emanateScent(board)        
        self.age += 1

    def emanateScent(self, board):
        Particle.generate(board, self, 75)

    def move(self, board):
        possibleMoves = ['N', 'E', 'S', 'W']
        hasMoved = False
        while len(possibleMoves) > 0 and not hasMoved:
            roll = randint(0, len(possibleMoves) - 1)
            direction = possibleMoves[roll]
            if not self.containsAnimal(board, direction) and self.validCell(board, direction):
                self.moveInDirection(board, direction)
                self.body.actionEnergyExpenditure(1)
                hasMoved = True
            else:
                possibleMoves.remove(direction)

    def attemptToEat(self, board):
        directions = ['N', 'E', 'S', 'W']
        hasEaten = False
        while len(directions) > 0 and not hasEaten:
            roll = randint(0, len(directions) - 1)
            direction = directions[roll]
            if self.checkForValidEntityFromList(board, direction, self.diet) and not self.containsAnimal(board, direction):
                coords = self.getCoordsAtDirection(direction)
                prey = board.getEntityOfClasses(coords, self.diet)
                self.body.actionEnergyExpenditure(uniform(1, 3))
                self.body.eat(prey)
                prey.die(board)
                self.moveInDirection(board, direction)
                hasEaten = True
            else:
                directions.remove(directions[roll])
        return hasEaten

    def attemptToBreed(self, board):
        hasBred = False
        if self.remainingStepsToBreed <= 0 and self.body.canReproduce() and self.age >= self.maturityAge:     
            possibleSpaces = ['N', 'E', 'S', 'W']
            while len(possibleSpaces) > 0 and not hasBred:
                roll = randint(0, len(possibleSpaces) - 1)
                direction = possibleSpaces[roll]
                if not self.containsAnimal(board, direction) and self.validCell(board, direction):
                    self.breed(board, direction)
                    self.body.actionEnergyExpenditure(uniform(2, 4))
                    hasBred = True
                else:
                    possibleSpaces.remove(direction)
            self.resetStepsToBreed()
        if not hasBred:
            self.decrementStepsToBreed()
        return hasBred
    
    def breed(self, board, direction):
        newCoords = self.getCoordsAtDirection(direction)
        newAnimal = self.__class__(newCoords, self.generation + 1)
        newAnimal.brain = deepcopy(self.brain)
        newAnimal.brain.mutate()
        board.addEntity(newAnimal, newCoords)


class Herbivore(Animal):
    def __init__(self, coords, generation=0, mass=30, massCapacity=60, randomize=False):
        super().__init__(coords, generation, mass, massCapacity, randomize)
        self.name ='Herbivore'
        self.texture = 'assets/blueCircle.png'
        self.diet.append(Plant)
        self.maturityAge = 15
        self.stepsToBreed = randint(12, 20)

    def move(self, board):
        if not self.attemptToEat(board):
            if randint(1, 100) <= 10:
                super().move(board)
        self.attemptToBreed(board)


class Carnivore(Animal):
    def __init__(self, coords, generation=0, mass=50, massCapacity=200, randomize=False):
        super().__init__(coords, generation, mass, massCapacity, randomize)
        self.name = 'Carnivore'
        self.texture = 'assets/orangeCircle.png'
        self.diet.append(Herbivore)
        self.maturityAge = 13
        self.stepsToBreed = randint(10, 15)

    def move(self, board):
        scents = self.nose.smell(self, board, Herbivore)
        decision, value = max(enumerate(self.brain.decide(scents)), key=lambda p: p[1])
        if not decision == 4:
            self.body.actionEnergyExpenditure(uniform(.25, .4))  # caloric penalty for searcing for a valid move if not necessary
            directions = ['N', 'E', 'S', 'W']
            direction = directions[decision]
            coords = board.getCoordsAtDirection(self.coords, direction)
            if board.validPosition(coords) and not board.cellContains(coords, self.__class__):
                self.body.actionEnergyExpenditure(uniform(.6, 1))
                self.moveInDirection(board, direction) 
                self.label.raise_()
        if self.body.hungry:
            self.attemptToEat(board)       
        self.attemptToBreed(board)

    def die(self, board):
        if board.carnivores == 1:
            board.carnivoreTemplate = self
        super().die(board)
        board.carnivores -= 1

    def breed(self, board, direction):
        super().breed(board, direction)
        board.carnivores += 1

    def attemptToEat(self, board):
        if board.cellContains(self.coords, Herbivore):
            prey = board.getEntityOfClass(self.coords, Herbivore)
            self.body.actionEnergyExpenditure(uniform(1, 3))
            self.body.eat(prey)
            prey.die(board)
            return True
        return False


class Plant(Organism):
    def __init__(self, coords, generation=0, mass=1, massCapacity=35, germinationChance=30):
        super().__init__(coords, generation)
        self.name = 'Plant'
        self.displayPriority = 5
        self.texture = 'assets/plant.png'
        self.body = PlantBody(mass, massCapacity)
        self.germinationChance = germinationChance

    def simulate(self, board):
        self.spreadSeeds(board)
        self.body.grow()

    def spreadSeeds(self, board):
        for _ in range(randint(1, 5)):
            directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
            direction = directions[randint(0, len(directions) - 1)]
            magnitude = randint(1, 10)
            coords = self.getCoordsAtDirection(direction, magnitude)
            if board.validPosition(coords):
                if not board.cellContains(coords, Plant) and not board.cellContains(coords, Seed):
                    board.addEntity(Seed(coords, self.generation + 1, randint(12, 20)), coords)
    

class Seed(Organism):
    def __init__(self, coords, generation=0, daysToSprout=6):
        super().__init__(coords, generation)
        self.name = 'Seed'
        self.daysToSprout = daysToSprout

    def simulate(self, board):
        if self.daysToSprout > 0:
            self.daysToSprout -= 1
        else:
            self.sprout(board)
                
    def sprout(self, board):
        board.replaceEntity(self, Plant(self.coords, self.generation, 20))
    
