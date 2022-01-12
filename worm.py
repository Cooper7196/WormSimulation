import csv
import math
import time
import random
import pygame

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

        self.rotation = 0
        self.speed = 0

        self.x = 400
        self.y = 400

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

    def setNeuronToMax(self, neuron):
        self.neurons[neuron][self.currentState] = self.threshold

    def simulateConnectome(self):
        for neuron in self.connectome:
            if neuron[:3] not in self.musclePrefixes:
                if self.neurons[neuron][self.currentState] >= self.threshold:
                    self.neurons[neuron][self.nextState] = 0
                    self.fireNeuron(neuron)
        self.neurons["MVULVA"] = [0, 0]
        self.calculateMotion()

        for neuron in self.neurons:
            self.neurons[neuron][self.currentState] = self.neurons[neuron][self.nextState]

        self.currentState, self.nextState = self.nextState, self.currentState

    def calculateMotion(self):
        self.leftSpeed = 0
        self.rightSpeed = 0

        for leftMuscle in self.leftMuscles:
            self.leftSpeed += self.neurons[leftMuscle][self.nextState]
            # self.neurons[leftMuscle][self.nextState] *= 0.7

            self.neurons[leftMuscle][self.nextState] = 0
            self.neurons[leftMuscle][self.currentState] = 0

        for rightMuscle in self.rightMuscles:
            self.rightSpeed += self.neurons[rightMuscle][self.nextState]
            # self.neurons[rightMuscle][self.nextState] *= 0.7
            
            self.neurons[rightMuscle][self.nextState] = 0
            self.neurons[rightMuscle][self.currentState] = 0

        # self.rotation = self.rotation + (self.rightSpeed - self.leftSpeed)

        # self.rotation += self.rightSpeed - self.leftSpeed
        # print(self.rotation)
        if self.rightSpeed > self.leftSpeed:
            self.rotation += 5
        if self.leftSpeed > self.rightSpeed:
            self.rotation -= 5

        self.speed = (abs(self.leftSpeed) + abs(self.rightSpeed))

        self.speed = self.speed / 100


        self.x += (math.cos(math.radians(self.rotation)) * self.speed)
        self.y += (math.sin(math.radians(self.rotation)) * self.speed)
        
        # print(self.rightSpeed, self.leftSpeed, self.rotation, self.speed)
    def simulateTouch(self):
        self.setNeuronToMax("FLPR")
        self.setNeuronToMax("FLPL")
        self.setNeuronToMax("ASHL")
        self.setNeuronToMax("ASHR")
        self.setNeuronToMax("IL1VL")
        self.setNeuronToMax("IL1VR")
        self.setNeuronToMax("OLQDL")
        self.setNeuronToMax("OLQDR")
        self.setNeuronToMax("OLQVR")
        self.setNeuronToMax("OLQVL")

    def simulateFood(self):
        self.setNeuronToMax("ADFL")
        self.setNeuronToMax("ADFR")
        self.setNeuronToMax("ASGR")
        self.setNeuronToMax("ASGL")
        self.setNeuronToMax("ASIL")
        self.setNeuronToMax("ASIR")
        self.setNeuronToMax("ASJR")
        self.setNeuronToMax("ASJL")
        self.setNeuronToMax("AWCL")
        self.setNeuronToMax("AWCR")
        self.setNeuronToMax("AWAL")
        self.setNeuronToMax("AWAR")

    def runBrain(self):
        # if self.isHungry:
        #     self.setNeuronToMax("RIML")
        #     self.setNeuronToMax("RIMR")
        #     self.setNeuronToMax("RICL")
        #     self.setNeuronToMax("RICR")
        #     self.simulateConnectome()
        self.simulateConnectome()


class Worm:
    def __init__(self, screen, length, x, y, radius):
        self.screen = screen
        self.x = x
        self.y = y

        self.head = WormNode(screen, x, y, radius)
        self.body = [self.head]

        for i in range(length):
            tmpWorm = WormNode(
                screen, self.x, self.y, radius, leader=len(
                    self.body) - 1)
            tmpWorm.oldX = tmpWorm.x
            tmpWorm.oldY = tmpWorm.y

            self.body.append(tmpWorm)

    def update(self):

        self.head.oldX = self.x
        self.head.oldY = self.y

        self.head.x = self.x
        self.head.y = self.y

        for node in self.body[1:]:
            node.oldX = node.x
            node.oldY = node.y

            node.x = self.body[node.leader].oldX
            node.y = self.body[node.leader].oldY

    def draw(self):
        for node in self.body[1:]:
            node.draw()
        pygame.draw.circle(
            self.body[0].screen, (255, 0, 0), [
                self.body[0].x, self.body[0].y], self.body[0].radius)

class WormNode:
    def __init__(self, screen, x, y, radius, leader=None):
        self.x, self.y = x, y
        self.oldX, self.oldY = x, y
        self.radius = radius
        self.screen = screen
        self.leader = leader

    def draw(self):
        """ Draw the worm """
        pygame.draw.circle(
            self.screen, (255, 255, 255), [
                self.x, self.y], self.radius)
        


brain = WormBrain('CElegansConnectome.csv', THRESHOLD)

width = 1366
height = 768
pygame.init()
screen = pygame.display.set_mode((width, height))
worm = Worm(screen, 50, 0, 0, 7)
clock = pygame.time.Clock()
running = True

speed = 3
rotation = 0
# brain.isHungry = True
test = time.time()
# brain.simulateFood()
for i in range(40):
    
    # neuron = random.choice(list(brain.neurons.keys()))
    # brain.setNeuronToMax(neuron)
    # brain.runBrain()
    pass
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_f]:
        print("test")
        brain.simulateFood()

    brain.runBrain()

    
    if brain.x <= 0: 
        brain.x = 0
        brain.simulateTouch()
        print("touch")
    if brain.x >= width:
        brain.x = width
        brain.simulateTouch()
        print("touch")
    if brain.y <= 0:
        brain.y = 0
        brain.simulateTouch()
        print("touch")
    if brain.y >= height:
        brain.y = height
        brain.simulateTouch()
        print("touch")


    screen.fill((155, 118, 83))

    worm.x = brain.x
    worm.y = brain.y
    worm.update()
    worm.draw()

    pygame.display.update()
    clock.tick(60)
