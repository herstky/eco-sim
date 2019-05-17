class Particle(): 
    '''
    Particles start at an altitude above ground level and float to adjacent cells until they hit the
    ground. Particles behave independently of other entities and can therefore be simulated in parallel. 
    '''
    def __init__(self, board, sourceClass, coords, count=1000, diffusionRate=.1, degradationRate=.1):
        self.board = board
        self.name = 'Particle'
        self.sourceClass = sourceClass
        self.coords = coords
        self.count = count
        self.diffusionRate = diffusionRate # the fraction of count that will diffuse to adjacent cells
        self.degradationRate = degradationRate

    def addToBoard(self, coords):
        row, col = coords
        self.board[row][col].generateParticles(self, coords, self.count)

    def degrade(self):
        row, col = self.coords
        self.board[row][col].destroyParticles(self, self.coords, 5 + round(self.degradationRate * self.count))

    def diffuse(self):
        if self.count <= 0:
            return
        directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        diffusingParticles = round(self.count * self.diffusionRate)
        for direction in directions:
            if not self.validCell(direction):
                break
            outgoingParticles = diffusingParticles // len(directions)
            adjCoords = self.getCoordsAtDirection(direction)
            adjRow, adjCol = adjCoords
            self.board[adjRow][adjCol].transferParticles(self, self.coords, adjCoords, outgoingParticles)

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

    def simulate(self):
        self.degrade()
        self.diffuse()
    