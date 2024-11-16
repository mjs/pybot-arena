import random
from abc import ABC
from dataclasses import dataclass

@dataclass
class NearbyBot:
    name: str
    x: float
    y: float
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
    collision: bool
    nearby: list[NearbyBot]

@dataclass
class Action:
    speed: float | None
    angle: float | None


class Algo(ABC):

    def name(self) -> str:
        raise NotImplementedError

    def next(self, state: CurrentState) -> Action:
        raise NotImplementedError


# XXX firing bullets
# XXX color per bot
# XXX ensure unique names


# XXX move these out

class RandomAlgo(Algo):
    def __init__(self):
        self.speed = random.random() * 2
        self.angle = random.random() * 360

    def name(self):
        return "random"

    def next(self, state: CurrentState) -> Action:
        if state.collision:
            self.speed = (random.random() * 2) - 1
            self.angle = random.random() * 360
        return Action(speed=self.speed, angle=self.angle)


class HeadlightsAlgo(Algo):
    def __init__(self):
        self.speed = 0.5
        self.angle = random.random() * 360

    def name(self):
        return "test"

    def next(self, state: CurrentState) -> Action:
        if state.nearby:
            return Action(speed=0.1, angle=state.nearby[0].relative_angle)
        if state.collision:
            self.angle = random.random() * 360
        return Action(speed=self.speed, angle=self.angle)
