import random

from bot import Bot, CurrentState, Action, SetSpeed, SetAngle, Fire


class Random(Bot):

    def default_name(self):
        return "random"

    def default_color(self):
        return "palegreen"

    def next(self, state: CurrentState) -> Action | None:
        if state.collision:
            return SetAngle(random.random() * 360)
        if state.speed == 0:
            return SetSpeed((random.random() * 2) - 1)
        if random.random() < 0.1:
            return Fire()
        return None


class Basic(Bot):
    def __init__(self):
        self.queue = [
            SetAngle(random.random() * 360),
            SetSpeed(0.5),
        ]

    def default_name(self):
        return "basic"

    def default_color(self):
        return "firebrick"

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
