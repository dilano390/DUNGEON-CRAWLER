from typing import List

import Box2D

from b2Helper import B2Helper
from b2PyHelper import B2PyHelper
from dungeonHelper import Side


class Room:
    def __init__(self, x: int, y: int, w: int, h: int, corridor_sides: List[Side], corridor_width: int, side: Side,
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
        self.door_blocker = None
        self.door_blockers = []
        self.door_blockers.append(self.b2h.create_edge(0, self.h, 0, 0))
        self.door_blockers.append(self.b2h.create_edge(0, self.h, self.w, 0))
        self.door_blockers.append(self.b2h.create_edge(self.w, 0, 0, self.h))
        self.door_blockers.append(self.b2h.create_edge(self.w, 0, 0, 0))
        left = self.b2h.create_edge(0, h, 0, 0)
        top = self.b2h.create_edge(w, 0, 0, h)
        bottom = self.b2h.create_edge(w, 0, 0, 0)
        right = self.b2h.create_edge(0, h, w, 0)
        self.corridors = corridor_sides
        self.closed = False
        # comp 4300
        # 0  = left
        # 1 = right
        # 2 =  top
        # 3 = bottom

        self.walls = [left, right, top, bottom]
        for i in range(len(self.corridors)):
            corridor = self.corridors[i]
            if corridor:
                self.create_wall(Side(i), corridor_width, h, w)

    def close_room(self):
        self.door_blocker = self.world.CreateStaticBody(position=self.b2pyh.convert_cords_to_b2_vec2(self.x, self.y),
                                                        shapes=self.door_blockers)
        self.closed = True

    def open_room(self):
        self.world.DestroyBody(self.door_blocker)
        self.closed = False

    def create_wall(self, corridor_side: Side, corridor_width: int, h: int, w: int) -> None:
        if corridor_side == Side.TOP:
            self.walls[2] = self.b2h.create_edge(w / 2 - corridor_width / 2, 0, 0, self.h)
            self.walls.append(self.b2h.create_edge(w / 2 - corridor_width / 2, 0, w / 2 + corridor_width / 2, self.h))
        elif corridor_side == Side.BOTTOM:
            self.walls[3] = self.b2h.create_edge(w / 2 - corridor_width / 2, 0, 0, 0)
            self.walls.append(self.b2h.create_edge(w / 2 - corridor_width / 2, 0, w / 2 + corridor_width / 2, 0))
        elif corridor_side == Side.LEFT:
            self.walls.append(self.b2h.create_edge(0, h / 2 - corridor_width / 2, 0, h / 2 + corridor_width / 2))
            self.walls[0] = self.b2h.create_edge(0, h / 2 - corridor_width / 2, 0, 0)
        elif corridor_side == Side.RIGHT:
            self.walls[1] = self.b2h.create_edge(0, h / 2 - corridor_width / 2, self.w, 0)
            self.walls.append(self.b2h.create_edge(0, h / 2 - corridor_width / 2, self.w, h / 2 + corridor_width / 2))
