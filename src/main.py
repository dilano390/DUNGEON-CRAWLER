import random

import pygame

from dungeonGameInstance import DungeonGameInstance
from enemy import Enemy
from gameFlow import setUpCrosshair, handleEvents, determineCameraOffset, bulletDecay, drawGame, checkBullets, killEnemy

pygame.display.set_caption("Dilano Emanuel Jermaine Doelwijt G20230417")


def main() -> None:
    pygame.init()
    pygame.mouse.set_visible(False)

    gameInstance = DungeonGameInstance()
    world = gameInstance.world
    dungeon = gameInstance.dungeon
    screen = gameInstance.screen
    player = gameInstance.player
    clock = gameInstance.clock
    b2h = gameInstance.b2Helper
    b2pyh = gameInstance.b2PyHelper

    for i in range(50):
        dungeon.addRoom(500, 500)

    for room in dungeon.rooms:
        for i in range(5):
            Enemy(tuple((room.x, room.y)), tuple((room.w, room.h)), random.randrange(2, 17),
                  10, b2pyh, b2h, world)

    crosshair = setUpCrosshair(b2pyh, gameInstance, world)

    b2h.addBoxToWorld(b2h.createPolygon(10, 30, 30, 30),
                      b2pyh.convertCordsToB2Vec2(gameInstance.WINDOW_WIDTH / 2, gameInstance.WINDOW_HEIGHT / 2), 20, 2,
                      1)

    prevX = player.b2Object.position[0]
    prevY = player.b2Object.position[1]

    while gameInstance.gameActive:
        handleEvents(gameInstance)

        crosshair.position = b2pyh.convertTupleToB2Vec2(b2pyh.flipYaxis(pygame.mouse.get_pos()))

        prevX, prevY = determineCameraOffset(gameInstance, player, prevX, prevY)

        player.determineVelocity()

        screen.fill((80, 80, 80))

        drawGame(b2pyh, gameInstance, screen, world)

        pygame.display.flip()

        checkBullets(gameInstance)
        bulletDecay(gameInstance, world)
        killEnemy(gameInstance, world)

        world.Step(gameInstance.TIME_STEP, 10, 10)
        clock.tick(gameInstance.FPS)


if __name__ == '__main__':
    main()
