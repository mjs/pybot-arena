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


class Algo:

    def name(self) -> str:
        raise NotImplementedError

    def colour(self):
        return pygame.Color(255, 255, 255, 255)

    def next(self, state: CurrentState) -> Action | None:
        raise NotImplementedError


# XXX color per bot
# XXX ensure unique names
# XXX fuel?


# XXX move these out


class RandomAlgo(Algo):

    def name(self):
        return "random"

    def colour(self):
        return pygame.Color(255, 255, 255, 255)

    def next(self, state: CurrentState) -> Action | None:
        if state.collision:
            return SetAngle(random.random() * 360)
        if state.speed == 0:
            return SetSpeed((random.random() * 2) - 1)
        if random.random() < 0.1:
            return Fire()
        return None


# XXX rename
class HeadlightsAlgo(Algo):
    def __init__(self):
        self.queue = [
            SetAngle(random.random() * 360),
            SetSpeed(0.5),
        ]

    # XXX maybe should be set on command line
    def name(self):
        return "test"

    # XXX maybe should be set on command line or randomly assigned
    def colour(self):
        return pygame.Color(0, 255, 255, 255)

    def next(self, state: CurrentState) -> Action | None:
        if state.collision:
            self.queue = []
            return SetAngle(random.random() * 360)
        if self.queue:
            return self.queue.pop(0)

        if state.nearby:
            if state.speed != 0.1:
                return SetSpeed(0.1)
            first = state.nearby[0]
            if abs(state.angle - first.relative_angle) < 1:
                return Fire()
            return SetAngle(first.relative_angle)

        if state.speed != 0.5:
            self.queue = [
                SetSpeed(0.5),
            ]
            return SetAngle(random.random() * 360)
