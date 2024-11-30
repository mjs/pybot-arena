from dataclasses import dataclass
from bot import Bot, CurrentState, Action, SetSpeed, SetAngle, Fire
# @dataclass
# class NearbyBot:
#     name: str
#     x: float
#     y: float
#     distance: float
#     speed: float
#     angle: float
#     relative_angle: float


# @dataclass
# class NearbyBullet:
#     x: float
#     y: float
#     distance: float
#     speed: float
#     angle: float
#     relative_angle: float


# @dataclass
# class CurrentState:
#     ticks: int
#     x: float
#     y: float
#     speed: float
#     angle: float
#     collision: bool
#     nearby_bots: list[NearbyBot]
#     nearby_bullets: list[NearbyBullet]
#     can_fire: bool




class zbot(Bot):
    def add_history(self, thisstate):
        # check that history exists
        if not hasattr(self, "history"):
            self.history = []

        self.history.append(thisstate)
        if len(self.history) > 10:
            self.history.pop(0)
    
    def get_history(self):
        return self.history

    def default_name(self) -> str:
        return "ZedBot"

    def default_color(self) -> str:
        return "magenta"

    def next(self, state: CurrentState) -> Action | None:
        
        self.add_history(state)

        if state.collision:
            return SetAngle(107)
        
        if state.speed == 0:
            print("speed is 0")
            return SetSpeed(1)
        
        if state.nearby_bullets:
            for bullet_count,nearbullet in enumerate(state.nearby_bullets):
                if len(self.get_history()) > 1:
                    hist = self.get_history()
                    for old_state in [hist[-1],hist[-2]]:
                        if nearbullet.distance and bullet_count< len(old_state.nearby_bullets) and nearbullet.distance < \
                            old_state.nearby_bullets[bullet_count].distance:
                            return SetAngle(nearbullet.relative_angle+90)


                
        if state.nearby_bots:
            for nearbot in state.nearby_bots:
                if state.can_fire and abs(state.angle - nearbot.relative_angle) < 2:
                    return Fire()
                
                return SetAngle(nearbot.relative_angle)
            

        return SetSpeed(1)
    

