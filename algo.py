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
    collision: bool   # XXX maybe don't keep this
    nearby: list[NearbyBot]

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


class Algo(ABC):

    def name(self) -> str:
        raise NotImplementedError

    def next(self, state: CurrentState) -> Action | None:
        raise NotImplementedError


# XXX firing bullets
# XXX color per bot
# XXX ensure unique names
# XXX fuel? 


# XXX move these out

class RandomAlgo(Algo):

    def name(self):
        return "random"

    def next(self, state: CurrentState) -> Action | None:
        if state.collision:
            return SetAngle(random.random() * 360)
        if state.speed == 0:
            return SetSpeed((random.random() * 2) - 1)
        return None


# XXX rename
class HeadlightsAlgo(Algo):
    def __init__(self):
        self.queue = [
            SetAngle(random.random() * 360),
            SetSpeed(0.5),
        ]

    def name(self):
        return "test"

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
            return SetAngle(first.relative_angle)

        if state.speed != 0.5:
            self.queue = [
                SetSpeed(0.5),
            ]
            return SetAngle(random.random() * 360)
