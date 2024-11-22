import pygame
from pycollision import Collision


class Background:

    def __init__(self, img: str, screen, pos=(0, 0)):
        self.bg_image = pygame.image.load(img).convert_alpha()
        self.bg_x, self.bg_y = pos
        self.screen = screen

    def update(self):
        self.screen.blit(self.bg_image, (self.bg_x, self.bg_y))

    def get_pos(self):
        return self.bg_x, self.bg_y

    def get_rect(self):
        return self.bg_image.get_rect()


class BackgroundWall:

    def __init__(self, img: str, screen, pos=(0, 0), split=(5, 5)):
        self.img = pygame.image.load(img).convert_alpha()
        self.x, self.y = pos
        self.screen = screen
        self.collision = Collision(
            img, split, wall_collision=True, wall_padding=(1, 1, 1, 1)
        )

    def set_pos(self, x, y):
        self.x, self.y = x, y
        self.collision.setSpritePos(self.x, self.y)

    def update(self):
        self.screen.blit(self.img, (self.x, self.y))

    def get_collision_object(self):
        return self.collision

    def get_rect(self) -> pygame.Rect:
        return self.img.get_rect()
