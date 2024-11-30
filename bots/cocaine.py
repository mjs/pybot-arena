import random

from bot import Bot, CurrentState, Action, SetSpeed, SetAngle, Fire


class CocaineBear(Bot):

    def __init__(self):
        self.queue = [
            SetAngle(random.random() * 360),
            SetSpeed(0.5),
        ]

    def cocaine_rampage(self, state) -> Action | None:
        if state.collision:
            self.queue = []
            return SetAngle(random.random() * 360)
        if self.queue:
            return self.queue.pop(0)

        if state.nearby_bots and state.can_fire:
            frenemy = state.nearby_bots[0]
            if abs(state.angle - frenemy.relative_angle) > 5:
                self.queue.append(SetAngle(frenemy.relative_angle))
            self.queue.append(Fire())
            self.queue.append(SetAngle((state.angle + 180) % 360))

    def next(self, state: CurrentState) -> Action | None:
        return self.cocaine_rampage(state)

    def default_name(self):
        return "cocaine_bear"

    def default_color(self):
        return "white"
