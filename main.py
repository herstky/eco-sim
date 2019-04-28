import simulation as sim
import entities 
from time import sleep

board = sim.Board()
iterations = 100
wait = .5
for i in range(iterations):
    board.printBoard()
    board.tick()
    sleep(wait)
