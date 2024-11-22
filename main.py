import importlib
import sys
from dataclasses import dataclass

import pygame

from bot import Bot
from controller import Controller
import assets
import background as bg
import entities

SPAWN_POINTS = [(200, 200), (650, 120), (250, 450), (650, 450), (500, 350)]


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

            # XXX stop game and announce winner when one is left
            # if controller.getLives() == 0:
            #     game_over = True
            #     controller.reset()

        background.update()
        controller.update()

        time_rect = screen.blit(
            score_font.render(f"{time}", True, (255, 255, 255)),
            (screen.get_width() - time_rect.width - 100, 20),
        )

        if game_over:
            screen.blit(
                game_over_font.render("GAME OVER", True, (255, 255, 255)), (300, 50)
            )
            screen.blit(
                game_over_font.render(
                    "Click anywhere to restart", True, (255, 255, 255)
                ),
                (200, 300),
            )

        pygame.display.update()


@dataclass
class TankSpec:
    bot: Bot
    name: str
    color_name: str


def parse_tank_specs(args: list[str]) -> list[TankSpec]:
    """Parse the tank details from the command line.

    Each arg takes the form: <package.BotClass>[,name,[color]]
    """
    specs = []
    for arg in args:
        parts = iter(arg.split(","))
        bot = load_bot(next(parts))
        name = bot.default_name()
        color_name = bot.default_color()

        try:
            name = next(parts)
            color_name = next(parts)
        except StopIteration:
            pass

        specs.append(TankSpec(bot, name, color_name))
    return specs


def load_bot(source) -> "Bot":
    module_name, bot_name = source.rsplit(".", -1)
    mod = importlib.import_module(module_name)
    cls = getattr(mod, bot_name)
    return cls()


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Tank Game")
    pygame.display.set_icon(pygame.image.load(assets.PLAYER_TANK))

    screen = pygame.display.set_mode((900, 700))

    running = True

    controller = Controller(screen)

    background = bg.Background(assets.BACKGROUND, screen, (-5, -5))
    bg_rect = background.get_rect()

    split = (20, 20)

    backg_wall = bg.BackgroundWall(assets.BACKGROUND_WALL1, screen, (0, 0), split=split)
    wall_coll1 = backg_wall.get_collision_object()

    backg_wall2 = bg.BackgroundWall(assets.BACKGROUND_WALL2, screen, split=split)
    rect = backg_wall2.get_rect()
    backg_wall2.set_pos(bg_rect.width - rect.width, 0)
    wall_coll2 = backg_wall2.get_collision_object()

    backg_wall3 = bg.BackgroundWall(assets.BACKGROUND_WALL3, screen, split=split)
    rect = backg_wall3.get_rect()
    backg_wall3.set_pos(0, bg_rect.height - rect.height)
    wall_coll3 = backg_wall3.get_collision_object()

    backg_wall4 = bg.BackgroundWall(assets.BACKGROUND_WALL4, screen, split=split)
    rect = backg_wall4.get_rect()
    backg_wall4.set_pos(bg_rect.width - rect.width, bg_rect.height - rect.height)
    wall_coll4 = backg_wall4.get_collision_object()

    backg_wall5 = bg.BackgroundWall(assets.BACKGROUND_WALL5, screen, split=split)
    backg_wall5.set_pos(400, 400)
    wall_coll5 = backg_wall5.get_collision_object()

    backg_wall6 = bg.BackgroundWall(assets.BACKGROUND_WALL6, screen, split=split)
    backg_wall6.set_pos(500, 150)
    wall_coll6 = backg_wall6.get_collision_object()

    for wall in [
        (backg_wall, wall_coll1),
        (backg_wall2, wall_coll2),
        (backg_wall3, wall_coll3),
        (backg_wall4, wall_coll4),
        (backg_wall5, wall_coll5),
        (backg_wall6, wall_coll6),
    ]:
        controller.add_obstacle(*wall)

    # XXX try for grayscale bots which color more easily

    spawn_points = iter(SPAWN_POINTS)

    specs = parse_tank_specs(sys.argv[1:])
    # XXX ensure unique names
    # XXX exit with error if number of bots exceeds spawn points
    for spec in specs:
        controller.add_tank(
            entities.Tank(
                bot=spec.bot,
                name=spec.name,
                color=pygame.Color(spec.color_name),
                pos=next(spawn_points),
                screen=screen,
                img_path=assets.PLAYER_TANK,
                controller=controller,
            )
        )

    game_over_font = pygame.font.SysFont("Times", 50, True)
    score_font = pygame.font.SysFont("Consolas", 30)

    # XXX show the tank names and their colors around the edges
    main()
