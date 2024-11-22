import random
import pygame
from dataclasses import dataclass


@dataclass
class NearbyBot:
    name: str
    x: float
    y: float
    distance: float
    speed: float
    angle: float
    relative_angle: float


@dataclass
class NearbyBullet:
    x: float
    y: float
    distance: float
    angle: float
    relative_angle: float


@dataclass
class CurrentState:
    ticks: int
    x: float
    y: float
    speed: float
    angle: float
    collision: bool
    nearby_bots: list[NearbyBot]
    nearby_bullets: list[NearbyBullet]
    can_fire: bool


class Action:
    pass


@dataclass
class SetAngle(Action):
    angle: float


@dataclass
class SetSpeed(Action):
    speed: float


@dataclass
class Fire(Action):
    pass


class Bot:

    def default_name(self) -> str:
        raise NotImplementedError

    def default_color(self) -> str:
        return "white"

    def next(self, state: CurrentState) -> Action | None:
        raise NotImplementedError
