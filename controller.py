import math

from entities import Bullet


class Controller:
    bots = set()
    bullets = set()
    screen = None
    obstacles = set()
    bg_x, bg_y = (0, 0)  # background position
    prev_bg_x, prev_bg_y = (0, 0)  # previous background position

    def __init__(self, screen, spawn_pos=None):
        if spawn_pos is None:
            spawn_pos = []

        self.screen = screen
        self.spawn_lst = spawn_pos

    def addObstacle(self, obstacle, collidObj):
        self.obstacles.add((obstacle, collidObj))

    def addBot(self, bot):
        self.bots.add(bot)

    def createBullet(self, bot, radius, speed):
        normal = (math.cos(math.radians(bot.angle + 90)), 
                 math.sin(math.radians(bot.angle - 90)))
        bullet = Bullet(self.screen, bot, normal, bot.center(), bot.angle, radius, speed)
        self.bullets.add(bullet)

    def updateBots(self):
        for bot in self.bots:
            bot.update(other_bots=[b for b in self.bots if b!=bot])

    def updateObstacles(self):
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
                if collid.rect_collide(bullet.getBbox())[0]:
                    self.bullets.remove(bullet)
                    break

        # XXX optimise
        for bot in self.bots:
            collid_count = 0
            for _, collid in self.obstacles:
                if collid.rect_collide(
                        bot.getBbox())[0] or not (
                        100 <= bot.pos_x <= 800 and 100 <= bot.pos_y <= 600):
                    collid_count += 1

            # XXX adjust for bot to bot collisions
            # if self.player.colliderect(enemy.getRectObject()):
                # self.player.resetPreviousPos()
                # enemy.resetPreviousPos()

            if collid_count > 0:
                bot.resetPreviousPos()
                bot.speed = 0
                bot.setCollision(True)

        for bullet in self.bullets.copy():
            for bot in self.bots.copy():
                if bot.colliderect(bullet.getRect()) and bullet.owner is not bot:
                    self.bots.remove(bot)
                    self.bullets.remove(bullet)
                    break

    def update(self):
        self.updateObstacles()
        self.updateBots()
        self.update_bullets()
        self.check_collisions()

    def setSpawnlst(self, spawnlst):
        self.spawn_lst = spawnlst

    def reset(self):
        self.bots = set()
        self.bullets = set()
