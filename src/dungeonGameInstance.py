import Box2D
import pygame

import dungeon
from b2Helper import B2Helper
from b2PyHelper import B2PyHelper
from player import Player


class DungeonGameInstance:
    def __init__(self):
        self.PPM = 20
        self.FPS = 60
        self.TIME_STEP = 1.0 / self.FPS
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 800
        self.INPUT_SENSITIVITY = 10
        self.BULLET_LIFETIME = 3000
        self.BULLET_LIFETIME_AFTER_COLL = 500
        self.NON_COLLIDING_CATEGORY = 0
        self.NON_COLLIDING_MASK = 0
        self.bulletsUpForDeletion = []
        self.enemiesUpForDeletion = []
        self.gameActive = True

        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.world = Box2D.b2World([0, 0], doSleep=True)
        self.clock = pygame.time.Clock()
        self.cameraOffset = [0, 0]
        self.b2PyHelper = B2PyHelper(self.PPM, self.cameraOffset, self.INPUT_SENSITIVITY, self.WINDOW_HEIGHT)
        self.b2Helper = B2Helper(self.world, self.PPM)
        self.dungeon = dungeon.Dungeon(self.WINDOW_HEIGHT / 2, self.WINDOW_WIDTH / 2, self.world, 50, 50, self.b2Helper,
                                       self.b2PyHelper)

        self.bullets = []
        self.player = Player(tuple((self.WINDOW_HEIGHT / 2, self.WINDOW_HEIGHT / 2)), self.b2PyHelper, self.b2Helper,
                             self.cameraOffset, self.world, self.INPUT_SENSITIVITY, self.bullets)
