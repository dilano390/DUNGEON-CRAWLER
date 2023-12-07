import random

import Box2D

from b2Helper import B2Helper
from b2PyHelper import B2PyHelper


class Enemy:  # TODO ADD BOSSES
    def __init__(self, cage_pos: tuple, cage_dim: tuple, lives: int, speed: int, b2_py_helper: B2PyHelper,
                 b2_helper: B2Helper, world: Box2D.b2World, w = 20, h = 20, big : bool = False):
        self.lives = lives
        self.speed = speed
        self.cage_pos = cage_pos
        self.cage_dim = cage_dim
        self.b2_py_helper = b2_py_helper
        self.b2_helper = b2_helper
        self.world = world
        self.direction = (0, 0)
        self.w = w
        self.h = h
        self.x = self.constrain(self.get_random_number(0, cage_dim[0]), 0 + self.w + 5, self.cage_dim[0] - self.w - 5) + \
                 cage_pos[0]
        self.y = self.constrain(self.get_random_number(0, cage_dim[1]), 0 + self.h + 5, self.cage_dim[1] - self.h - 5) + \
                 cage_pos[1]
        self.pos = tuple((self.x, self.y))
        self.b2_object = self.world.CreateDynamicBody(
            position=(self.b2_py_helper.convert_cords_to_b2_vec2(self.x, self.y)),
            shapes=(self.b2_helper.create_polygon(0, 0, self.w, self.h)))
        self.b2_object.mass = self.get_random_number(10, 40)
        self.b2_object.linearDamping = 5
        self.b2_object.fixtures[0].friction = 3
        self.b2_object.userData = {'enemy': self,'big' : big,'color': tuple((255, 100, 0))}

    def take_damage(self, damage):
        color = self.b2_object.userData['color']
        red = color[0] - 155 / self.lives * damage
        red = self.constrain(red, 155, 255)
        self.b2_object.userData['color'] = tuple((red, color[1], color[2]))
        self.lives -= damage
        if self.lives <= 0:
            self.world.DestroyBody(self.b2_object)

    def update(self, target):
        # Get positions of both bodies
        enemy_pos = self.b2_object.position
        target_pos = target.position

        direction = target_pos - enemy_pos  # This gives a vector pointing from A to B
        # Normalize the direction vector
        direction.Normalize()

        # Define a speed or velocity at which bodyA will move
        speed = self.speed  # Adjust as needed

        # Calculate the desired velocity vector by multiplying the direction by speed
        desired_velocity = direction * speed

        # Calculate the impulse needed to achieve the desired velocity (assuming bodyA has a mass)
        current_velocity = self.b2_object.linearVelocity
        impulse = self.b2_object.mass * (desired_velocity - current_velocity)

        # Apply the impulse to move bodyA towards bodyB
        self.b2_object.ApplyLinearImpulse(impulse, enemy_pos, True)
        # self.b2Object.ApplyForce(impulse, enemy_pos, True)

    @staticmethod
    def constrain(val, min_val, max_val):
        return min(max_val, max(min_val, val))

    @staticmethod
    def get_random_number(lower, upper):
        return random.randrange(lower, upper)
