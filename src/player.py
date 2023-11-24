import math
from typing import Tuple, List

import Box2D
import pygame

from b2Helper import B2Helper
from b2PyHelper import B2PyHelper
from bullet import Bullet


class Player:
    def __init__(self, position: tuple, b2PyHelper: B2PyHelper, b2Helper: B2Helper, cameraOffset: Tuple[float, float],
                 world: Box2D.b2World, sensitivity: int, bullets: List[Bullet]):
        self.b2Helper = b2Helper
        self.b2PyHelper = b2PyHelper
        self.cameraOffset = cameraOffset
        self.world = world
        self.b2Object = self.world.CreateDynamicBody(
            position=(self.b2PyHelper.convertTupleToB2Vec2(position)),
            shapes=(self.b2Helper.createPolygon(0, 0, 10, 10)))
        self.b2Object.userData = {'player': True}
        self.sensitivity = sensitivity
        self.bullets = bullets

    def determineVelocity(self) -> None:
        velY = 0
        velX = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            velY += self.sensitivity
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            velY -= self.sensitivity
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            velX += self.sensitivity
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            velX -= self.sensitivity
        self.b2Object.linearVelocity = Box2D.b2Vec2(velX, velY)

    def shoot(self) -> None:
        mousePos = self.b2PyHelper.flipYaxis(pygame.mouse.get_pos())
        playerPos = self.b2PyHelper.convertB2Vec2toTuple(self.b2Object.position)

        mousePos = tuple((mousePos[0] - self.cameraOffset[0], mousePos[1] + self.cameraOffset[1]))
        distance = [mousePos[0] - playerPos[0], mousePos[1] - playerPos[1]]
        norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
        direction = [distance[0] / norm, distance[1] / norm]
        offset = 8
        playerPos = tuple((playerPos[0] + direction[0] * offset, playerPos[1] + direction[1] * offset))
        speed = 600
        bullet_vector = [direction[0] * math.sqrt(2) * speed, direction[1] * math.sqrt(2) * speed]
        self.bullets.append(
            Bullet(self.b2PyHelper.convertTupleToB2Vec2(playerPos), self.b2PyHelper.convertTupleToB2Vec2(bullet_vector),
                   100, self.world, self.b2PyHelper, self.b2Helper))

        # bullet.userData = {'shatter_after_impact': True, 'impacted': False, 'impactTime': 0}
