from typing import Tuple

import Box2D
import pygame

from b2PyHelper import B2PyHelper
from dungeonGameInstance import DungeonGameInstance
from enemy import Enemy
from player import Player


def setUpCrosshair(b2pyh: B2PyHelper, gameInstance: DungeonGameInstance, world: Box2D.b2World) -> Box2D.b2Body:
    crosshair = world.CreateStaticBody(
        position=(b2pyh.convertTupleToB2Vec2(b2pyh.flipYaxis(pygame.mouse.get_pos()))),
        shapes=(Box2D.b2CircleShape(radius=0.3)))
    crosshair.fixtures[0].filterData.categoryBits = gameInstance.NON_COLLIDING_CATEGORY
    crosshair.fixtures[0].filterData.maskBits = gameInstance.NON_COLLIDING_MASK
    return crosshair


def handleEvents(gameInstance: DungeonGameInstance) -> None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameInstance.gameActive = False
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            gameInstance.player.shoot()


def determineCameraOffset(gameInstance: DungeonGameInstance, player: Player, prevX: float, prevY: float) -> Tuple[
    float, float]:
    dx = (player.b2Object.position[0] - prevX) * gameInstance.PPM
    dy = (player.b2Object.position[1] - prevY) * gameInstance.PPM
    prevX = player.b2Object.position[0]
    prevY = player.b2Object.position[1]
    gameInstance.cameraOffset[0] -= dx
    gameInstance.cameraOffset[1] += dy
    return prevX, prevY


def checkBullets(gameInstance: DungeonGameInstance):
    for bullet in gameInstance.bullets:
        if len(bullet.body.contacts):
            for contact in bullet.body.contacts:
                contactUserData = contact.other.userData
                if contactUserData is not None:
                    if 'player' in contactUserData:  # DO NOT REMOVE. IF YOU REMOVE YOU CAUSE GHOST BULLETS
                        return
                    if 'enemy' in contactUserData:
                        enemy: Enemy = contactUserData['enemy']
                        enemy.takeDamage(2)
            gameInstance.bulletsUpForDeletion.append(bullet)
            bullet.impactTime = pygame.time.get_ticks()
            gameInstance.bullets.remove(bullet)


def checkPlayerHits(gameInstance: DungeonGameInstance):
    body = gameInstance.player.b2Object
    player = gameInstance.player
    if len(body.contacts):
        for contact in body.contacts:
            contactUserData = contact.other.userData
            if contactUserData is not None:
                if 'enemy' in contactUserData:
                    player.playerTakeDamage(gameInstance)


def bulletDecay(gameInstance: DungeonGameInstance, world: Box2D.b2World) -> None:
    for bullet in gameInstance.bulletsUpForDeletion:
        if pygame.time.get_ticks() - bullet.impactTime > gameInstance.BULLET_LIFETIME_AFTER_COLL:
            world.DestroyBody(bullet.body)
            gameInstance.bulletsUpForDeletion.remove(bullet)


def killEnemies(room):
    for enemy in room.enemies:
        if enemy.lives <= 0:
            room.enemies.remove(enemy)


def drawGame(b2pyh: B2PyHelper, gameInstance: DungeonGameInstance, screen: pygame.surface,
             world: Box2D.b2World) -> None:

    screen.blit(gameInstance.background,(0,0))
    x = 10
    for i in range(gameInstance.player.lives):
        screen.blit(gameInstance.heartImage, (x, 0))
        x += 50

    for body in world.bodies:
        for fixture in body.fixtures:
            shape = fixture.shape
            if isinstance(shape, Box2D.b2CircleShape):
                pos = b2pyh.flipYaxis(b2pyh.convertB2Vec2toTuple(body.position))
                screen.blit(gameInstance.crosshairImage,(pos[0] -8 , pos[1] -8))
                # pygame.draw.circle(screen, (255, 0, 100), pos,
                #                    shape.radius * gameInstance.PPM)
            else:
                vertices = [(body.transform * v) * gameInstance.PPM for v in shape.vertices]
                vertices = [(v[0], gameInstance.WINDOW_HEIGHT - v[1]) for v in vertices]
                b2pyh.offsetBodies(vertices)

                if isinstance(shape, Box2D.b2EdgeShape):
                    if abs(vertices[0][0] - vertices[1][0]) <= 5:
                        pygame.draw.line(screen, (66, 12, 55), vertices[0], vertices[1], 3)
                    else:
                        pygame.draw.line(screen, (66, 12, 55), vertices[0], vertices[1], 3)
                elif isinstance(shape, Box2D.b2PolygonShape):
                    color = (255, 0, 0)
                    if body.userData is not None:
                        if 'color' in body.userData:
                            color = body.userData['color']
                            pygame.draw.polygon(screen, color, vertices)
                        if 'player' in body.userData:
                            screen.blit(gameInstance.playerImage,(vertices[0][0] - 10,vertices[1][1]))
                        if 'enemy' in body.userData:
                            screen.blit(gameInstance.enemyImage,(vertices[0][0] - 20,vertices[1][1]))
                    else:
                        pygame.draw.polygon(screen, color, vertices)