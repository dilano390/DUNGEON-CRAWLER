from enum import Enum
from typing import List

from enemy import Enemy

class Axis(Enum):
    HORIZONTAL = 0
    VERTICAL = 1


class Side(Enum):
    LEFT = 0
    RIGHT = 1
    TOP = 2
    BOTTOM = 3


def flipSide(side: Side) -> Side:
    if side == Side.LEFT: return Side.RIGHT
    if side == Side.RIGHT: return Side.LEFT
    if side == Side.TOP: return Side.BOTTOM
    if side == Side.BOTTOM: return Side.TOP

def updateAllEnemiesInList(theList : List[Enemy],target):
    for e in theList:
        e.update(target)


def checkCollision(r1x: int, r1y: int, r1w: int, r1h: int, r2x: int, r2y: int, r2w: int, r2h: int) -> bool:
    # Check if the two rectangles overlap horizontally
    if r1x + r1w < r2x or r2x + r2w < r1x:
        return False

    # Check if the two rectangles overlap vertically
    if r1y + r1h < r2y or r2y + r2h < r1y:
        return False

    # If both checks pass, the rectangles overlap
    return True
