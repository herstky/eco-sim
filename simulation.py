import entities 
import random as rand

class Board:
    def __init__(self, rows=15, cols=50):
        self.rows = rows
        self.cols = cols
        self.board = [[[entities.Entity()]] * cols for row in range(rows)] 
        self.populateBoard()

    def __getitem__(self, row):
        return self.board[row]

    def populateBoard(self):
        herbivoreChance = 5
        carnivoreChance = 5
        plantChance = 10
        for row in range(self.rows):
            for col in range(self.cols):
                roll = rand.randint(1, 100)
                if roll <= herbivoreChance:
                    self.board[row][col] = [entities.Herbivore()]
                elif roll <= herbivoreChance + carnivoreChance:
                    self.board[row][col] = [entities.Carnivore()]
                elif roll <= herbivoreChance + carnivoreChance + plantChance:
                    self.board[row][col] = [entities.Plant(rand.randint(2, 4))]

    def tick(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if isinstance(self.board[row][col], entities.Animal):
                    animal = self.board[row][col]
                    animal.move((self, row, col))
                    animal.decrementStepsInRound()
        for row in range(self.rows):
            for col in range(self.cols):
                if isinstance(self.board[row][col], entities.Animal):
                    self.board[row][col].resetStepsInRound()

    def printBoard(self):
        for col in range(self.cols + 2):
            print('-', end='')
        for row in range(self.rows):
            print('')
            for col in range(self.cols):
                if col == 0:
                    print('|{}'.format(self.board[row][col].character), end='')
                elif col == self.cols - 1:
                    print('{}|'.format(self.board[row][col].character), end='')
                else:
                    print(self.board[row][col].character, end='')
        print('')
        for col in range(self.cols + 2):
            print('-', end='')    
        print('')

                    
