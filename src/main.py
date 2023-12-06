import pygame

from dungeonGameInstance import DungeonGameInstance
from dungeonHelper import updateAllEnemiesInList
from gameFlow import (setUpCrosshair, handleEvents, determineCameraOffset, bulletDecay, drawGame, checkBullets,
                      killEnemies, checkPlayerHits)

pygame.display.set_caption("Dilano Emanuel Jermaine Doelwijt G20230417")


def main() -> None:
    pygame.init()
    pygame.mouse.set_visible(False)

    game_instance = DungeonGameInstance()
    world = game_instance.world
    dungeon = game_instance.dungeon
    screen = game_instance.screen
    player = game_instance.player
    clock = game_instance.clock
    b2h = game_instance.b2_helper
    b2pyh = game_instance.b2_py_helper

    crosshair = setUpCrosshair(b2pyh, game_instance, world)

    b2h.add_box_to_world(b2h.create_polygon(10, 30, 30, 30),
                         b2pyh.convert_cords_to_b2_vec2(game_instance.WINDOW_WIDTH / 2, game_instance.WINDOW_HEIGHT / 2), 20, 2,
                         1)

    prev_x = player.b2_object.position[0]
    prev_y = player.b2_object.position[1]

    while game_instance.game_active:
        current_room = dungeon.current_room
        handleEvents(game_instance)

        crosshair.position = b2pyh.convert_tuple_to_b2_vec2(b2pyh.flip_y_axis(pygame.mouse.get_pos()))

        prev_x, prev_y = determineCameraOffset(game_instance, player, prev_x, prev_y)

        player.determine_velocity()

        screen.fill((80, 80, 80))

        drawGame(b2pyh, game_instance, screen, world)

        killEnemies(current_room)
        updateAllEnemiesInList(current_room.enemies, player.b2_object)

        checkPlayerHits(game_instance)

        pygame.display.flip()

        dungeon.track_and_change_room(b2pyh.convert_b2_vec2_to_tuple(player.b2_object.position))

        checkBullets(game_instance)
        bulletDecay(game_instance, world)

        world.Step(game_instance.TIME_STEP, 10, 10)
        clock.tick(game_instance.FPS)


if __name__ == '__main__':
    main()
