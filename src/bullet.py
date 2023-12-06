import Box2D
from pygame import time

from b2Helper import B2Helper
from b2PyHelper import B2PyHelper


class Bullet:  # TODO BULLETS UP FOR DELETION SHOULD STILL BE ABLE TO DAMAGE ENEMIES
    def __init__(self, position: tuple, velocity: Box2D.b2Vec2, density: int, world: Box2D.b2World,
                 b2_py_helper: B2PyHelper, b2_helper: B2Helper):
        self.b2_helper = b2_helper
        self.b2_py_helper = b2_py_helper
        self.pos = position
        self.velocity = velocity
        self.world = world
        self.body = self.world.CreateDynamicBody(position=position, bullet=True,
                                                 shapes=(self.b2_helper.create_polygon(0, 0, 3, 3)),
                                                 linearVelocity=velocity)
        self.body.userData = {'bullet': True}
        self.body.density = density
        self.creation_time = time.get_ticks()
        self.impact_time = 0
        self.body.mass = 30
