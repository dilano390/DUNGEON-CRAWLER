import Box2D
import pygame

import dungeon
from b2Helper import B2Helper
from b2PyHelper import B2PyHelper
from dungeonHelper import updateAllEnemiesInList
from enemySpawner import spawnEnemy
from gameFlow import (setUpCrosshair, handleEvents, determineCameraOffset, bulletDecay, drawGame, checkBullets,
                      killEnemies, checkPlayerHits, handleMouseInput)
from player import Player


class DungeonGameInstance:
    def __init__(self):

        self.PPM = 20
        self.FPS = 60
        self.TIME_STEP = 1.0 / self.FPS
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 800
        self.INPUT_SENSITIVITY = 10
        self.BULLET_LIFETIME = 3000
        self.BULLET_LIFETIME_AFTER_COLL = 500
        self.NON_COLLIDING_CATEGORY = 0
        self.NON_COLLIDING_MASK = 0

        self.bullets_up_for_deletion = []
        self.enemies_up_for_deletion = []
        self.game_active = True
        self.start_screen = True
        self.game_over = False
        self.victory = False
        self.main_game_loop = False

        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.world = Box2D.b2World([0, 0], doSleep=True)
        self.clock = pygame.time.Clock()
        self.camera_offset = [0, 0]
        self.b2_py_helper = B2PyHelper(self.PPM, self.camera_offset, self.INPUT_SENSITIVITY, self.WINDOW_HEIGHT)
        self.b2_helper = B2Helper(self.world, self.PPM)
        self.bullets = []
        self.background_offset = (0, 0)
        self.player: Player = Player(tuple((self.WINDOW_HEIGHT / 2, self.WINDOW_HEIGHT / 2)), self.b2_py_helper,
                                     self.b2_helper,
                                     self.camera_offset, self.world, self.INPUT_SENSITIVITY, self.bullets)
        win_game = lambda: setattr(self, 'victory', True) or setattr(self, 'main_game_loop', False)

        self.dungeon = dungeon.Dungeon(self.WINDOW_HEIGHT / 2, self.WINDOW_WIDTH / 2, 700, 3, self.world, 200, 70,
                                       self.b2_helper,
                                       self.b2_py_helper, spawnEnemy, win_game)

        self.crosshair = setUpCrosshair(self.b2_py_helper, self, self.world)

        self.prev_x = self.player.b2_object.position[0]
        self.prev_y = self.player.b2_object.position[1]

        self.heart_image = pygame.image.load("assets/heart.png")  # TODO ADD THE OS PATH JOIN
        self.heart_image = pygame.transform.scale(self.heart_image, (64, 64))
        self.wall_image_v = pygame.image.load("assets/wallV.png")
        self.wall_image_v = pygame.transform.scale(self.wall_image_v, (20, 700))
        self.wall_image_h = pygame.image.load("assets/wallH.png")
        self.wall_image_h = pygame.transform.scale(self.wall_image_h, (700, 20))
        self.background = pygame.image.load("assets/background.png")
        self.background = pygame.transform.scale(self.background, (10000, 10000))
        self.player_image = pygame.image.load("assets/player.png")
        self.player_image = pygame.transform.scale(self.player_image, (10, 10))
        self.enemy_image = pygame.image.load("assets/enemy.png")
        self.enemy_image = pygame.transform.scale(self.enemy_image, (23, 23))
        self.big_enemy_image = pygame.image.load("assets/bigEnemy.png")
        self.big_enemy_image = pygame.transform.scale(self.big_enemy_image,(35,35))
        self.crosshair_image = pygame.image.load("assets/crosshair.png")
        self.bullet_image = pygame.image.load("assets/bullet.png")
        self.bullet_image = pygame.transform.scale(self.bullet_image, (5, 5))
        self.start_screen_image = pygame.image.load("assets/startScreen.png")
        self.start_screen_image = pygame.transform.scale(self.start_screen_image, (800, 800))
        self.game_over_image = pygame.image.load("assets/gameOverScreen.png")
        self.game_over_image = pygame.transform.scale(self.game_over_image, (800, 800))
        self.victory_image = pygame.image.load("assets/victoryScreen.png")
        self.victory_image = pygame.transform.scale(self.victory_image, (800, 800))
        self.sniper_image = pygame.image.load("assets/sniper.png")
        self.sniper_image = pygame.transform.scale(self.sniper_image,(64,64))
        self.pistol_image = pygame.image.load("assets/pistol.png")
        self.pistol_image = pygame.transform.scale(self.pistol_image,(64,64))
        self.weapon_images = [self.pistol_image,self.sniper_image]
    def reset_game(self):
        self.bullets_up_for_deletion = []
        self.enemies_up_for_deletion = []
        self.game_active = True
        self.start_screen = True
        self.game_over = False
        self.victory = False
        self.main_game_loop = False

        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.world = Box2D.b2World([0, 0], doSleep=True)
        self.clock = pygame.time.Clock()
        self.camera_offset = [0, 0]
        self.b2_py_helper = B2PyHelper(self.PPM, self.camera_offset, self.INPUT_SENSITIVITY, self.WINDOW_HEIGHT)
        self.b2_helper = B2Helper(self.world, self.PPM)
        self.bullets = []
        self.background_offset = (0, 0)
        self.player: Player = Player(tuple((self.WINDOW_HEIGHT / 2, self.WINDOW_HEIGHT / 2)), self.b2_py_helper,
                                     self.b2_helper,
                                     self.camera_offset, self.world, self.INPUT_SENSITIVITY, self.bullets)

        win_game: () = lambda: setattr(self, 'victory', True) or setattr(self, 'main_game_loop', False)

        self.dungeon = dungeon.Dungeon(self.WINDOW_HEIGHT / 2, self.WINDOW_WIDTH / 2, 700, 3, self.world, 200, 70,
                                       self.b2_helper,
                                       self.b2_py_helper, spawnEnemy, win_game)

        self.crosshair = setUpCrosshair(self.b2_py_helper, self, self.world)
        self.prev_x = self.player.b2_object.position[0]
        self.prev_y = self.player.b2_object.position[1]

    def handle_graphics(self):
        self.screen.fill((80, 80, 80))
        self.crosshair.position = self.b2_py_helper.convert_tuple_to_b2_vec2(
            self.b2_py_helper.flip_y_axis(pygame.mouse.get_pos()))
        drawGame(self.b2_py_helper, self, self.screen, self.world)
        self.draw_text_top_right(f" Room {self.dungeon.current_room_num + 1} of {self.dungeon.room_count}")

    def draw_text_top_right(self, text):
        font = pygame.font.SysFont('timesnewroman', 16)
        text_surface = font.render(text, True, (0, 0, 0))  # Rendering text

        text_rect = text_surface.get_rect()
        text_rect.topright = (800, 0)

        self.screen.blit(text_surface, text_rect)  # Drawing text onto the screen

    def handle_logic(self):
        current_room = self.dungeon.current_room
        self.prev_x, self.prev_y = determineCameraOffset(self, self.player, self.prev_x, self.prev_y)
        killEnemies(current_room)
        checkPlayerHits(self)
        updateAllEnemiesInList(current_room.enemies, self.player.b2_object)
        self.dungeon.track_and_change_room(self.b2_py_helper.convert_b2_vec2_to_tuple(self.player.b2_object.position))
        checkBullets(self)
        bulletDecay(self, self.world)

        self.world.Step(self.TIME_STEP, 10, 10)
        self.clock.tick(self.FPS)

    def handle_input(self):
        self.player.determine_velocity()
        handleEvents(self)
        handleMouseInput(self)

    def draw_main_screen(self):
        self.screen.blit(self.start_screen_image, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_active = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.start_screen = False
                self.main_game_loop = True

    def draw_game_over_screen(self):
        self.screen.blit(self.game_over_image, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_active = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.game_over = False
                self.reset_game()
                self.main_game_loop = True

    def draw_victory_screen(self):
        self.screen.blit(self.victory_image, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_active = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.victory = False
                self.reset_game()
                self.main_game_loop = True

# TODO ADD QUESTION MARK BUTTON THAT WILL SHOW KEYS

# TODO PAUSE BUTTON
