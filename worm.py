import csv
from pprint import pprint
# import pygame

THRESHOLD = 15


class WormBrain:
    def __init__(self, filePath, threshold):
        self.currentState = 0
        self.nextState = 1
        self.connectome, self.neurons = self.loadConnectomeWeights(
            filePath)
        self.neurons = {neuron: [0, 0] for neuron in list(self.neurons)}
        self.threshold = threshold

        self.isHungry = False
        self.isTouched = False
        self.isSensingFood = False
        self.threshold = threshold

        self.leftSpeed = 0
        self.rightSpeed = 0

        self.musclePrefixes = ['MVU', 'MVL', 'MDL', 'MVR', 'MDR']
        self.leftMuscles = [
            'MDL07',
            'MDL08',
            'MDL09',
            'MDL10',
            'MDL11',
            'MDL12',
            'MDL13',
            'MDL14',
            'MDL15',
            'MDL16',
            'MDL17',
            'MDL18',
            'MDL19',
            'MDL20',
            'MDL21',
            'MDL22',
            'MDL23',
            'MVL07',
            'MVL08',
            'MVL09',
            'MVL10',
            'MVL11',
            'MVL12',
            'MVL13',
            'MVL14',
            'MVL15',
            'MVL16',
            'MVL17',
            'MVL18',
            'MVL19',
            'MVL20',
            'MVL21',
            'MVL22',
            'MVL23'
        ]
        self.rightMuscles = [
            'MDR07',
            'MDR08',
            'MDR09',
            'MDR10',
            'MDR11',
            'MDR12',
            'MDR13',
            'MDR14',
            'MDR15',
            'MDR16',
            'MDR17',
            'MDR18',
            'MDR19',
            'MDR20',
            'MDL21',
            'MDR22',
            'MDR23',
            'MVR07',
            'MVR08',
            'MVR09',
            'MVR10',
            'MVR11',
            'MVR12',
            'MVR13',
            'MVR14',
            'MVR15',
            'MVR16',
            'MVR17',
            'MVR18',
            'MVR19',
            'MVR20',
            'MVL21',
            'MVR22',
            'MVR23'
        ]

    def loadConnectomeWeights(self, filePath):
        connectomeWeights = {}
        neurons = set()

        with open(filePath, 'r') as file:
            reader = csv.reader(file)
            for connection in list(reader)[1:]:
                neurons.add(connection[0])
                neurons.add(connection[1])
                if not connectomeWeights.get(connection[0]):
                    connectomeWeights[connection[0]] = {}
                connectomeWeights[connection[0]
                                  ][connection[1]] = int(connection[2])
        return (connectomeWeights, neurons)

    def fireNeuron(self, neuron):
        for i in self.connectome[neuron]:
            self.neurons[i][self.nextState] += self.connectome[neuron][i]

    def simulateConnectome(self):
        for neuron in self.connectome:
            if neuron[:3] not in self.musclePrefixes:
                if self.neurons[neuron][self.currentState] >= self.threshold:
                    self.neurons[neuron][self.nextState] = 0
                    self.fireNeuron(neuron)

        self.calculateMotion()

        for neuron in self.neurons:
            self.neurons[neuron][self.currentState] = self.neurons[neuron][self.nextState]

        self.currentState, self.nextState = self.nextState, self.currentState

    def calculateMotion(self):
        for leftMuscle in self.leftMuscles:
            self.leftSpeed += self.neurons[leftMuscle][self.nextState]
            self.neurons[leftMuscle][self.nextState] = 0

        for rightMuscle in self.rightMuscles:
            self.rightSpeed += self.neurons[rightMuscle][self.nextState]
            self.neurons[rightMuscle][self.nextState] = 0

    def runBrain(self):
        if self.isHungry:
            self.fireNeuron("RIML")
            self.fireNeuron("RIMR")
            self.fireNeuron("RICL")
            self.fireNeuron("RICR")
            self.simulateConnectome()

        if self.isTouched:
            self.fireNeuron("FLPR")
            self.fireNeuron("FLPL")
            self.fireNeuron("ASHL")
            self.fireNeuron("ASHR")
            self.fireNeuron("IL1VL")
            self.fireNeuron("IL1VR")
            self.fireNeuron("OLQDL")
            self.fireNeuron("OLQDR")
            self.fireNeuron("OLQVR")
            self.fireNeuron("OLQVL")
            self.simulateConnectome()

        if self.isSensingFood:
            self.fireNeuron("ADFL")
            self.fireNeuron("ADFR")
            self.fireNeuron("ASGR")
            self.fireNeuron("ASGL")
            self.fireNeuron("ASIL")
            self.fireNeuron("ASIR")
            self.fireNeuron("ASJR")
            self.fireNeuron("ASJL")
            self.simulateConnectome()


brain = WormBrain('CElegansConnectome.csv', THRESHOLD)

brain.neurons["ADAL"][0] = 15
pprint(brain.neurons)
brain.simulateConnectome()
pprint(brain.neurons)
