import random

import Box2D

from b2Helper import B2Helper
from b2PyHelper import B2PyHelper
from dungeonHelper import Side, flipSide, checkCollision
from room import Room


class Dungeon:
    def __init__(self, x: int, y: int, room_wh: int, room_count: int, world: Box2D.b2World,
                 corridor_len: int, corridor_width: int, b2h: B2Helper,
                 b2pyh: B2PyHelper, enemy_spawner) -> None:
        self.world = world
        self.rooms = []
        self.x = x
        self.y = y
        self.corridor_len = corridor_len
        self.corridor_width = corridor_width
        self.b2h = b2h
        self.b2pyh = b2pyh
        self.enemy_spawn_func = enemy_spawner
        for _ in range(room_count):
            self.add_room(room_wh, room_wh)
        self.visited = [self.rooms[0]]
        self.current_room = self.rooms[0]
        self.current_room.close_room()
        self.enemy_spawn_func(self.rooms[0], self.b2pyh, self.b2h, self.world)
        self.room_changed = False
        self.room_count = len(self.rooms)

    def track_and_change_room(self, player_position):

        for room in self.rooms:
            if checkCollision(player_position[0], player_position[1], 10, 10, room.x + 10, room.y + 10, room.w - 20,
                              room.h - 20):
                if self.current_room != room and room not in self.visited:
                    self.visited.append(room)
                    self.enemy_spawn_func(room, self.b2pyh, self.b2h, self.world)
                    room.close_room()

                self.current_room = room
                if not len(self.current_room.enemies) and self.current_room.closed:
                    self.current_room.open_room()
                    if self.rooms[-1] == room:
                        print("You win")  # TODO: END THE GAME LOOP -> PROGRESS TO WIN SCREEN
                return

    def add_corridor(self, side: Side, room_w: int, room_h: int) -> None:
        x = self.x
        x2 = self.x
        y = self.y
        y2 = self.y
        h = 0
        w = 0
        if side == Side.RIGHT:
            x += room_w
            x2 = x
            y += room_h / 2 - self.corridor_width / 2
            y2 += room_h / 2 + self.corridor_width / 2
            w = self.corridor_len
        elif side == Side.LEFT:
            y += room_h / 2 - self.corridor_width / 2
            y2 += room_h / 2 + self.corridor_width / 2
            x -= self.corridor_len
            x2 = x
            w = self.corridor_len
        elif side == Side.TOP:
            y += room_h
            y2 = y
            x += room_w / 2 - self.corridor_width / 2
            x2 += room_w / 2 + self.corridor_width / 2
            h = self.corridor_len
        else:
            y -= self.corridor_len
            y2 = y
            h = self.corridor_len
            x += room_w / 2 - self.corridor_width / 2
            x2 += room_w / 2 + self.corridor_width / 2
        edges = [self.b2h.create_edge(w, h, x, y), self.b2h.create_edge(w, h, x2, y2)]
        self.world.CreateStaticBody(position=self.b2pyh.convert_cords_to_b2_vec2(0, 0), shapes=edges)

    def adjust_for_side(self, x: int, y: int, w: int, h: int, side: Side) -> tuple:
        new_x, new_y = x, y
        if side == Side.LEFT:
            new_x -= self.corridor_len
        elif side == Side.RIGHT:
            new_x += w + self.corridor_len
        elif side == Side.TOP:
            new_y += h + self.corridor_len
        else:
            new_y -= self.corridor_len
        return new_x, new_y

    def find_non_overlapping_side(self, w: int, h: int) -> Side:
        sides = list(Side)
        random.shuffle(sides)  # Shuffle sides to try in random order

        for side in sides:
            overlap = False
            for room in self.rooms:
                new_x, new_y = self.adjust_for_side(self.x, self.y, w, h, side)
                if checkCollision(new_x, new_y, w, h, room.x, room.y,
                                  room.w, room.h):
                    overlap = True
                    break  # Exit the loop if overlap found

            if not overlap:
                return side  # Return the side if no overlap
        return None  # Return None if no non-overlapping side is found

    def add_room(self, w: int, h: int) -> None:
        corridors = [False, False, False, False]
        side = self.find_non_overlapping_side(w, h)
        if len(self.rooms):
            prev_side = self.rooms[-1].side
            prev_side = flipSide(prev_side)
            corridors[prev_side.value] = True
        if side is None:
            return

        corridors[side.value] = True

        room = Room(self.x, self.y, w, h, corridors, self.corridor_width, side, self.world, self.b2h, self.b2pyh)
        self.world.CreateStaticBody(position=self.b2pyh.convert_cords_to_b2_vec2(self.x, self.y), shapes=room.walls)
        # TODO REMOVE THIS CALL TO BOX2D FROM THIS CLASS
        self.add_corridor(side, w, h)
        self.rooms.append(room)
        if side == Side.TOP:
            self.y += h + self.corridor_len
        elif side == Side.LEFT:
            self.x -= w + self.corridor_len
        elif side == Side.RIGHT:
            self.x += w + self.corridor_len
        else:
            self.y -= h + self.corridor_len
