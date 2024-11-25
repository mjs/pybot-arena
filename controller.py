import math
import structlog

from entities import Bullet


log = structlog.get_logger()


class Controller:
    tanks = set()
    bullets = set()
    screen = None
    obstacles = set()
    bg_x, bg_y = (0, 0)  # background position
    prev_bg_x, prev_bg_y = (0, 0)  # previous background position

    def __init__(self, screen):
        self.screen = screen

    def add_obstacle(self, obstacle, collidObj):
        self.obstacles.add((obstacle, collidObj))

    def add_tank(self, tank):
        self.tanks.add(tank)

    def create_bullet(self, tank, radius, speed):
        normal = (
            math.cos(math.radians(tank.angle + 90)),
            math.sin(math.radians(tank.angle - 90)),
        )
        bullet = Bullet(
            self.screen, tank, normal, tank.center, tank.angle, radius, speed
        )
        self.bullets.add(bullet)

    def update_tanks(self):
        for tank in self.tanks:
            tank.update(others=[t for t in self.tanks if t != tank])

    def update_obstacles(self):
        for obs, _ in self.obstacles:
            obs.update()

    def update_bullets(self):
        for bullet in self.bullets.copy():
            bullet.update()
            if bullet.destroyed():
                self.bullets.remove(bullet)

    def check_collisions(self):
        for bullet in self.bullets.copy():
            for _, collid in self.obstacles:
                if collid.rect_collide(bullet.get_bbox())[0]:
                    self.bullets.remove(bullet)
                    break

        # XXX optimise
        for tank in self.tanks:
            collid_count = 0
            for _, collid in self.obstacles:
                if collid.rect_collide(tank.get_bbox())[0] or not (
                    100 <= tank.pos_x <= 800 and 100 <= tank.pos_y <= 600
                ):
                    collid_count += 1

            # XXX adjust for tank to tank collisions
            # if self.player.colliderect(enemy.getRectObject()):
            # self.player.reset_previous_pos()
            # enemy.reset_previous_pos()

            if collid_count > 0:
                tank.reset_previous_pos()
                tank.set_collision(True)

        for bullet in self.bullets.copy():
            for tank in self.tanks.copy():
                if tank.colliderect(bullet.get_rect()) and bullet.owner is not tank:
                    log.info("Tank destroyed", name=tank.name, by=bullet.owner.name)
                    self.tanks.remove(tank)
                    self.bullets.remove(bullet)
                    break

    def update(self):
        self.update_obstacles()
        self.update_tanks()
        self.update_bullets()
        self.check_collisions()

    def reset(self):
        self.tanks = set()
        self.bullets = set()
