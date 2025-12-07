from enum import IntEnum
from ball import Ball
from game import Game
from paddle import Paddle

class BrickType(IntEnum):
    NONE = 0
    NORMAL = 1
    BALL = 2
    SHIELD = 3
    TWICE = 4

    def label(self):
        if BrickType(self) == 2:
            return "Ball"
        elif BrickType(self) == 3:
            return "Shield"
        elif BrickType(self) == 4:
            return "Twice"
        else:
            return

    def color(self):
        if BrickType(self) == 2:
            return (255,0,0)
        if BrickType(self) == 3:
            return (0,255,0)
        if BrickType(self) == 4:
            return (0,0,255)
        else:
            return (255,255,255)

    def effect(self):
        if self == BrickType.TWICE:
            return BrickType.NORMAL
        elif self == BrickType.BALL:
            Game.balls.append(Ball(100,0,-3,4))
            return BrickType.NONE
        elif self == BrickType.SHIELD:
            Paddle.set_shield()
            return BrickType.NONE
        else:
            return BrickType.NONE

def main():
    for i in range(0,max(BrickType) + 1):
        bt = BrickType(i)
        print(f"i = {i}, bt = {bt}, bt.label = {bt.label()}")

if __name__ == "__main__":
    main()


