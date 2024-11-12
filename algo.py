from dataclasses import dataclass

@dataclass
class CurrentState:
    ticks: int
    speed: float
    angle: float
    collision: bool


@dataclass
class Action:
    speed: int
    angle: int


import random

class RandomAlgo:
    def __init__(self):
        self.speed = random.random() * 2 
        self.angle = random.random() * 360

    def __call__(self, state):
        if state.collision:
            self.speed = (random.random() * 2) - 1
            self.angle = random.random() * 360
        return Action(speed=self.speed, angle=self.angle)
