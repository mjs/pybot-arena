import random

from bot import Bot, CurrentState, Action, SetSpeed, SetAngle, Fire


class Menno(Bot):
    def __init__(self):
        self.queue = [
            SetAngle(random.random() * 360),
            SetSpeed(0.5),
        ]
        self.next_eval_ticks = 0
        self.attacking = False

    def default_name(self):
        return "menno"

    def default_color(self):
        return "black"

    def next(self, state: CurrentState) -> Action | None:
        if state.collision:
            return SetAngle(state.angle + random.randint(10, 110))

        if state.ticks - self.next_eval_ticks > 500:
            self.next_eval_ticks = state.ticks

            if any(b.distance < 150 for b in state.nearby_bullets):
                self.attacking = False
                self.queue = [
                    SetAngle(state.angle + 10 + (random.random() * 20)),
                    SetSpeed(-0.5),
                ]
            elif any(b.distance < 100 for b in state.nearby_bots):
                self.attacking = False
                self.queue = [
                    SetAngle(state.angle - 90),
                    SetSpeed(0.5),
                ]
            elif state.nearby_bots:
                self.attacking = True
                self.queue = [
                    SetSpeed(0.2),
                ]
            else:
                self.attacking = False
                self.queue = [
                    SetSpeed(0.3),
                ]

        if self.queue:
            return self.queue.pop(0)

        if self.attacking:
            if state.nearby_bots:
                first = state.nearby_bots[0]
                if (
                    state.can_fire
                    and abs(state.angle - first.relative_angle) < 2
                    and first.distance < 150
                ):
                    return Fire()
                return SetAngle(first.relative_angle)
            else:
                self.attacking = False
                self.queue = [SetAngle(random.random() * 360)]
                return SetSpeed(0.3)
