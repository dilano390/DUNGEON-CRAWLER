import Box2D
import pygame

import dungeon
from b2Helper import B2Helper
from b2PyHelper import B2PyHelper
from dungeonHelper import updateAllEnemiesInList
from enemySpawner import spawnEnemy
from gameFlow import (setUpCrosshair, handleEvents, determineCameraOffset, bulletDecay, drawGame, checkBullets,
                      killEnemies, checkPlayerHits)
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
        self.dungeon = dungeon.Dungeon(self.WINDOW_HEIGHT / 2, self.WINDOW_WIDTH / 2, 700, 15, self.world, 200, 70,
                                       self.b2_helper,
                                       self.b2_py_helper, spawnEnemy)

        self.crosshair = setUpCrosshair(self.b2_py_helper, self, self.world)

        self.heart_image = pygame.image.load("assets/heart.png")  # TODO ADD THE OS PATH JOIN
        self.heart_image = pygame.transform.scale(self.heart_image, (64, 64))
        self.wall_image_v = pygame.image.load("assets/wallV.png")  # TODO ADD THE OS PATH JOIN
        self.wall_image_v = pygame.transform.scale(self.wall_image_v, (20, 700))
        self.wall_image_h = pygame.image.load("assets/wallH.png")  # TODO ADD THE OS PATH JOIN
        self.wall_image_h = pygame.transform.scale(self.wall_image_h, (700, 20))
        self.background = pygame.image.load("assets/background.png")  # TODO ADD THE OS PATH JOIN
        self.background = pygame.transform.scale(self.background, (10000, 10000))
        self.player_image = pygame.image.load("assets/player.png")  # TODO ADD THE OS PATH JOIN
        self.player_image = pygame.transform.scale(self.player_image, (10, 10))
        self.enemy_image = pygame.image.load("assets/enemy.png")  # TODO ADD THE OS PATH JOIN
        self.enemy_image = pygame.transform.scale(self.enemy_image, (23, 23))
        self.crosshair_image = pygame.image.load("assets/crosshair.png")
        self.bullet_image = pygame.image.load("assets/bullet.png")
        self.bullet_image = pygame.transform.scale(self.bullet_image, (5, 5))

        self.prev_x = self.player.b2_object.position[0]
        self.prev_y = self.player.b2_object.position[1]

    def handle_graphics(self):
        self.screen.fill((80, 80, 80))
        self.crosshair.position = self.b2_py_helper.convert_tuple_to_b2_vec2(
            self.b2_py_helper.flip_y_axis(pygame.mouse.get_pos()))
        drawGame(self.b2_py_helper, self, self.screen, self.world)
        pygame.display.flip()

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

# TODO ADD QUESTION MARK BUTTON THAT WILL SHOW KEYS
# TODO MAIN MENU
# TODO GAME OVER SCREEN
# TODO PAUSE BUTTON
# TODO ADD PROGRESS TRACKER
# TODO ADD TIMER
# TODO ADD HIGHSCORES FROM THE TIME
