import math
from typing import Tuple

import pygame

import assets
import bot


class Tank:

    def __init__(
        self,
        bot: bot.Bot,
        name: str,
        color: pygame.Color,
        img_path: str,
        screen,
        pos,
        controller,
        fire_speed=0.6,
        fire_radius: int = 150,
        reload_delay: int = 1000,
        visibility: float = 250,
    ):
        self.bot = bot
        self.name = name
        self.screen = screen
        self.pos_x, self.pos_y = pos
        self.speed = 0
        self.angle = 0
        self.fire_speed = fire_speed
        self.reload_delay = reload_delay
        self.reload_counter = reload_delay
        self.controller = controller
        self.visibility = visibility

        # Load image and apply color
        # XXX try gray scaling it first
        self.tank_image = pygame.image.load(img_path).convert_alpha()
        mask = pygame.Surface(self.tank_image.get_size()).convert_alpha()
        mask.fill(color)
        self.tank_image.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        self.transformed_image = self.tank_image
        self._rect = self.tank_image.get_rect()

        self.previous_x, self.previous_y = pos
        self.fire_radius = fire_radius

        self._fired = False
        self.collision = False

    @property
    def center(self) -> Tuple[int, int]:
        return self.tank_image.get_rect(center=(self.pos_x, self.pos_y)).center

    def _calc_adj_hyp(self, pos):
        mouse_x, mouse_y = pos
        center_x, center_y = self.center

        adj = mouse_x - center_x
        opp = mouse_y - center_y

        hyp = math.hypot(adj, opp)

        return adj, opp, hyp

    def _calc_angle(self, pos):
        """calculates angle towards a point"""
        adj, opp, hyp = self._calc_adj_hyp(pos)
        if hyp == 0:
            hyp = 1
        nx, ny = adj / hyp, opp / hyp  # normalize
        return math.degrees(math.atan2(-nx, -ny))

    def fire(self):
        if not self._fired:
            self._fired = True
            self.controller.create_bullet(self, self.fire_radius, self.fire_speed)

    def get_bbox(self):
        rect = self.transformed_image.get_rect(center=(self.pos_x, self.pos_y))
        return rect[0], rect[1], rect[0] + rect[2], rect[1] + rect[3]

    def get_rect_object(self):
        return self.transformed_image.get_rect(center=(self.pos_x, self.pos_y))

    def reset_previous_pos(self):
        self.pos_x, self.pos_y = self.previous_x, self.previous_y

    def pos(self) -> Tuple[float, float]:
        return self._rect[:2]

    def update(self, others: list["Tank"]):
        state = bot.CurrentState(
            ticks=pygame.time.get_ticks(),
            x=self.pos_x,
            y=self.pos_y,
            speed=self.speed,
            angle=self.angle,
            collision=self.collision,
            can_fire=not self._fired,
            nearby_bots=[
                bot.NearbyBot(
                    name=other.name,
                    x=other.pos_x,
                    y=other.pos_y,
                    distance=dist(self.center, other.center),
                    speed=other.speed,
                    angle=other.angle,
                    relative_angle=norm_angle(self._calc_angle(other.center)),
                )
                for other in others
                if self.in_circle(other.pos_x, other.pos_y, self.visibility)
            ],
            nearby_bullets=[
                bot.NearbyBullet(
                    x=bullet.pos_x,
                    y=bullet.pos_y,
                    distance=dist(self.center, bullet.center),
                    speed=bullet.speed,
                    relative_angle=norm_angle(self._calc_angle(bullet.center)),
                    angle=bullet.angle,
                )
                for bullet in self.controller.bullets
                if bullet.owner != self
                and self.in_circle(bullet.pos_x, bullet.pos_y, self.visibility)
            ],
        )
        self.collision = False

        action = self.bot.next(state)

        typ = type(action)
        if typ is bot.SetSpeed:
            self.speed = action.speed
            self.speed = min(self.speed, 0.5)
            self.speed = max(self.speed, -0.5)
        elif typ is bot.SetAngle:
            # XXX limit allowed angle change
            self.angle = norm_angle(action.angle)
        elif typ is bot.Fire:
            self.fire()

        direction_x = math.cos(math.radians(self.angle + 90)) * self.speed
        direction_y = math.sin(math.radians(self.angle - 90)) * self.speed

        self.transformed_image = pygame.transform.rotate(self.tank_image, self.angle)
        self.previous_x, self.previous_y = self.pos_x, self.pos_y
        self.pos_x = direction_x + self.pos_x
        self.pos_y = direction_y + self.pos_y

        self._rect = self.transformed_image.get_rect(center=(self.pos_x, self.pos_y))
        self.screen.blit(self.transformed_image, self._rect)

        if self.reload_counter > 0:
            self.reload_counter -= 1
        else:
            self.reload_counter = self.reload_delay
            self._fired = False

    def colliderect(self, rect):
        return self.get_rect_object().colliderect(rect)

    def in_circle(self, x, y, radius):
        return dist(self.center, (x, y)) < radius

    def set_collision(self, collid: bool):
        self.collision = collid


def dist(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))


def norm_angle(angle):
    while angle >= 360:
        angle -= 360
    while angle < 0:
        angle += 360
    return angle


class Bullet:

    def __init__(
        self,
        screen,
        owner,
        normal,
        initial_pos,
        angle,
        fire_radius: int,
        speed: float = 0.5,
    ):
        self.angle = angle
        self.speed = speed
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

        self.transformed_img = pygame.transform.rotate(self.bullet_image, angle)

    @property
    def pos_x(self):
        return self.current_pos[0]

    @property
    def pos_y(self):
        return self.current_pos[1]

    @property
    def center(self):
        return self.current_pos

    def update(self):
        self.current_pos = (
            (self.normal[0] + self.current_pos[0]),
            (self.normal[1] + self.current_pos[1]),
        )

        if self.dist() >= self._fire_radius:
            self._destroyed = True

        self.screen.blit(self.transformed_img, self.current_pos)

    def dist(self):
        return math.hypot(
            (self.current_pos[0] - self._initial_pos[0]),
            (self.current_pos[1] - self._initial_pos[1]),
        )

    def destroyed(self):
        return self._destroyed

    def get_rect(self):
        return self.transformed_img.get_rect(center=(self.current_pos))

    def colliderect(self, rect):
        return self.get_rect().colliderect(rect)

    def get_bbox(self):
        rect = self.transformed_img.get_rect(center=self.current_pos)
        return rect[0], rect[1], rect[0] + rect[2], rect[1] + rect[3]
