import math

from entities import Bullet


class Controller:
    bots = set()
    bullets = set()
    screen = None
    obstacles = set()
    bg_x, bg_y = (0, 0)  # background position
    prev_bg_x, prev_bg_y = (0, 0)  # previous background position

    def __init__(self, screen):
        self.screen = screen

    def add_obstacle(self, obstacle, collidObj):
        self.obstacles.add((obstacle, collidObj))

    def add_bot(self, bot):
        self.bots.add(bot)

    def create_bullet(self, bot, radius, speed):
        normal = (
            math.cos(math.radians(bot.angle + 90)),
            math.sin(math.radians(bot.angle - 90)),
        )
        bullet = Bullet(
            self.screen, bot, normal, bot.center(), bot.angle, radius, speed
        )
        self.bullets.add(bullet)

    def update_bots(self):
        for bot in self.bots:
            bot.update(other_bots=[b for b in self.bots if b != bot])

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
        for bot in self.bots:
            collid_count = 0
            for _, collid in self.obstacles:
                if collid.rect_collide(bot.get_bbox())[0] or not (
                    100 <= bot.pos_x <= 800 and 100 <= bot.pos_y <= 600
                ):
                    collid_count += 1

            # XXX adjust for bot to bot collisions
            # if self.player.colliderect(enemy.getRectObject()):
            # self.player.reset_previous_pos()
            # enemy.reset_previous_pos()

            if collid_count > 0:
                bot.reset_previous_pos()
                bot.speed = 0
                bot.set_collision(True)

        for bullet in self.bullets.copy():
            for bot in self.bots.copy():
                if bot.colliderect(bullet.get_rect()) and bullet.owner is not bot:
                    # XXX who killed who, eventually on screen
                    # XXX explosions
                    self.bots.remove(bot)
                    self.bullets.remove(bullet)
                    break

    def update(self):
        self.update_obstacles()
        self.update_bots()
        self.update_bullets()
        self.check_collisions()

    def reset(self):
        self.bots = set()
        self.bullets = set()
