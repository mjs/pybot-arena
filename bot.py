import random
import pygame
from dataclasses import dataclass


@dataclass
class NearbyBot:
    name: str
    # XXX maybe don't need these
    x: float
    y: float
    # XXX distance
    relative_angle: float
    speed: float
    angle: float


@dataclass
class CurrentState:
    ticks: int
    x: float
    y: float
    speed: float
    angle: float
    # XXX fire_delay time
    collision: bool  # XXX maybe don't keep this
    nearby: list[NearbyBot]
    # XXX also report nearby bullets to allow avoidance
    # XXX also report nearby walls to allow for smarter avoidance?


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


# XXX color per bot
# XXX show n
# XXX fuel?
