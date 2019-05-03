import entities 
import random as rand
from time import sleep

class Board:
    def __init__(self, rows=20, cols=30):
        self.rows = rows
        self.cols = cols
        self.entities = []
        self.board = [[[entities.EmptySpace(self)] for col in range(self.cols)] for row in range(self.rows)]
        self.populateBoard()

    def __getitem__(self, row):
        return self.board[row]

    # adds entity to entities list and inserts it at the front of the list at the given coords
    def addEntity(self, entity, coords):
        entity.row, entity.col = coords
        self.entities.append(entity)
        self.board[entity.row][entity.col].insert(0, entity)
        pass # TODO delete
 
    # removes entity from board, but leaves it in the entities list
    def removeEntityFromBoard(self, entity):
        row = entity.row
        col = entity.col
        entity.row = None
        entity.col = None
        self.board[row][col].remove(entity)
        if len(self.board[row][col]) == 0:
            self.board[row][col].insert(entities.EmptySpace(self))

    # completely destroys entity
    def deleteEntity(self, entity):
        self.entities.remove(entity)
        self.removeEntityFromBoard(entity)

    # returns entity at the front of the list at the given coords
    def getEntity(self, coords):
        row, col = coords
        return self.board[row][col][0]

    # insert entity at the front of the list at the given coords
    # also removes entity from previous location
    def moveEntity(self, entity, coords):
        row, col = coords
        if entity.row is not None and entity.col is not None:
            self.removeEntityFromBoard(entity)
        entity.row = row
        entity.col = col
        self.addEntity(entity, coords)

    def simulateEntities(self):
        for entity in self.entities:
            entity.simulate()

    def updateEntities(self):
        # for entity in self.entities:
            # entity.update()
        self.entities.sort(key=lambda x: x.speed, reverse=True) # faster entities go first

    def populateBoard(self):
        herbivoreChance = 30
        carnivoreChance = 5
        plantChance = 10
        for row in range(self.rows):
            for col in range(self.cols):
                roll = rand.randint(1, 100)
                if roll <= herbivoreChance:
                    self.addEntity(entities.Herbivore(self), (row, col))
                # elif roll <= herbivoreChance + carnivoreChance:
                #     self.addEntity(entities.Carnivore(self), (row, col))
                # elif roll <= herbivoreChance + carnivoreChance + plantChance:
                #     self.addEntity(entities.Plant(self, rand.randint(2, 4)), (row, col))

    def tick(self):
        self.simulateEntities()
        self.updateEntities()

    # prints the first entity in every cell
    # it would appear the MS interpreter can't print all this. TODO delete
    def printBoard(self):
        for col in range(self.cols + 2):
            print('-', end='')
        for row in range(self.rows):
            print('')
            for col in range(self.cols):
                if col == 0:
                    print('|{}'.format(self.getEntity((row, col)).character), end='')
                elif col == self.cols - 1:
                    print('{}|'.format(self.getEntity((row, col)).character), end='')
                else:
                    print(self.getEntity((row, col)).character, end='')
        print('')
        for col in range(self.cols + 2):
            print('-', end='')    
        print('')

class Simulation:
    def __init__(self, board, iterations=10, wait=0.25):
        self.board = board
        self.iterations = iterations
        self.wait = wait

    def run(self):
        for _ in range(self.iterations):
            board.printBoard()
            board.tick()
            sleep(self.wait)

if __name__ == '__main__':
    board = Board()
    sim = Simulation(board)
    sim.run()
