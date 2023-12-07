import pygame

from dungeonGameInstance import DungeonGameInstance

pygame.display.set_caption("Dilano Emanuel Jermaine Doelwijt G20230417")


def main() -> None:
    pygame.init()
    pygame.mouse.set_visible(False)

    game_instance = DungeonGameInstance()




    while game_instance.game_active:
        if game_instance.start_screen:
            game_instance.draw_main_screen()

        elif game_instance.main_game_loop:
            game_instance.handle_input()
            game_instance.handle_logic()
            game_instance.handle_graphics()
        elif game_instance.game_over:
            game_instance.draw_game_over_screen()
        elif game_instance.victory:
            game_instance.draw_victory_screen()
        pygame.display.flip()

if __name__ == '__main__':
    main()
