import random

import Box2D

from b2Helper import B2Helper
from b2PyHelper import B2PyHelper
from dungeonGameInstance import DungeonGameInstance


class Enemy:
    def __init__(self, cagePos: tuple, cageDim: tuple, lives: int, speed: int, b2PyHelper: B2PyHelper,
                 b2Helper: B2Helper, world: Box2D.b2World):
        self.lives = lives
        self.speed = speed
        self.cagePos = cagePos
        self.cageDim = cageDim
        self.b2PyHelper = b2PyHelper
        self.b2Helper = b2Helper
        self.world = world

        self.w = 20
        self.h = 20
        self.x = self.constrain(self.getRandomNumber(cageDim[0]), 0 + self.w + 5, self.cageDim[0] - self.w - 5) + \
                 cagePos[0]
        self.y = self.constrain(self.getRandomNumber(cageDim[1]), 0 + self.h + 5, self.cageDim[1] - self.h - 5) + \
                 cagePos[1]

        self.b2Object = self.b2Object = self.world.CreateDynamicBody(
            position=(self.b2PyHelper.convertCordsToB2Vec2(self.x, self.y)),
            shapes=(self.b2Helper.createPolygon(0, 0, self.w, self.h)))
        self.b2Object.mass = 200
        self.b2Object.linearDamping = 5
        self.b2Object.fixtures[0].friction = 3
        self.b2Object.userData = {'enemy': self, 'color': tuple((255, 100, 0))}

    def takeDamage(self, damage, gameInstance: DungeonGameInstance):
        color = self.b2Object.userData['color']
        red = color[0] - 155 / self.lives * damage
        red = self.constrain(red, 155, 255)
        self.b2Object.userData['color'] = tuple((red, color[1], color[2]))
        self.lives -= damage
        print(self.lives)
        if self.lives <= 0:
            gameInstance.enemiesUpForDeletion.append(self)

    @staticmethod
    def constrain(val, min_val, max_val):
        return min(max_val, max(min_val, val))

    @staticmethod
    def getRandomNumber(upper):
        return random.randrange(0, upper)
