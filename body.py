from constants import *

class Body:
    def __init__(self, mass=10, massCapacity=100):
        self.mass = mass
        self.massCapacity = massCapacity
        self.edibleMassFraction = 1

class AnimalBody(Body):
    def __init__(self, mass=10, massCapacity=100):
        super().__init__(mass, massCapacity)
        self.fatMassFraction = .20
        self.muscleMassFraction = .35
        self.fatStorageFraction = self.fatMassFraction / (self.fatMassFraction + self.muscleMassFraction)
        self.muscleStorageFraction = 1 - self.fatStorageFraction
        self.edibleMassFraction = self.muscleMassFraction + self.fatMassFraction
        self.totalEnergyExpenditure = 0 # keeps track of the total amount of energy spent during current tick
        self.stomachContentsMass = 0
        self.stomachCapacity = self.mass * .1 # animal can only consume some percent of its body weight
        self.satiationThreshold = .8
        self.starvationThreshold = .05 # fatMassFraction dropping below this threshold causes death
        self.satiationAmount = 10
        self.digestionRate = .1

    def hungry(self):
        return (self.stomachContentsMass / self.stomachCapacity) < self.satiationThreshold

    def eat(self, organism):
        edibleMass = self.mass * self.edibleMassFraction
        remainingStomachCapacity = self.stomachCapacity - self.stomachContentsMass
        self.stomachContentsMass += min(edibleMass, remainingStomachCapacity)

    def starved(self):
        return self.fatMassFraction < self.starvationThreshold

    def metabolize(self):
        amountDigested = min(self.stomachContentsMass * self.digestionRate, self.stomachCapacity * self.digestionRate)
        self.stomachContentsMass -= amountDigested
        energyGained = 7000 * amountDigested # assuming energy content of 7000 KJ/kg for food consumed
        netEnergy = energyGained - self.totalEnergyExpenditure
        
        # energy is burned from or stored purely as fat if energy is lost or if fully grown
        if netEnergy < 0 or self.mass >= self.massCapacity: 
            massGained = netEnergy / BODY_FAT_ENERGY_CONTENT
            startingFatMass = self.mass * self.fatMassFraction
            self.mass += massGained
            self.fatMassFraction = (startingFatMass + massGained) / self.mass
        else: 
            self.mass += (netEnergy / (self.fatStorageFraction * BODY_FAT_ENERGY_CONTENT +
                         self.muscleStorageFraction * BODY_MUSCLE_ENERGY_CONTENT))
        
    def canReproduce(self):
        return self.fatMassFraction >= .12

    # Resets the total energy expenditure to the baseline. This method should be called before 
    # any other energy expenditure calculations are done
    def baselineEnergyExpenditure(self):
        self.totalEnergyExpenditure = 4000 + 45 * self.mass

    # magnitude should be approximately 1 for moving a single space, 2-3 for chasing prey, etc
    def actionEnergyExpenditure(self, magnitude):
        self.totalEnergyExpenditure += 2000 + magnitude * self.mass * 25 