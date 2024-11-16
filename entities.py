import random

import pygame
import math
from typing import Tuple
from algo import Algo, CurrentState, NearbyBot, SetAngle, SetSpeed, Fire
import assets

# XXX collapse Tank and Bot

class Tank:

    def __init__(
            self,
            img_path: str,
            screen,
            pos,
            controller,
            speed: float = 0.5,
            fire_radius: int = 250,
            fire_delay: int = 500,
            fire_speed=0.5):

        self.screen = screen
        self.pos_x, self.pos_y = pos
        self.speed = speed
        self.angle = 0
        self._fired = False
        self.fire_speed = fire_speed
        self.fire_delay = fire_delay
        self.time_counter = fire_delay
        self.controller = controller

        self.tank_image = pygame.image.load(img_path).convert_alpha()

        self.transformed_image = self.tank_image
        self._rect = self.tank_image.get_rect()

        self.previous_x, self.previous_y = pos
        self.fire_radius = fire_radius

    def center(self) -> Tuple[int, int]:
        return self.tank_image.get_rect(center=(self.pos_x, self.pos_y)).center

    def _calcAdjHyp(self, pos):
        mouse_x, mouse_y = pos
        center_x, center_y = self.center()

        adj = mouse_x - center_x
        opp = mouse_y - center_y

        hyp = math.hypot(adj, opp)

        return adj, opp, hyp

    def _calcAngle(self, pos):
        """ calculates angle towards a point """
        adj, opp, hyp = self._calcAdjHyp(pos)
        if hyp == 0:
            hyp = 1
        nx, ny = adj / hyp, opp / hyp  # normalize
        return math.degrees(math.atan2(-nx, -ny))

    def fire(self):
        if not self._fired:
            self._fired = True
            self.controller.createBullet(self, self.fire_radius, self.fire_speed)

    def getBbox(self):
        # XXX
        # rect = self.transformed_image.get_rect(center=(self.pos_x, self.pos_y))
        rect = self.tank_image.get_rect(center=(self.pos_x, self.pos_y))
        return rect[0], rect[1], rect[0] + rect[2], rect[1] + rect[3]

    def getRectObject(self):
        return self.transformed_image.get_rect(center=(self.pos_x, self.pos_y))

    def resetPreviousPos(self):
        self.pos_x, self.pos_y = self.previous_x, self.previous_y

    def pos(self) -> Tuple[float, float]:
        return self._rect[:2]

    def update(self):
        self.screen.blit(self.transformed_image, self._rect)
        # XXX tidy
        if self.time_counter > 0:
            self.time_counter -= 1

        else:
            self.time_counter = self.fire_delay
            self._fired = False

    def colliderect(self, rect):
        return self.getRectObject().colliderect(rect)

    def collidelist(self, lst):
        return self.getRectObject().collidelist(lst)

    def setPos(self, pos):
        self.pos_x, self.pos_y = pos

    def in_circle(self, x, y, radius):
        center_x, center_y = self.center()
        dist = (center_x - x) ** 2 + (center_y - y) ** 2
        return dist < radius**2


class Bot(Tank):

    def __init__(self, algo: Algo, *args, detection_radius: float=200, **kwargs):
        super().__init__(*args, **kwargs)
        self.algo = algo
        self.detection_radius = detection_radius
        self.collision = False

    def update(self, other_bots: list['Bot']):
        state = CurrentState(
            ticks=pygame.time.get_ticks(),
            x=self.pos_x,
            y=self.pos_y,
            speed=self.speed,
            angle=self.angle,
            collision=self.collision,
            nearby = [
                NearbyBot(
                    name=other.algo.name(),
                    x=other.pos_x,
                    y=other.pos_y,
                    relative_angle=self._calcAngle(other.center()),
                    speed=other.speed,
                    angle=other.angle,
                )
                for other in other_bots
                if self.in_circle(other.pos_x, other.pos_y, self.detection_radius)
            ]
        )
        self.collision = False

        action = self.algo.next(state)

        typ = type(action)
        if typ is SetSpeed:
            self.speed = action.speed
            self.speed = min(self.speed, 0.5)
            self.speed = max(self.speed, -0.5)
        elif typ is SetAngle:
            # XXX limit allowed angle change 
            self.angle = action.angle
            self.angle = min(self.angle, 360)
            self.angle = max(self.angle, 0)
        elif typ is Fire:
            self.fire()

        direction_x = math.cos(math.radians(self.angle + 90)) * self.speed
        direction_y = math.sin(math.radians(self.angle - 90)) * self.speed

        self.transformed_image = pygame.transform.rotate(
            self.tank_image, self.angle)
        self.previous_x, self.previous_y = self.pos_x, self.pos_y
        self.pos_x = direction_x + self.pos_x
        self.pos_y = direction_y + self.pos_y

        self._rect = self.transformed_image.get_rect(
            center=(self.pos_x, self.pos_y))

        super().update()

    def setCollision(self, collid: bool):
        self.collision = collid


class Bullet:

    def __init__(
            self,
            screen,
            owner,
            normal,
            initial_pos,
            angle,
            fire_radius: int,
            speed: float = 0.5):
        self.screen = screen
        self._destroyed = False
        self.bullet_image = pygame.image.load(assets.BULLET).convert_alpha()
        self.transformed_img = self.bullet_image
        self.owner = owner
        self._fire_radius = fire_radius

        self.normal = normal[0] * speed, normal[1] * speed
        self._initial_pos = initial_pos

        rect = self.transformed_img.get_rect()
        self.current_pos = initial_pos[0] - rect.centerx, initial_pos[1] - rect.centery

        self.transformed_img = pygame.transform.rotate(
            self.bullet_image, angle)

    def update(self):
        self.current_pos = ((self.normal[0] + self.current_pos[0]),
                            (self.normal[1] + self.current_pos[1]))

        if self.dist() >= self._fire_radius:
            self._destroyed = True

        self.screen.blit(self.transformed_img, self.current_pos)

    def dist(self):
        return math.hypot(
            (self.current_pos[0] - self._initial_pos[0]),
            (self.current_pos[1] - self._initial_pos[1]))

    def destroyed(self):
        return self._destroyed

    def getRect(self):
        return self.transformed_img.get_rect(center=(self.current_pos))

    def colliderect(self, rect):
        return self.getRect().colliderect(rect)

    def collidelist(self, lst):
        return self.getRect().collidelist(lst)

    def getBbox(self):
        rect = self.transformed_img.get_rect(center=self.current_pos)
        return rect[0], rect[1], rect[0] + rect[2], rect[1] + rect[3]
