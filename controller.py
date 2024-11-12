import assets
from entities import Bullet, Enemy
from random import choice


class Controller:
    bots = set()
    bullets = set()
    enemies = set()
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

    def createBullet(self, tank_object, normal_pos, fire_pos, angle, radius, speed):
        bullet = Bullet(self.screen, tank_object, normal_pos, fire_pos, angle, radius, speed)
        self.bullets.add(bullet)

    def updateBots(self):
        for bot in self.bots:
            bot.update()

    #XXX to go
    def updateEnemies(self):
        for tank in self.enemies:
            tank.update()

    def updateObstacles(self):
        for obs, _ in self.obstacles:
            obs.update()

    def update_bullets(self):
        bg_x, bg_y = self.bg_x - self.prev_bg_x, self.bg_y - self.prev_bg_y

        for bullet in self.bullets.copy():
            bullet.update((bg_x, bg_y))

            if bullet.destroyed():
                self.bullets.remove(bullet)

    def checkCollision(self):
        for bullet in self.bullets.copy():
            for _, collid in self.obstacles:
                if collid.rect_collide(bullet.getBbox())[0]:
                    self.bullets.remove(bullet)
                    break

        # XXX optimise
        for bot in self.bots:
            collid_count = 0
            for _, collid in self.obstacles:
                if collid.rect_collide(bot.getBbox())[0] or \
                        not (100 <= bot.pos_x <= 800 and 100 <= bot.pos_y <= 600):
                    collid_count += 1

            if collid_count > 0:
                bot.resetPreviousPos()
                bot.speed = 0
                bot.setCollision(True)

        for enemy in self.enemies:
            collid_count = 0
            for _, collid in self.obstacles:
                if collid.rect_collide(enemy.getBbox())[0] or \
                        not (100 <= enemy.pos_x <= 800 and 100 <= enemy.pos_y <= 600):
                    collid_count += 1
                    enemy.change_angle()

            if collid_count > 0:
                enemy.setCollision(True)

            else:
                enemy.setCollision(False)

            # XXX
            #if self.player.colliderect(enemy.getRectObject()):
                #self.player.resetPreviousPos()
                #enemy.resetPreviousPos()

        # XXX
        # for bullet in self.bullets.copy():
        #     for tank in self.enemies.copy():
        #         if bullet.tankObject() == self.player and tank.colliderect(bullet.getRect()):
        #             self.enemies.remove(tank)
        #             self.bullets.remove(bullet)
        #             self.score += 1
        #             break

        #     if bullet.tankObject() != self.player and self.player.colliderect(bullet.getRect()):
        #         self.bullets.remove(bullet)
        #         self.lives -= 1

    def getEnemyCount(self):
        return len(self.enemies)

    def update(self):
        self.update_bullets()
        self.updateObstacles()
        self.updateBots()
        self.updateEnemies()
        self.checkCollision()

    def setSpawnlst(self, spawnlst):
        self.spawn_lst = spawnlst

    def spawnEnemy(self):
        pos = choice(self.spawn_lst)
        enemy = Enemy(follow_radius=200, pos=pos, screen=self.screen, img_path=assets.ENEMY_TANK,
                      controller=self, speed=0.4, fire_speed=0.5,
                      fire_delay=450, fire_radius=150)
        self.enemies.add(enemy)

    def reset(self):
        self.bots = set()
        self.enemies = set()
        self.bullets = set()
