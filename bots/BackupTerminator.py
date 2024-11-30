import random

from bot import Bot, CurrentState, Action, SetSpeed, SetAngle, Fire
import math

class BackupTerminator(Bot):
    def __init__(self):
        self.queue = [
            SetAngle(random.random() * 360),
            SetSpeed(0.5),
        ]

    def default_name(self):
        return "BackupTerminator"

    def default_color(self):
        return "blue"

    def next(self, state: CurrentState) -> Action | None:
        if state.collision:
            self.queue = []
            return SetAngle(random.random() * 360)
        if self.queue:
            return self.queue.pop(0)

        if state.nearby_bullets:
            return SetSpeed(-1)

        if state.nearby_bots:
            if state.speed != 0.1:
                return SetSpeed(0.1)
            first = state.nearby_bots[0]
            if state.can_fire and abs(state.angle - first.relative_angle) < 1:
                return Fire()
            return SetAngle(first.relative_angle)

        if state.speed != 0.5:
            self.queue = [
                SetSpeed(0.5),
            ]
            return SetAngle(random.random() * 360)
        

def distance2(state, x, y):
    return (state.x - x)** 2 + (state.y -y ) ** 2

def find_nearest(state, objects):
    nearest = None
    dist2 = None
    for object in objects:
        objectDist2 = distance2(state, object.x, object.y)
        if nearest == None or objectDist2 < dist2:
            nearest = object
            dist2 = objectDist2
    return nearest

class Basic3(Bot):
    def __init__(self):
        self.queue = [
            SetAngle(random.random() * 360),
            SetSpeed(0.5),
        ]
        self.evadeTime = 0
    def default_name(self):
        return "basic3"

    def default_color(self):
        return "red"

    def next(self, state: CurrentState) -> Action | None:
        self.evadeTime = max(0, self.evadeTime-1)
        if state.collision:
            self.queue = []
            return SetAngle(random.random() * 360)
        if self.queue:
            return self.queue.pop(0)

        if state.nearby_bullets:
            nearest = find_nearest(state, state.nearby_bullets)
            if self.evadeTime == 0:
                self.evadeTime = 200
                self.queue = [SetAngle(state.angle + 90)]
                return SetSpeed(-1)
        
        if state.nearby_bots:
            if state.speed != 0.1:
                return SetSpeed(0.1)
            nearest = find_nearest(state, state.nearby_bots)
            if state.can_fire and abs(state.angle - nearest.relative_angle) < 1:
                return Fire()
            if distance2(state, nearest.x, nearest.y) < 100:
                if self.evadeTime == 0:
                    self.evadeTime = 200
                    return SetSpeed(-1)
            if self.evadeTime == 0:
                return SetAngle(nearest.relative_angle)

        if state.speed != 0.5:
            self.queue = [
                SetSpeed(0.5),
            ]
            return SetAngle(random.random() * 360)
        