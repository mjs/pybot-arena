from typing import Tuple

import pygame
import entities
from controller import Controller
import background as bg
import assets
import algo


def checkWallCollision(points: Tuple[int, int, int, int]):
    return any((wall_coll1.rect_collide(points)[0], wall_coll2.rect_collide(points)[0],
                wall_coll3.rect_collide(points)[0], wall_coll4.rect_collide(points)[0],
               wall_coll5.rect_collide(points)[0], wall_coll6.rect_collide(points)[0]))


def main():
    global running

    time = 0
    game_over = False

    time_rect = pygame.Rect(50, 50, 100, 100)

    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

        if not game_over:
            key_press = pygame.key.get_pressed()

            time += 1

            # if controller.getLives() == 0:
            #     game_over = True
            #     controller.reset()

        background.update()
        controller.update()

        time_rect = screen.blit(score_font.render(f"{time}", True, (255, 255, 255)),
                                (screen.get_width()-time_rect.width-100, 20))

        if game_over:
            screen.blit(game_over_font.render("GAME OVER", True, (255, 255, 255)), (300, 50))
            screen.blit(game_over_font.render("Click anywhere to restart", True, (255, 255, 255)), (200, 300))

        pygame.display.update()


if __name__ == "__main__":

    pygame.init()
    pygame.display.set_caption("Tank Game")
    pygame.display.set_icon( pygame.image.load(assets.PLAYER_TANK))

    screen = pygame.display.set_mode((900, 700))

    running = True

    controller = Controller(screen)

    background = bg.Background(assets.BACKGROUND, screen, (-5, -5))
    bg_rect = background.getRect()

    split = (20, 20)

    backg_wall = bg.BackgroundWall(assets.BACKGROUND_WALL1, screen, (0, 0), split=split)
    wall_coll1 = backg_wall.getCollisionObject()

    backg_wall2 = bg.BackgroundWall(assets.BACKGROUND_WALL2, screen, split=split)
    rect = backg_wall2.get_rect()
    backg_wall2.setPos(bg_rect.width - rect.width, 0)
    wall_coll2 = backg_wall2.getCollisionObject()

    backg_wall3 = bg.BackgroundWall(assets.BACKGROUND_WALL3, screen, split=split)
    rect = backg_wall3.get_rect()
    backg_wall3.setPos(0, bg_rect.height - rect.height)
    wall_coll3 = backg_wall3.getCollisionObject()

    backg_wall4 = bg.BackgroundWall(assets.BACKGROUND_WALL4, screen, split=split)
    rect = backg_wall4.get_rect()
    backg_wall4.setPos(bg_rect.width - rect.width, bg_rect.height - rect.height)
    wall_coll4 = backg_wall4.getCollisionObject()

    backg_wall5 = bg.BackgroundWall(assets.BACKGROUND_WALL5, screen, split=split)
    backg_wall5.setPos(400, 400)
    wall_coll5 = backg_wall5.getCollisionObject()

    backg_wall6 = bg.BackgroundWall(assets.BACKGROUND_WALL6, screen, split=split)
    backg_wall6.setPos(500, 150)
    wall_coll6 = backg_wall6.getCollisionObject()

    for wall in [(backg_wall, wall_coll1), (backg_wall2, wall_coll2), (backg_wall3, wall_coll3),
                 (backg_wall4, wall_coll4), (backg_wall5, wall_coll5), (backg_wall6, wall_coll6)]:
        controller.addObstacle(*wall)

    spawn_lst = [(650, 120), (250, 450), (650, 450)]

    controller.setSpawnlst(spawn_lst)  # XXX to go?

    controller.addBot(entities.Bot(
        next_action=algo.RandomAlgo(), 
        pos=spawn_lst[0], 
        screen=screen, 
        img_path=assets.ENEMY_TANK,
        controller=controller, 
        speed=0, 
        fire_speed=0.5,
        fire_delay=450, fire_radius=150,
    ))

    controller.addBot(entities.Bot(
        next_action=algo.RandomAlgo(), 
        pos=spawn_lst[1], 
        screen=screen, 
        img_path=assets.ENEMY_TANK,
        controller=controller, 
        speed=0, 
        fire_speed=0.5,
        fire_delay=450, fire_radius=150,
    ))

    game_over_font = pygame.font.SysFont('Times', 50, True)
    score_font = pygame.font.SysFont('Consolas', 30)
    main()
