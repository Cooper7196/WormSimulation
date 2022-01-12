import pygame
import math


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
        for node in self.body:
            node.draw()

class WormNode:
    def __init__(self, screen, x, y, radius, leader=None):
        self.x, self.y = x, y
        self.oldX, self.oldY = x, y
        self.radius = radius
        self.screen = screen
        self.leader = leader

    def draw(self):
        """ Draw the worm """
        pygame.draw.circle(self.screen, (255, 255, 255), [self.x, self.y], self.radius, 0)


# Window dimensions.
width = 800
height = 800
pygame.init()
screen = pygame.display.set_mode((width, height))
worm = Worm(screen, 35, width / 2, height / 2, 5)
clock = pygame.time.Clock()
running = True

speed = 3
rotation = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        rotation -= 3
    elif keys[pygame.K_d]:
        rotation += 3

    worm.x += math.sin(math.radians(rotation)) * speed
    worm.y -= math.cos(math.radians(rotation)) * speed

    screen.fill((0, 0, 0))
    worm.update()
    worm.draw()
    pygame.display.update()
    clock.tick(60)
