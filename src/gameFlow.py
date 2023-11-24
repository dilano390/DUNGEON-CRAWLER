from typing import Tuple

import Box2D
import pygame

from b2PyHelper import B2PyHelper
from dungeonGameInstance import DungeonGameInstance
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


def bulletDecay(gameInstance: DungeonGameInstance, world: Box2D.b2World) -> None:
    for bullet in gameInstance.bulletsUpForDeletion:
        world.DestroyBody(bullet)
        gameInstance.bulletsUpForDeletion.remove(bullet)


def drawGame(b2pyh: B2PyHelper, gameInstance: DungeonGameInstance, screen: pygame.surface,
             world: Box2D.b2World) -> None:
    for body in world.bodies:
        # if body.userData is not None:
        #     if body.userData["shatter_after_impact"] and not body.userData["impacted"] and len(body.contacts) > 0:
        #         body.userData["impact_time"] = pygame.time.get_ticks()
        #         body.userData["impacted"] = True
        #     if body.userData["impacted"]:
        #         if pygame.time.get_ticks() - body.userData["impact_time"] > gameInstance.BULLET_LIFETIME:
        #             gameInstance.bulletsUpForDeletion.append(body)

        for fixture in body.fixtures:
            shape = fixture.shape
            if isinstance(shape, Box2D.b2CircleShape):
                pos = b2pyh.flipYaxis(b2pyh.convertB2Vec2toTuple(body.position))
                pygame.draw.circle(screen, (255, 0, 100), pos,
                                   shape.radius * gameInstance.PPM)
            else:
                vertices = [(body.transform * v) * gameInstance.PPM for v in shape.vertices]
                vertices = [(v[0], gameInstance.WINDOW_HEIGHT - v[1]) for v in vertices]
                b2pyh.offsetBodies(vertices)

                if isinstance(shape, Box2D.b2EdgeShape):
                    pygame.draw.line(screen, (0, 155, 255), vertices[0], vertices[1], 3)
                elif isinstance(shape, Box2D.b2PolygonShape):

                    pygame.draw.polygon(screen, (255, 0, 0), vertices)
