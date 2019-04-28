import simulation as sim
import entities 
from time import sleep

board = sim.Board()
iterations = 200
wait = .25
for i in range(iterations):
    board.printBoard()
    board.tick()
    sleep(wait)
