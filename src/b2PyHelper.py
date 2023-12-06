from typing import List, Tuple

import Box2D


class B2PyHelper:
    def __init__(self, ppm: int, camera_offset: List[int], sensitivity: int, window_height: int):
        self.camera_offset = camera_offset
        self.sensitivity = sensitivity
        self.PPM = ppm
        self.WINDOW_HEIGHT = window_height

    def convert_tuple_to_b2_vec2(self, loc: tuple) -> Box2D.b2Vec2:
        return Box2D.b2Vec2(loc[0] / self.PPM, loc[1] / self.PPM)

    def convert_cords_to_b2_vec2(self, x: int, y: int) -> Box2D.b2Vec2:
        return Box2D.b2Vec2(x / self.PPM, y / self.PPM)

    def convert_b2_vec2_to_tuple(self, loc: Box2D.b2Vec2) -> tuple:
        return tuple([loc.x * self.PPM, loc.y * self.PPM])

    def flip_y_axis(self, cords: tuple) -> tuple:
        return tuple((cords[0], self.WINDOW_HEIGHT - cords[1]))

    def offset_bodies(self, vertices: List[Tuple[float]]):
        for i in range(len(vertices)):
            v = vertices[i]
            vertices[i] = tuple((v[0] + self.camera_offset[0], v[1] + self.camera_offset[1]))
