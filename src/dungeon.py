import random
import Box2D
from b2Helper import B2Helper
from b2PyHelper import B2PyHelper
from dungeonHelper import Side, flipSide, checkCollision
# from player import Player
from room import Room

class Dungeon:
    def __init__(self, x: int, y: int, roomWH: int, roomCount: int, world: Box2D.b2World,
                 corridorLen: int, corridorWidth: int, b2h: B2Helper,
                 b2pyh: B2PyHelper, enemySpawner) -> None:
        self.world = world
        self.rooms = []
        self.x = x
        self.y = y
        self.corridorLen = corridorLen
        self.corridorWidth = corridorWidth
        self.b2h = b2h
        self.b2pyh = b2pyh
        self.enemySpawnFunc = enemySpawner
        for i in range(roomCount):
            self.addRoom(roomWH, roomWH)
        self.visited = [self.rooms[0]]
        self.currentRoom = self.rooms[0]
        self.currentRoom.closeRoom()
        self.enemySpawnFunc(self.rooms[0], self.b2pyh, self.b2h, self.world)
        self.roomChanged = False
        self.roomCount = len(self.rooms)


    def trackAndChangeRoom(self, playerPosition):

        for room in self.rooms:
            if checkCollision(playerPosition[0], playerPosition[1], 10, 10, room.x + 10, room.y + 10, room.w - 20, room.h - 20):
                if not self.currentRoom == room and room not in self.visited:
                    self.visited.append(room)
                    self.enemySpawnFunc(room, self.b2pyh, self.b2h, self.world)
                    room.closeRoom()




                self.currentRoom = room
                if not len(self.currentRoom.enemies) and self.currentRoom.closed:
                    self.currentRoom.openRoom()
                return

    def addCorridor(self, side: Side, roomW: int, roomH: int) -> None:
        x = self.x
        x2 = self.x
        y = self.y
        y2 = self.y
        h = 0
        w = 0
        if side == Side.RIGHT:
            x += roomW
            x2 = x
            y += roomH / 2 - self.corridorWidth / 2
            y2 += roomH / 2 + self.corridorWidth / 2
            w = self.corridorLen
        elif side == Side.LEFT:
            y += roomH / 2 - self.corridorWidth / 2
            y2 += roomH / 2 + self.corridorWidth / 2
            x -= self.corridorLen
            x2 = x
            w = self.corridorLen
        elif side == Side.TOP:
            y += roomH
            y2 = y
            x += roomW / 2 - self.corridorWidth / 2
            x2 += roomW / 2 + self.corridorWidth / 2
            h = self.corridorLen
        else:
            y -= self.corridorLen
            y2 = y
            h = self.corridorLen
            x += roomW / 2 - self.corridorWidth / 2
            x2 += roomW / 2 + self.corridorWidth / 2
        edges = [self.b2h.createEdge(w, h, x, y), self.b2h.createEdge(w, h, x2, y2)]
        self.world.CreateStaticBody(position=self.b2pyh.convertCordsToB2Vec2(0, 0), shapes=edges)

    def adjustForSide(self, x: int, y: int, w: int, h: int, side: Side) -> tuple:
        newX, newY = x, y
        if side == Side.LEFT:
            newX -= self.corridorLen
        elif side == Side.RIGHT:
            newX += w + self.corridorLen
        elif side == Side.TOP:
            newY += h + self.corridorLen
        else:
            newY -= self.corridorLen
        return newX, newY

    def findNonOverlappingSide(self, w: int, h: int) -> Side:
        sides = list(Side)
        random.shuffle(sides)  # Shuffle sides to try in random order

        for side in sides:
            overlap = False
            for room in self.rooms:
                new_x, new_y = self.adjustForSide(self.x, self.y, w, h, side)
                if checkCollision(new_x, new_y, w, h, room.x, room.y,
                                  room.w, room.h):
                    overlap = True
                    break  # Exit the loop if overlap found

            if not overlap:
                return side  # Return the side if no overlap
        print("FAILED TO FIND")
        return None  # Return None if no non-overlapping side is found

    def addRoom(self, w: int, h: int) -> None:
        corridors = [False, False, False, False]
        side = self.findNonOverlappingSide(w, h)
        if len(self.rooms):
            prevSide = self.rooms[-1].side
            prevSide = flipSide(prevSide)
            corridors[prevSide.value] = True
        if side is None:
            return

        corridors[side.value] = True

        room = Room(self.x, self.y, w, h, corridors, self.corridorWidth, side, self.world, self.b2h, self.b2pyh)
        self.world.CreateStaticBody(position=self.b2pyh.convertCordsToB2Vec2(self.x, self.y), shapes=room.walls)
        # TODO REMOVE THIS CALL TO BOX2D FROM THIS CLASS
        self.addCorridor(side, w, h)
        self.rooms.append(room)
        if side == Side.TOP:
            self.y += h + self.corridorLen
        elif side == Side.LEFT:
            self.x -= w + self.corridorLen
        elif side == Side.RIGHT:
            self.x += w + self.corridorLen
        else:
            self.y -= h + self.corridorLen
