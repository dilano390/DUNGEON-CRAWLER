from typing import Tuple

import Box2D
import pygame

from b2PyHelper import B2PyHelper
from enemy import Enemy
from player import Player


def setUpCrosshair(b2pyh: B2PyHelper, game_instance, world: Box2D.b2World) -> Box2D.b2Body:
    crosshair = world.CreateStaticBody(
        position=(b2pyh.convert_tuple_to_b2_vec2(b2pyh.flip_y_axis(pygame.mouse.get_pos()))),
        shapes=(Box2D.b2CircleShape(radius=0.3)))
    crosshair.fixtures[0].filterData.categoryBits = game_instance.NON_COLLIDING_CATEGORY
    crosshair.fixtures[0].filterData.maskBits = game_instance.NON_COLLIDING_MASK
    return crosshair


def handleEvents(game_instance) -> None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_instance.game_active = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
            game_instance.player.switch_weapon()

def handleMouseInput(game_instance) -> None:
    mouse_keys = pygame.mouse.get_pressed(num_buttons=3)
    if mouse_keys[0]:
        game_instance.player.shoot()

def determineCameraOffset(game_instance, player: Player, prev_x: float, prev_y: float) -> Tuple[
    float, float]:
    dx = (player.b2_object.position[0] - prev_x) * game_instance.PPM
    dy = (player.b2_object.position[1] - prev_y) * game_instance.PPM
    prev_x = player.b2_object.position[0]
    prev_y = player.b2_object.position[1]
    game_instance.camera_offset[0] -= dx
    game_instance.camera_offset[1] += dy
    return prev_x, prev_y


def checkBullets(game_instance):
    for bullet in game_instance.bullets:
        handleBullet(bullet, game_instance)


def handleBullet(bullet, game_instance):
    if len(bullet.body.contacts):
        for contact in bullet.body.contacts:
            contact_user_data = contact.other.userData
            if contact_user_data is not None:
                if 'enemy' in contact_user_data:
                    enemy: Enemy = contact_user_data['enemy']
                    damage = game_instance.player.current_weapon.damage
                    enemy.take_damage(damage)
                elif 'player' in contact_user_data:  # DO NOT REMOVE. IF YOU REMOVE YOU CAUSE GHOST BULLETS
                    return True

        game_instance.bullets_up_for_deletion.append(bullet)
        bullet.impact_time = pygame.time.get_ticks()
        game_instance.bullets.remove(bullet)


def checkPlayerHits(game_instance):
    body = game_instance.player.b2_object
    player = game_instance.player
    if len(body.contacts):
        for contact in body.contacts:
            contact_user_data = contact.other.userData
            if contact_user_data is not None and 'enemy' in contact_user_data:
                player.player_take_damage(game_instance)


def bulletDecay(game_instance, world: Box2D.b2World) -> None:
    for bullet in game_instance.bullets_up_for_deletion:
        if pygame.time.get_ticks() - bullet.impact_time > game_instance.BULLET_LIFETIME_AFTER_COLL:
            world.DestroyBody(bullet.body)
            game_instance.bullets_up_for_deletion.remove(bullet)


def killEnemies(room):
    for enemy in room.enemies:
        if enemy.lives <= 0:
            room.enemies.remove(enemy)


def drawGame(b2pyh: B2PyHelper, game_instance, screen: pygame.surface,
             world: Box2D.b2World) -> None:
    drawBackground(game_instance, screen)
    determineBackgroundOffsets(game_instance)

    handleBox2dDrawing(b2pyh, game_instance, screen, world)
    x = 10
    for _ in range(game_instance.player.lives):
        screen.blit(game_instance.heart_image, (x, 0))
        x += 50


def handleBox2dDrawing(b2pyh, game_instance, screen, world):
    for body in world.bodies:
        for fixture in body.fixtures:
            shape = fixture.shape
            handleBody(b2pyh, body, game_instance, screen, shape)


def handleBody(b2pyh, body, game_instance, screen, shape):
    if isinstance(shape, Box2D.b2CircleShape):
        pos = b2pyh.flip_y_axis(b2pyh.convert_b2_vec2_to_tuple(body.position))
        screen.blit(game_instance.crosshair_image, (pos[0] - 8, pos[1] - 8))
    else:
        vertices = [(body.transform * v) * game_instance.PPM for v in shape.vertices]
        vertices = [(v[0], game_instance.WINDOW_HEIGHT - v[1]) for v in vertices]
        b2pyh.offset_bodies(vertices)

        handleDrawingBodyWithVertices(body, game_instance, screen, shape, vertices)


def handleDrawingBodyWithVertices(body, game_instance, screen, shape, vertices):
    if isinstance(shape, Box2D.b2EdgeShape):
        pygame.draw.line(screen, (66, 12, 55), vertices[0], vertices[1], 3)
    elif isinstance(shape, Box2D.b2PolygonShape):
        handlePolygonDrawing(body, game_instance, screen, vertices)


def handlePolygonDrawing(body, game_instance, screen, vertices):
    color = (255, 0, 0)
    if body.userData is not None:
        if 'player' in body.userData:
            screen.blit(game_instance.player_image, (vertices[0][0] - 10, vertices[1][1]))
        elif 'enemy' in body.userData:
            if 'color' in body.userData:
                color = body.userData['color']
            pygame.draw.polygon(screen, color, vertices)
            if 'big' in body.userData and  body.userData['big']:
                screen.blit(game_instance.big_enemy_image, (vertices[0][0] - 32, vertices[1][1]))
            else:
                screen.blit(game_instance.enemy_image, (vertices[0][0] - 20, vertices[1][1]))


        elif 'bullet' in body.userData:
            screen.blit(game_instance.bullet_image, (vertices[0][0] - 5, vertices[1][1]))
    else:
        pygame.draw.polygon(screen, color, vertices)


def drawBackground(game_instance, screen):
    screen.blit(game_instance.background, determineBackgroundPos(game_instance))


def determineBackgroundPos(game_instance):
    x_offset = game_instance.camera_offset[0] - (5000 + game_instance.background_offset[0])
    y_offset = game_instance.camera_offset[1] - (5000 + game_instance.background_offset[1])
    return x_offset, y_offset


def determineBackgroundOffsets(game_instance):
    if game_instance.camera_offset[0] - game_instance.background_offset[0] > 4000:
        game_instance.background_offset = (
            game_instance.background_offset[0] + 4000, game_instance.background_offset[1])
    if game_instance.camera_offset[1] - game_instance.background_offset[1] > 4000:
        game_instance.background_offset = (
            game_instance.background_offset[0], game_instance.background_offset[1] + 4000)
    if game_instance.camera_offset[0] - game_instance.background_offset[0] < -4000:
        game_instance.background_offset = (
            game_instance.background_offset[0] - 4000, game_instance.background_offset[1])
    if game_instance.camera_offset[1] - game_instance.background_offset[1] < -4000:
        game_instance.background_offset = (
            game_instance.background_offset[0], game_instance.background_offset[1] - 4000)
