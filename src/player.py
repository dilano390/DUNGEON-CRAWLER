import math
from typing import Tuple, List

import Box2D
import pygame

from b2Helper import B2Helper
from b2PyHelper import B2PyHelper
from bullet import Bullet


class Player:
    def __init__(self, position: tuple, b2_py_helper: B2PyHelper, b2_helper: B2Helper,
                 camera_offset: Tuple[float, float],
                 world: Box2D.b2World, sensitivity: int, bullets: List[Bullet]):
        self.b2_helper = b2_helper
        self.b2_py_helper = b2_py_helper
        self.camera_offset = camera_offset
        self.world = world
        self.b2_object = self.world.CreateDynamicBody(
            position=(self.b2_py_helper.convert_tuple_to_b2_vec2(position)),
            shapes=(self.b2_helper.create_polygon(0, 0, 10, 10)))
        self.b2_object.userData = {'player': True}
        self.sensitivity = sensitivity
        self.bullets = bullets
        self.lives = 5
        self.last_damage_time = 0

    def determine_velocity(self) -> None:
        vel_y = 0
        vel_x = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            vel_y += self.sensitivity
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            vel_y -= self.sensitivity
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            vel_x += self.sensitivity
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            vel_x -= self.sensitivity
        self.b2_object.linearVelocity = Box2D.b2Vec2(vel_x, vel_y)

    def player_take_damage(self, game_instance):
        if pygame.time.get_ticks() - self.last_damage_time > 1000:
            self.lives -= 1
            self.last_damage_time = pygame.time.get_ticks()
            if self.lives <= 0:
                game_instance.main_game_loop = False
                game_instance.game_over = True

    def shoot(self) -> None:
        mouse_pos = self.b2_py_helper.flip_y_axis(pygame.mouse.get_pos())
        player_pos = self.b2_py_helper.convert_b2_vec2_to_tuple(self.b2_object.position)

        mouse_pos = tuple((mouse_pos[0] - self.camera_offset[0], mouse_pos[1] + self.camera_offset[1]))
        distance = [mouse_pos[0] - player_pos[0], mouse_pos[1] - player_pos[1]]
        norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
        if norm == 0: norm += 0.2
        direction = [distance[0] / norm, distance[1] / norm]
        offset = 8
        player_pos = tuple((player_pos[0] + direction[0] * offset, player_pos[1] + direction[1] * offset))
        speed = 600
        bullet_vector = [direction[0] * math.sqrt(2) * speed, direction[1] * math.sqrt(2) * speed]
        self.bullets.append(
            Bullet(self.b2_py_helper.convert_tuple_to_b2_vec2(player_pos),
                   self.b2_py_helper.convert_tuple_to_b2_vec2(bullet_vector),
                   50, self.world, self.b2_py_helper, self.b2_helper))
