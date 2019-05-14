from constants import *

# TODO create stomach class that uses a queue for food contents

class Stomach:
    def __init__(self, body, capacityRatio):
        self.body = body
        self.contents = []
        self.capacityRatio = capacityRatio
        self.contentsMass = 0
        self.digestionRate = .1

    def capacity(self):
        

    def consume(self, organism):
        edibleMass = organism.mass * organism.edibleMassFraction
        remainingStomachCapacity = self.capacityRatio * self.body.mass - self.contentsMass
        organism.body.mass = min(edibleMass, remainingStomachCapacity)
        contents.put(organism)
        self.stomachContentsMass += min(edibleMass, remainingStomachCapacity)

    def digest(self):
        amountDigested = 0
        while amountDigested < digestionRate * self.body.mass and self.contentsMass > 0:
            contents[0] -= min(self.body.mass * )
            amountDigested += self.min()    
        amountDigested = min(self.mass * self.digestionRate, self.stomachContentsMass)
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
            startingMass = self.mass
            startingFatMass = self.mass * self.fatMassFraction
            startingMuscleMass = self.mass * self.muscleMassFraction
            massGained = netEnergy / (self.fatStorageFraction * BODY_FAT_ENERGY_CONTENT + self.muscleStorageFraction * BODY_MUSCLE_ENERGY_CONTENT)
            fatMassGained = massGained * self.fatStorageFraction 
            muscleMassGained = massGained * self.muscleStorageFraction 
            self.mass += massGained
            self.fatMassFraction = (startingFatMass + fatMassGained) / self.mass
            self.muscleMassFraction = (startingMuscleMass + muscleMassGained) / self.mass


class Body:
    def __init__(self, mass=10, massCapacity=100):
        self.mass = mass
        self.massCapacity = massCapacity
        self.edibleMassFraction = 1
        self.energyContent = 1000


class AnimalBody(Body):
    def __init__(self, mass=50, massCapacity=300):
        super().__init__(mass, massCapacity)
        self.fatMassFraction = .20
        self.muscleMassFraction = .35
        self.fatStorageFraction = self.fatMassFraction / (self.fatMassFraction + self.muscleMassFraction)
        self.muscleStorageFraction = 1 - self.fatStorageFraction
        self.edibleMassFraction = self.muscleMassFraction + self.fatMassFraction
        self.totalEnergyExpenditure = 0 # keeps track of the total amount of energy spent during current tick
        self.stomachContentsMass = 0
        self.stomachCapacityRatio = .35 # animal can only consume some percent of its body weight
        self.satiationThreshold = .8
        self.starvationThreshold = .05 # fatMassFraction dropping below this threshold causes death
        self.satiationAmount = 10
        self.stomach = Stomach(self, self.mass * self.stomachCapacityRatio)
        self.digestionRate = .1
        self.energyContent = 7000

    def hungry(self):
        return self.stomachContentsMass / (self.mass * self.stomachCapacityRatio) < self.satiationThreshold

    def eat(self, organism):
        self.stomach.consume(organism)

    def starved(self):
        return self.fatMassFraction < self.starvationThreshold

    def metabolize(self):
        amountDigested = min(self.mass * self.digestionRate, self.stomachContentsMass)
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
            startingMass = self.mass
            startingFatMass = self.mass * self.fatMassFraction
            startingMuscleMass = self.mass * self.muscleMassFraction
            massGained = netEnergy / (self.fatStorageFraction * BODY_FAT_ENERGY_CONTENT + self.muscleStorageFraction * BODY_MUSCLE_ENERGY_CONTENT)
            fatMassGained = massGained * self.fatStorageFraction 
            muscleMassGained = massGained * self.muscleStorageFraction 
            self.mass += massGained
            self.fatMassFraction = (startingFatMass + fatMassGained) / self.mass
            self.muscleMassFraction = (startingMuscleMass + muscleMassGained) / self.mass

    def canReproduce(self):
        return self.fatMassFraction >= .12

    # Resets the total energy expenditure to the baseline. This method should be called before 
    # any other energy expenditure calculations are done
    def baselineEnergyExpenditure(self):
        self.totalEnergyExpenditure = 5000 + 80 * self.mass

    # magnitude should be approximately 1 for moving a single space, 2-3 for chasing prey, etc
    def actionEnergyExpenditure(self, magnitude):
        self.totalEnergyExpenditure += 2000 + magnitude * self.mass * 150 


class PlantBody(Body):
    def __init__(self, mass=1, massCapacity=35):
        super().__init__(mass, massCapacity)
        self.growthRate = .2

    def grow(self):
        # mass added increases as plant grows, until massCapacity is reached
        if self.mass < self.massCapacity:
            self.mass += min(self.massCapacity, self.mass * self.growthRate)