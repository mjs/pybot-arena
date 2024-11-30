from structlog import get_logger
import random
import math
from bot import Bot, CurrentState, Action, SetSpeed, SetAngle, Fire


logger = get_logger()

def normalize_angle(angle):
    return (angle + 180) % 360 - 180

class ImportVictory(Bot):
    def __init__(self):
        self.queue = [
            SetAngle(random.random() * 360),
            SetSpeed(0.5),
            Fire()
        ]

    def default_name(self):
        return "import victory"

    def default_color(self):
        return "aquamarine4"

    def next(self, state: CurrentState) -> Action | None:
        if state.collision:
            self.queue = []
            return SetAngle(random.random() * 360)
        if self.queue:
            # If action is Fire but we cannot fire... go forward or backwards randomly
            # until we can fire
            if isinstance(self.queue[0], Fire) and not state.can_fire:
                # ignore the fire
                self.queue.pop(0)
            else:
                # Apply next action
                return self.queue.pop(0)



        if state.nearby_bots:
            # For the closest bot
            bot = sorted(state.nearby_bots, key=lambda bot: bot.distance)[0]

            logger.info("Target acquired", target=bot)

            # turn at bot, fire (multiple times left/centre/right), then reverse at full speed

            centre_aim = bot.relative_angle
            left_aim = bot.relative_angle - 3
            right_aim = bot.relative_angle + 3

            if state.can_fire:
                r = random.random()
                if r < 0.33:
                    self.queue.append(SetAngle(left_aim))
                elif r < 0.66:
                    self.queue.append(SetAngle(centre_aim))
                else:
                    self.queue.append(SetAngle(right_aim))
                self.queue.append(Fire())

            # If there are bullets nearby, try to dodge them by aiming up/down
            if state.nearby_bullets:
                bullet = sorted(state.nearby_bullets, key=lambda bullet: bullet.distance)[0]
                if bullet.distance < 100:

                    self.queue.append(SetAngle(
                        normalize_angle(bullet.relative_angle + 90)
                    ))

                    for _ in range(500):
                        self.queue.append(SetSpeed(-1.0))
            else:
                # no bullets but nearby bots
                self.queue.append(SetAngle(
                    normalize_angle(bot.relative_angle + 90)
                ))

                for _ in range(500):
                    self.queue.append(SetSpeed(-1.0))

        else:
            # If no nearby bots, just move backwards randomly
            if random.random() < 0.01:
                return Fire()
            if random.random() < 0.02:
                self.queue.append(SetAngle(random.random() * 360))

            return SetSpeed(0.99)


