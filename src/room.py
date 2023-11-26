from typing import List

import Box2D

from b2Helper import B2Helper
from b2PyHelper import B2PyHelper
from dungeonHelper import Side

class Room:
    def __init__(self, x: int, y: int, w: int, h: int, corridorSides: List[Side], corridorWidth: int, side: Side,
                 world: Box2D.b2World, b2h: B2Helper, b2pyh: B2PyHelper):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.world = world
        self.side = side
        self.b2h = b2h
        self.b2pyh = b2pyh
        self.enemies = []

        left = self.b2h.createEdge(0, h, 0, 0)
        top = self.b2h.createEdge(w, 0, 0, self.h)
        bottom = self.b2h.createEdge(w, 0, 0, 0)
        right = self.b2h.createEdge(0, h, self.w, 0)
        self.corridors = corridorSides

        # 0  = left
        # 1 = right
        # 2 =  top
        # 3 = bottom

        self.walls = [left, right, top, bottom]
        for i in range(len(self.corridors)):
            corridor = self.corridors[i]
            if corridor:
                self.createWall(Side(i), corridorWidth, h, w)

    def createWall(self, corridorSide: Side, corridorWidth: int, h: int, w: int) -> None:
        if corridorSide == Side.TOP:
            self.walls[2] = self.b2h.createEdge(w / 2 - corridorWidth / 2, 0, 0, self.h)
            self.walls.append(self.b2h.createEdge(w / 2 - corridorWidth / 2, 0, w / 2 + corridorWidth / 2, self.h))
        elif corridorSide == Side.BOTTOM:
            self.walls[3] = self.b2h.createEdge(w / 2 - corridorWidth / 2, 0, 0, 0)
            self.walls.append(self.b2h.createEdge(w / 2 - corridorWidth / 2, 0, w / 2 + corridorWidth / 2, 0))
        elif corridorSide == Side.LEFT:
            self.walls.append(self.b2h.createEdge(0, h / 2 - corridorWidth / 2, 0, h / 2 + corridorWidth / 2))
            self.walls[0] = self.b2h.createEdge(0, h / 2 - corridorWidth / 2, 0, 0)
        elif corridorSide == Side.RIGHT:
            self.walls[1] = self.b2h.createEdge(0, h / 2 - corridorWidth / 2, self.w, 0)
            self.walls.append(self.b2h.createEdge(0, h / 2 - corridorWidth / 2, self.w, h / 2 + corridorWidth / 2))
