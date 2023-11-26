from typing import List, Tuple
import Box2D


class B2PyHelper:
    def __init__(self, PPM: int, cameraOffset: List[int], sensitivity: int, WINDOW_HEIGHT: int):
        self.cameraOffset = cameraOffset
        self.sensitivity = sensitivity
        self.PPM = PPM
        self.cameraOffset = cameraOffset
        self.WINDOW_HEIGHT = WINDOW_HEIGHT

    def convertTupleToB2Vec2(self, loc: tuple) -> Box2D.b2Vec2:
        return Box2D.b2Vec2(loc[0] / self.PPM, loc[1] / self.PPM)

    def convertCordsToB2Vec2(self, x: int, y: int) -> Box2D.b2Vec2:
        return Box2D.b2Vec2(x / self.PPM, y / self.PPM)

    def convertB2Vec2toTuple(self, loc: Box2D.b2Vec2) -> tuple:
        return tuple([loc.x * self.PPM, loc.y * self.PPM])

    def flipYaxis(self, cords: tuple) -> tuple:
        return tuple((cords[0], self.WINDOW_HEIGHT - cords[1]))

    def offsetBodies(self, vertices: List[Tuple[float]]):
        for i in range(len(vertices)):
            vertice = vertices[i]
            vertices[i] = tuple((vertice[0] + self.cameraOffset[0], vertice[1] + self.cameraOffset[1]))
