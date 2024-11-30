import random
import stat

from bot import Action, Bot, CurrentState, Fire, SetAngle, SetSpeed


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

        if state.nearby_bots:
            if state.speed != 0.1:
                return SetSpeed(0.1)
            first = state.nearby_bots[0]
            if state.can_fire and abs(state.angle - first.relative_angle) < 2:
                return Fire()
            return SetAngle(first.relative_angle)

        if state.speed != 0.5:
            self.queue = [
                SetSpeed(0.5),
            ]
            return SetAngle(random.random() * 360)


class Advanced(Bot):
    def __init__(self):
        self.queue = [
            SetAngle(random.random() * 360),
            SetSpeed(0.5),
        ]

    def default_name(self):
        return "advanced"

    def default_color(self):
        return "palegreen"

    def next(self, state: CurrentState) -> Action | None:
        if state.collision:
            self.queue = []
            self.queue.append(SetAngle(state.angle + 10))
            self.queue.append(SetSpeed(1.0))
            return self.queue.pop(0)

        if self.queue:
            return self.queue.pop(0)

        if state.nearby_bots and not state.nearby_bullets and not state.collision:
            first = state.nearby_bots[0]
            print(f"I smell victory {first.distance}")
            if abs(state.angle - first.relative_angle) > 2:
                self.queue.append(SetAngle(first.relative_angle))
            if state.speed <= 1.0:
                self.queue.append(SetSpeed(1.0))
            if (
                state.can_fire
                and abs(state.angle - first.relative_angle) < 2
                and first.distance < 60
            ):
                self.queue.append(Fire())
                self.queue.append(SetAngle(state.angle + 60))
                self.queue.append(SetSpeed(-1.0))
            return self.queue.pop(0)

        if state.nearby_bullets and not state.collision:
            first = state.nearby_bullets[0]
            print(f"Oh no bullets at {first.distance}")
            if first.distance > 150:
                if state.speed <= 0.1:
                    self.queue.append(SetSpeed(1.0))
                else:
                    self.queue.append(SetSpeed(state.speed - 0.1))
            self.queue.append(SetAngle(first.relative_angle + 60))
            return self.queue.pop(0)

        if state.speed != 0.5:
            self.queue = [
                SetSpeed(0.5),
            ]
            return SetAngle(random.random() * 360)
