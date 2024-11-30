import random

from bot import Bot, CurrentState, Action, SetSpeed, SetAngle, Fire


class Aidie8Bot(Bot):

    def __init__(self):
        self.queue = [
            SetSpeed(1)
        ]

    def default_name(self):
        return "Aidie8_Bot"

    def default_color(self):
        return "blue"


    def next(self, state: CurrentState) -> Action | None:
        if state.collision:
            self.queue = []
            return SetAngle(random.random() * 360)
        if self.queue:
            return self.queue.pop(0)
        if state.nearby_bullets:
            closestbullet = state.nearby_bullets[0]
            for bullet in state.nearby_bullets:
                if bullet.distance < closestbullet.distance:
                    closestbullet = bullet

            angleAwayfromBullet = closestbullet.relative_angle - state.angle
            self.queue += [SetAngle(-angleAwayfromBullet)]
            return SetSpeed(1)
        if state.nearby_bots:
            first = state.nearby_bots[0]
            if first.distance < 6:
                self.queue += [SetSpeed(0.5)]
                return SetAngle(first.relative_angle + 30)
            if abs(first.relative_angle - state.angle) < 20 and state.speed > 0.5:
                self.queue += [SetSpeed(state.speed * -1)]
                return SetAngle(state.angle + 30)
            if state.can_fire and abs(state.angle - first.relative_angle) < 2:
                return Fire()




