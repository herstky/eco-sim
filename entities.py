import random as rand

class Entity:
    def __init__(self):
        self.name = 'Entity'
        self.character = ' '

class Animal(Entity):
    def __init__(self):
        self.name = 'Animal'
        self.character = '@'
        self.diet = []
        self.satiation = 100
        self.hungerAmount = 10
        self.stepsPerRound = 1
        self.remainingStepsInRound = self.stepsPerRound
        self.stepsToBreed = 8
        self.remainingStepsToBreed = self.stepsToBreed

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

    def restoreSatiation(self, amount=10):
        self.satiation += amount
        if self.satiation > 100:
            self.satiation = 100

    def depleteSatiation(self, position):
        self.satiation -= self.hungerAmount
        if self.satiation <= 0:
            self.die(position)

    def die(self, position):
        board, row, col = position
        board[row][col] = [Entity()]

    # returns a tuple containing the new coords, with the row as the first element
    # and the col as the second. returned coords must be checked for validity by 
    # calling function
    def getNewCoords(self, position, direction):
        row, col = position[1:]
        if direction == 'N':
                row -= 1
        elif direction == 'E':
                col += 1
        elif direction == 'S':
                row += 1
        elif direction == 'W':
                col -= 1
        return (row, col)
        
    def isClear(self, position, direction):
        board = position[0]
        row, col = self.getNewCoords(position, direction)
        if row < 0 or row > board.rows - 1 or col < 0 or col > board.cols - 1:
            return False
        elif not board[row][col][0].name == 'Entity':
            return False
        else:
            return True

    def move(self, position):
        if self.remainingStepsInRound <= 0: # this must always be checked first
            return 

        possibleMoves = ['N', 'E', 'S', 'W']
        hasMoved = False
        while len(possibleMoves) > 0 and not hasMoved:
            roll = rand.randint(0, len(possibleMoves) - 1)
            direction = possibleMoves[roll]
            if self.isClear(position, direction):
                self.moveToPosition(position, direction)
                hasMoved = True
            else:
                possibleMoves.remove(direction)

    def moveToPosition(self, position, direction):
        board, row, col = position
        newRow, newCol = self.getNewCoords(position, direction)
        board[row][col] = [Entity()]
        board[newRow][newCol] = [self]

    def attemptToEat(self, position):
        possibleMoves = ['N', 'E', 'S', 'W']
        hasEaten = False
        while len(possibleMoves) > 0 and not hasEaten:
            roll = rand.randint(0, len(possibleMoves) - 1)
            direction = possibleMoves[roll]
            if self.moveToEntity(position, direction, self.diet):
                self.restoreSatiation(10) # TODO restore amount based on food eaten
                hasEaten = True
            else:
                possibleMoves.remove(possibleMoves[roll])
        if not hasEaten:
            self.depleteSatiation(position)
        return hasEaten

    # checks if specified location contains an entity in the validEntities list
    def moveToEntity(self, position, direction, validEntities):
        board, startingRow, startingCol = position  
        row, col = self.getNewCoords(position, direction)
        if row < 0 or row > board.rows - 1 or col < 0 or col > board.cols - 1:
            return False
        for entity in validEntities:
            if isinstance(board[row][col][0], entity):
                board[startingRow][startingCol] = [Entity()]
                board[row][col] = [self]
                return True
            return False

    def attemptToBreed(self, position):
        hasBred = False
        if self.remainingStepsToBreed <= 0:     
            possibleSpaces = ['N', 'E', 'S', 'W']
            while len(possibleSpaces) > 0 and not hasBred:
                roll = rand.randint(0, len(possibleSpaces) - 1)
                direction = possibleSpaces[roll]
                if self.isClear(position, direction):
                    self.breed(position, direction)
                    self.resetStepsToBreed()
                    hasBred = True
                else:
                    possibleSpaces.remove(direction)
        if not hasBred:
            self.decrementStepsToBreed()
        return hasBred
    
    def breed(self, position, direction):
        board = position[0]
        newRow, newCol = self.getNewCoords(position, direction)
        board[newRow][newCol] = [self.__class__()]



class Herbivore(Animal):
    def __init__(self):
        super().__init__()
        self.name ='Herbivore'
        self.character = 'H'
        self.diet.append(Plant)
        self.hungerAmount = 1

    def move(self, position):
        if not self.attemptToEat(position):
            super().move(position)
        self.attemptToBreed(position)

class Carnivore(Animal):
    def __init__(self):
        super().__init__()
        self.name = 'Carnivore'
        self.character = 'C'
        self.diet.append(Herbivore)
        self.hungerAmount = 15

    def move(self, position):
        if not self.attemptToEat(position):
            super().move(position)
        self.attemptToBreed(position)

class Omnivore(Animal):
    def __init__(self):
        super().__init__()
        self.name = 'Omnivore'
        self.character = 'O'
        self.diet.extend((Plant, Animal))

class Plant(Entity):
    def __init__(self, size=4):
        self.name = 'Plant'
        self.characters = ['.', ':',';', '#']
        self.size = size
        self.setCharacter()

    def setCharacter(self):
        self.character = self.characters[self.size - 1]

class Scent(Entity):
    def __init__(self, intensity=3):
        self.name = 'Scent'
        self.intensity = intensity
        self.characters = ['~', 'S', '$']
        self.setCharacter()

    def setCharacter(self):
        self.character = self.characters[self.intensity - 1]