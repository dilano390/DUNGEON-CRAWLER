import Box2D
from pygame import time

from b2Helper import B2Helper
from b2PyHelper import B2PyHelper


class Bullet:  # TODO BULLETS UP FOR DELETION SHOULD STILL BE ABLE TO DAMAGE ENEMIES
    def __init__(self, position: tuple, velocity: Box2D.b2Vec2, density: int, world: Box2D.b2World,
                 b2PyHelper: B2PyHelper, b2Helper: B2Helper):
        self.b2Helper = b2Helper
        self.b2PyHelper = b2PyHelper
        self.pos = position
        self.velocity = velocity
        self.world = world
        self.body = self.world.CreateDynamicBody(position=position, bullet=True,
                                                 shapes=(self.b2Helper.createPolygon(0, 0, 3, 3)),
                                                 linearVelocity=velocity)
        self.body.userData = {'bullet': True}
        self.body.density = density
        self.creationTime = time.get_ticks()
        self.impactTime = 0
        self.body.mass = 30
