import pygame

from dungeonGameInstance import DungeonGameInstance

pygame.display.set_caption("Dilano Emanuel Jermaine Doelwijt G20230417")


def main() -> None:
    pygame.init()
    pygame.mouse.set_visible(False)

    game_instance = DungeonGameInstance()

    while game_instance.game_active:
        game_instance.handle_input()
        game_instance.handle_logic()
        game_instance.handle_graphics()


if __name__ == '__main__':
    main()
