from ecosim.simulation import *

app = QApplication(sys.argv)
window = Window()
with open('misc/results.txt', 'w') as outputFile:
    outputFile.write('Simulation Results:\n')
simulation = Simulation(window, .25)    
window.show()
sys.exit(app.exec_())
