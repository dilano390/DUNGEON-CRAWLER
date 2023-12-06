from random import randrange

from enemy import Enemy


def spawnEnemy(room, b2pyh, b2h,
               world):  # TODO ADD BOSS MONESTERS TO LAST ROOM AND MAYBEW MIDDLE ROOM ALSO MAKE LOW CHANCE FOR THEM TO RANDOMLY SPAWN
    for i in range(randrange(2, 6)):
        enemy = Enemy(tuple((room.x, room.y)), tuple((room.w, room.h)), randrange(2, 17),
                      randrange(1, 8), b2pyh, b2h, world)
        room.enemies.append(enemy)
