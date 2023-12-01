import random
import Box2D

from b2Helper import B2Helper
from b2PyHelper import B2PyHelper

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
        self.direction = (0, 0)
        self.w = 20
        self.h = 20
        self.x = self.constrain(self.getRandomNumber(0,cageDim[0]), 0 + self.w + 5, self.cageDim[0] - self.w - 5) + \
                 cagePos[0]
        self.y = self.constrain(self.getRandomNumber(0,cageDim[1]), 0 + self.h + 5, self.cageDim[1] - self.h - 5) + \
                 cagePos[1]
        self.pos = tuple((self.x, self.y))
        self.b2Object = self.world.CreateDynamicBody(
            position=(self.b2PyHelper.convertCordsToB2Vec2(self.x, self.y)),
            shapes=(self.b2Helper.createPolygon(0, 0, self.w, self.h)))
        self.b2Object.mass = self.getRandomNumber(10,40)
        self.b2Object.linearDamping = 5
        self.b2Object.fixtures[0].friction = 3
        self.b2Object.userData = {'enemy': self, 'color': tuple((255, 100, 0))}

    def takeDamage(self, damage):
        color = self.b2Object.userData['color']
        red = color[0] - 155 / self.lives * damage
        red = self.constrain(red, 155, 255)
        self.b2Object.userData['color'] = tuple((red, color[1], color[2]))
        self.lives -= damage
        if self.lives <= 0:
            self.world.DestroyBody(self.b2Object)

    def update(self, target):
        # Get positions of both bodies
        enemyPos = self.b2Object.position
        targetPos = target.position

        direction = targetPos - enemyPos  # This gives a vector pointing from A to B
        # Normalize the direction vector
        direction.Normalize()

        # Define a speed or velocity at which bodyA will move
        speed = self.speed  # Adjust as needed

        # Calculate the desired velocity vector by multiplying the direction by speed
        desired_velocity = direction * speed

        # Calculate the impulse needed to achieve the desired velocity (assuming bodyA has a mass)
        current_velocity = self.b2Object.linearVelocity
        impulse = self.b2Object.mass * (desired_velocity - current_velocity)

        # Apply the impulse to move bodyA towards bodyB
        self.b2Object.ApplyLinearImpulse(impulse, enemyPos, True)
        # self.b2Object.ApplyForce(impulse, enemyPos, True)

    @staticmethod
    def constrain(val, min_val, max_val):
        return min(max_val, max(min_val, val))

    @staticmethod
    def getRandomNumber(lower,upper):
        return random.randrange(lower, upper)
