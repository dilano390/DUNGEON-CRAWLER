from random import randrange

from enemy import Enemy


def spawnEnemy(room, b2pyh, b2h, world):
    for i in range(randrange(2, 6)):
        enemy = Enemy(tuple((room.x, room.y)), tuple((room.w, room.h)), randrange(2, 17),
                      randrange(1,8), b2pyh, b2h, world)
        room.enemies.append(enemy)
